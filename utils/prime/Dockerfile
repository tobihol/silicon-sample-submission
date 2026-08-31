# The runtime for silicon-sample-submission idea sessions: Prime Agent + the Claude Code
# CLI that simulator calls go through. Adapted from gssim_prime (same pinning, same kernel
# venv layout). The image holds NO credentials: Prime Agent's auth enters as a bind-mounted
# auth.json, the Claude CLI's as CLAUDE_CODE_OAUTH_TOKEN from the launcher's env file.
#
# Build (full runbook in utils/README.md):
#   docker build -t ssb-prime:latest utils/prime/
FROM node:22-bookworm-slim

# R is here for two reasons: design-based estimates come from the survey package, and the
# benchmark's shipped helper scripts (make clean / manifest / check in the submission
# template) are R and need tidyverse + jsonlite + digest. build-essential + gfortran let a
# session install further R packages at runtime.
RUN apt-get update && apt-get install -y --no-install-recommends \
        git ca-certificates curl jq procps openssh-client make \
        build-essential gfortran \
        r-base r-cran-haven r-cran-survey r-cran-jsonlite \
        r-cran-tidyverse r-cran-digest \
    && rm -rf /var/lib/apt/lists/*

# uv provides the Python for Prime Agent's IPython kernel (global rule: never bare pip)
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /usr/local/bin/

# Prime Agent is not on the npm registry — it ships as a signed tarball from the release
# bucket, which is what the upstream install script fetches. Pinning version + checksum
# here makes the image reproducible and removes the curl|sh step from the build.
ARG PRIME_AGENT_VERSION=0.7.2
ARG PRIME_AGENT_SHA256=bc5471f2a626d727b88a45eb745fff93b10c554a3c4fc5912f25d8c64b987f5e
ARG PRIME_AGENT_BASE_URL=https://pub-728493de92a943e2a9b2d17b4719f318.r2.dev
RUN curl -fsSL "${PRIME_AGENT_BASE_URL}/releases/v${PRIME_AGENT_VERSION}/prime-agent-${PRIME_AGENT_VERSION}.tgz" \
        -o /tmp/prime-agent.tgz \
    && echo "${PRIME_AGENT_SHA256}  /tmp/prime-agent.tgz" | sha256sum -c - \
    && npm install -g --no-fund --no-audit /tmp/prime-agent.tgz \
    && rm /tmp/prime-agent.tgz

# The Claude Code CLI is the simulator interface (plain completions), never an agent here.
ARG CLAUDE_CODE_VERSION=2.1.220
RUN npm install -g @anthropic-ai/claude-code@${CLAUDE_CODE_VERSION}

# The repo is bind-mounted by a host user whose uid differs from the container user;
# without this git refuses every command with "dubious ownership".
RUN git config --system safe.directory '*'

RUN useradd --create-home --shell /bin/bash agent

# The IPython kernel venv is baked into the image at a fixed path instead of being
# bootstrapped into ~/.prime at first use. Two reasons: a run does not spend its first
# minutes building a venv, and ~/.prime then holds ONLY experimental state (harness
# state, sessions, auth) — so wiping it between arms wipes nothing else.
# prime-agent-runtime is not on PyPI — it ships inside the npm package as a source tree
# with its own pyproject.toml. Installing it from there is deterministic; the alternative
# (PRIME_AGENT_BOOTSTRAP_KERNEL_ON_INSTALL) is an undocumented env var. As of 0.7.2
# PRIME_AGENT_KERNEL_VENV itself is documented (docs/skills.md); do NOT switch to
# PRIME_AGENT_KERNEL_PYTHON — with it Prime Agent installs nothing into the env, which
# disables Python-backed project skills (idea_01's `ssb`).
# Prime Agent installs its bundled Python skills into this venv at first kernel start,
# which is why the session user owns it.
# UV_PYTHON_INSTALL_DIR: without it uv drops the managed interpreter in root's cache and
# the venv's bin/python symlink dangles for the session user ("Permission denied").
# The venv lives one level down, in a directory the session user owns, because Prime Agent
# takes its bootstrap lock at "<venv>.bootstrap.lock" — a SIBLING of the venv. With the venv
# directly in /opt that mkdir is denied and every ipython call fails with EACCES.
ENV PRIME_AGENT_KERNEL_VENV=/opt/kernel/venv \
    UV_PYTHON_INSTALL_DIR=/opt/uv-python
RUN mkdir -p /opt/kernel \
    && uv python install 3.11 \
    && uv venv --python 3.11 ${PRIME_AGENT_KERNEL_VENV} \
    && uv pip install --python ${PRIME_AGENT_KERNEL_VENV}/bin/python \
         ipykernel /usr/local/lib/node_modules/prime-agent/dist/prime-agent-runtime \
    && chown -R agent:agent /opt/kernel ${UV_PYTHON_INSTALL_DIR}

# The mount skeleton is created root-owned before dropping privileges: the session user can
# write only inside the bind mounts, never at the /workspace root. The single-file mounts
# need their mountpoints to exist first — docker cannot create them inside a bind mount.
RUN mkdir -p /workspace/run /workspace/datasets /workspace/benchmark \
    && touch /workspace/pyproject.toml /workspace/uv.lock /workspace/.python-version
# Writable site-library so non-interactive install.packages() works; installs land in the
# ephemeral layer, so each session reinstalls what it needs.
RUN chown agent:agent /usr/local/lib/R/site-library

# Docker creates missing mountpoint parents root-owned, so without this /home/agent/.prime
# (parent of the bind-mounted agent/ state dir) is unwritable and /login dies with EACCES
# writing its ~/.prime/.config.json tmp file. Credentials themselves persist in the
# mounted ~/.prime/agent/auth.json (docs/providers.md), so pre-owning the parent is enough.
RUN mkdir -p /home/agent/.prime/agent && chown -R agent:agent /home/agent/.prime

USER agent
# UV_PROJECT_ENVIRONMENT keeps the workspace venv in the container HOME: the repo is shared
# with the host, and a .venv inside it would be stale on every host<->container switch.
# PRIME_AGENT_TELEMETRY / DO_NOT_TRACK: 0.7.2 added pseudonymous product analytics,
# default ON — a hermetic research container reports nothing. PI_SKIP_VERSION_CHECK
# drops the startup release-manifest fetch (one less network dependency; self-update
# would break the version pin anyway).
ENV HOME=/home/agent \
    LANG=C.UTF-8 \
    LC_ALL=C.UTF-8 \
    UV_PROJECT_ENVIRONMENT=/home/agent/.venv-workspace \
    PRIME_AGENT_TELEMETRY=0 \
    DO_NOT_TRACK=1 \
    PI_SKIP_VERSION_CHECK=1

# The lock check is not decoration: Prime Agent creates "<venv>.bootstrap.lock" on the first
# ipython call, and if the session user cannot make it, every tool call fails with EACCES
# while the agent looks healthy from the outside.
RUN prime-agent --version && claude --version \
    && Rscript -e 'library(haven); library(survey); library(jsonlite); library(tidyverse); library(digest)' \
    && mkdir "${PRIME_AGENT_KERNEL_VENV}.bootstrap.lock" \
    && rmdir "${PRIME_AGENT_KERNEL_VENV}.bootstrap.lock" \
    && ${PRIME_AGENT_KERNEL_VENV}/bin/python -c 'import rlm, ipykernel'

WORKDIR /workspace/run
CMD ["prime-agent"]
