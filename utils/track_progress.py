#!/usr/bin/env python3
"""Operator-side progress ledger: one row per Prime Agent session.

Aggregates what the three papers behind Prime Agent track — performance vs. compute:
  - harness cost   (tokens + $ from the arm's session JSONLs, exact provider counts)
  - simulator cost (billed tokens from each run's stages/*/cost.json, best-effort
                    matched to the session by timestamp window)
  - practice skill (non-stub, non-TARGET scoreboard rows produced in the window)

Usage:  uv run utils/track_progress.py [--idea idea_01] [--arm main]
Writes docs/progress-ledger.md. Read-only over .container-state/ and runs/.
"""
import argparse
import csv
import json
import statistics
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKEW = timedelta(hours=3)  # container-vs-host clock/timezone tolerance for run matching


def ts(s):
    if not s:
        return None
    s = s.replace("Z", "+00:00")
    d = datetime.fromisoformat(s)
    return d if d.tzinfo else d.replace(tzinfo=timezone.utc)


def walk_usage(obj, acc):
    if isinstance(obj, dict):
        u = obj.get("usage")
        if isinstance(u, dict) and "totalTokens" in u:
            acc["tokens"] += u.get("totalTokens", 0)
            acc["cost"] += (u.get("cost") or {}).get("total", 0.0)
        for v in obj.values():
            walk_usage(v, acc)
    elif isinstance(obj, list):
        for v in obj:
            walk_usage(v, acc)


def billed_in(obj):
    if isinstance(obj, dict):
        return sum(
            v if isinstance(v, (int, float)) and k in ("billed_est", "billed", "billed_tokens") else billed_in(v)
            for k, v in obj.items()
        )
    if isinstance(obj, list):
        return sum(billed_in(v) for v in obj)
    return 0


def ledger34(a):
    """idea_03 / idea_04: snapshots + Prime session JSONLs + a run_id-keyed scoreboard.
    idea_03's artifacts live in the escrow bundle (sessions were run on the operator's machine);
    idea_04's in .container-state. No simulator stages exist in either campaign (zero calls)."""
    if a.idea == "idea_03":
        base = ROOT / "submission/escrow/idea03_raw_logs"
        snapdir, prime = base / "snapshots", base / "prime_sessions/main/prime"
    else:
        snapdir, prime = ROOT / ".container-state/snapshots", ROOT / f".container-state/arms/{a.idea}/{a.arm}/prime"
    sessions = []
    for rj in sorted(snapdir.glob("*/run.json")):
        try:
            r = json.load(rj.open())
        except Exception:  # noqa: BLE001
            continue
        if r.get("idea") != a.idea or r.get("arm") != a.arm:
            continue
        start, end = ts(r.get("started_at")), ts(r.get("ended_at"))
        if not start:
            continue  # a killed wrapper leaves ended_at null (idea_03 s1) — end recovered from the JSONL below
        sessions.append({"id": r["run_id"], "start": start, "end": end,
                         "exit": r.get("exit_status"), "frozen": r.get("frozen_intact")})
    # One Prime JSONL = one session: assign each file to the run whose launch window contains the
    # file's own "session" entry timestamp (archives are stamped by the NEXT launch). Usage =
    # assistant messages' usage + per-call sub-agent childUsage — never the cumulative
    # aggregateUsage, never streaming duplicates.
    jsonls = list((prime / "sessions").glob("*.jsonl")) + list(prime.glob("_archive-*/sessions/*.jsonl"))
    from datetime import datetime as _dt
    starts = sorted((se["start"], se["id"]) for se in sessions)
    per_run = {}
    for f in jsonls:
        acc = {"tokens": 0, "cost": 0.0}
        opened = last = None
        for line in f.open():
            try:
                d = json.loads(line)
            except Exception:  # noqa: BLE001
                continue
            if d.get("type") == "session":
                opened = ts(d.get("timestamp"))
            m = d.get("message") or {}
            if d.get("type") == "message" and m.get("role") == "assistant":
                u = m.get("usage") or {}
                acc["tokens"] += u.get("totalTokens", 0)
                acc["cost"] += (u.get("cost") or {}).get("total", 0.0)
                if isinstance(m.get("timestamp"), (int, float)):
                    last = _dt.fromtimestamp(m["timestamp"] / 1000, tz=timezone.utc)
            elif d.get("type") == "child_usage_attributed":
                u = d.get("childUsage") or {}
                acc["tokens"] += u.get("totalTokens", 0)
                acc["cost"] += (u.get("cost") or {}).get("total", 0.0)
                if isinstance(d.get("timestamp"), str):
                    last = ts(d["timestamp"]) or last
        if not opened:
            continue
        owner = None
        for n, (st, rid) in enumerate(starts):
            nxt = starts[n + 1][0] if n + 1 < len(starts) else None
            if st - timedelta(minutes=2) <= opened and (nxt is None or opened < nxt):
                owner = rid
        if owner:
            r = per_run.setdefault(owner, {"tokens": 0, "cost": 0.0, "last": None})
            r["tokens"] += acc["tokens"]; r["cost"] += acc["cost"]
            if last and (r["last"] is None or last > r["last"]):
                r["last"] = last
    for se in sessions:
        r = per_run.get(se["id"], {"tokens": 0, "cost": 0.0, "last": None})
        se["harness_tokens"], se["harness_cost"] = r["tokens"], r["cost"]
        if se["end"] is None:
            se["end"] = r["last"] or se["start"]
    sb = ROOT / a.idea / "run/runs/scoreboard.csv"
    rows = list(csv.DictReader(sb.open())) if sb.is_file() else []
    for se in sessions:
        sc = [r for r in rows if r["run_id"] == se["id"] and r.get("stub") in ("False", "false", None, "")]
        se["n_scored"] = len(sc)
        for col, name in [("r_adj", "r_adj"), ("r_within_adj", "rwo"),
                          ("rmse_adj_pp", "rmse"), ("cal_beta", "beta")]:
            vals = []
            for r in sc:
                try:
                    v = float(r[col])
                except (KeyError, TypeError, ValueError):
                    continue
                if name in ("r_adj", "rwo") and abs(v) > 1.0:
                    continue  # pre-A4 idea_03 s1 scores exploded on ~zero-reliability halves; A4 clamps to [-1,1]
                vals.append(v)
            se[name] = statistics.mean(vals) if vals else None
    out = [
        f"# Progress ledger — {a.idea}, arm {a.arm} (one row per Prime Agent session)", "",
        f"Generated by `utils/track_progress.py --idea {a.idea}`; regenerate after every session.",
        "Harness tokens/$ are the provider counts from the Prime session JSONLs (main agent +",
        "attributed sub-agent usage in-window; $ is the API-equivalent display, all spend ran over",
        "subscription OAuth). Zero simulator calls in this campaign. Practice metrics average the",
        "session's non-stub scoreboard rows — ADJUSTED metrics (r_adj / r_within_adj / RMSE_adj);",
        "cross-session comparability caveats per the campaign log (instrument, reliability rule).", "",
        "| session | start (UTC) | h | exit | harness Mtok | API-equiv $ | scored rows | mean r_adj | r_within_adj | RMSE_adj pp | β |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    f2 = lambda v, fmt="{:.2f}": fmt.format(v) if v is not None else "—"  # noqa: E731
    tot = {"ht": 0, "hc": 0.0}
    for se in sessions:
        if se["harness_tokens"] == 0 and se["n_scored"] == 0 and (se["end"] - se["start"]) < timedelta(minutes=6):
            continue  # wedged/aborted launch with no session file — not a session
        hours = (se["end"] - se["start"]).total_seconds() / 3600
        tot["ht"] += se["harness_tokens"]; tot["hc"] += se["harness_cost"]
        out.append(
            f"| {se['id']} | {se['start']:%m-%d %H:%M} | {hours:.1f} | {se['exit'] if se['exit'] is not None else '—'}"
            f"{' ⚠frozen' if se['frozen'] is False else ''} | {se['harness_tokens']/1e6:.2f} | {se['harness_cost']:.2f}"
            f" | {se['n_scored']} | {f2(se['r_adj'])} | {f2(se['rwo'])} | {f2(se['rmse'])} | {f2(se['beta'])} |")
    out.append(f"| **total** | | | | **{tot['ht']/1e6:.2f}** | **{tot['hc']:.2f}** | | | | | |")
    out.append("")
    dest = ROOT / f"docs/progress-ledger-{a.idea.replace('idea_', 'idea')}.md"
    dest.write_text("\n".join(out))
    print(f"{len(sessions)} sessions -> {dest.relative_to(ROOT)} "
          f"(harness {tot['ht']/1e6:.1f}M tok / ${tot['hc']:.0f})")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--idea", default="idea_01")
    ap.add_argument("--arm", default="main")
    a = ap.parse_args()
    if a.idea in ("idea_03", "idea_04"):
        return ledger34(a)

    run_dir = ROOT / a.idea / "run"
    snaps = sorted((ROOT / ".container-state/snapshots").glob(f"*_{a.idea}_{a.arm}"))
    sessions = []
    for s in snaps:
        try:
            r = json.load((s / "run.json").open())
        except Exception:  # noqa: BLE001
            continue
        start, end = ts(r.get("started_at")), ts(r.get("ended_at"))
        if not start or not end or (end - start) < timedelta(minutes=2):
            continue  # skip aborted/instant launches
        sessions.append({"id": r["run_id"], "start": start, "end": end,
                         "exit": r.get("exit_status"), "frozen": r.get("frozen_intact")})

    # exact harness usage per session, from the arm's session JSONLs
    arm_dir = ROOT / f".container-state/arms/{a.idea}/{a.arm}/prime"
    jsonls = list((arm_dir / "sessions").glob("*.jsonl")) \
        + list(arm_dir.glob("_archive-*/sessions/*.jsonl")) \
        + list(arm_dir.glob("_stale-*/sessions/*.jsonl"))
    for se in sessions:
        acc = {"tokens": 0, "cost": 0.0}
        for f in jsonls:
            for line in f.open():
                if '"usage"' not in line:
                    continue
                try:
                    d = json.loads(line)
                except Exception:  # noqa: BLE001
                    continue
                t = ts(d.get("timestamp"))
                if t and se["start"] <= t <= se["end"]:
                    walk_usage(d, acc)
        se["harness_tokens"], se["harness_cost"] = acc["tokens"], acc["cost"]

    # simulator billed tokens + scoreboard metrics per harness run, matched by window
    inner = []
    for rj in sorted(run_dir.glob("runs/*/run.json")):
        try:
            r = json.load(rj.open())
        except Exception:  # noqa: BLE001
            continue
        started = ts(r.get("started"))
        billed = sum(billed_in(json.load(c.open())) for c in rj.parent.glob("stages/*/cost.json"))
        inner.append({"rid": rj.parent.name, "start": started, "billed": billed})

    rows = list(csv.DictReader((run_dir / "runs/scoreboard.csv").open())) \
        if (run_dir / "runs/scoreboard.csv").is_file() else []

    # each inner run belongs to exactly ONE session: the containing window if any,
    # else the nearest within SKEW (container clocks may drift from the host's)
    def dist(se, t):
        if se["start"] <= t <= se["end"]:
            return timedelta(0)
        return min(abs(t - se["start"]), abs(t - se["end"]))

    owner = {}
    for i in inner:
        if not i["start"] or not sessions:
            continue
        best = min(sessions, key=lambda se: dist(se, i["start"]))
        if dist(best, i["start"]) <= SKEW:
            owner[i["rid"]] = best["id"]

    for se in sessions:
        mine = [i for i in inner if owner.get(i["rid"]) == se["id"]]
        se["sim_billed"] = sum(i["billed"] for i in mine)
        rids = {i["rid"] for i in mine}
        sc = [r for r in rows if r["run_id"] in rids and r["stub"] == "False"
              and r["task_id"] != "TARGET"]
        se["n_scored"] = len(sc)
        for col, name in [("spearman_rho", "rho"), ("pearson_r_within_outcomes", "rwo"),
                          ("rmse_pp", "rmse"), ("cal_beta", "beta")]:
            vals = [float(r[col]) for r in sc if r.get(col) not in (None, "", "nan")]
            se[name] = statistics.mean(vals) if vals else None

    out = [
        "# Progress ledger — one row per Prime Agent session",
        "",
        f"Generated by `utils/track_progress.py` (idea={a.idea}, arm={a.arm}); regenerate after every session.",
        "Harness tokens are the provider's own counts from the session logs; the $ column",
        "is Prime Agent's API-EQUIVALENT price display — all spend runs over subscription",
        "OAuth (harness login + simulator CLAUDE_CODE_OAUTH_TOKEN), no metered API billing. Simulator",
        "billed tokens come from each run's `cost.json` (window-matched, ±3h skew).",
        "Practice metrics average the session's non-stub, non-TARGET scoreboard rows —",
        "cross-session comparability is judged per `docs/self-improvement-loop.md` (LOSO,",
        "design-twin protection), not from this table alone.",
        "",
        "| session | start (UTC) | h | exit | harness Mtok | API-equiv $ | sim billed Mtok | scored rows | mean ρ | within-r | RMSE pp | β |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    f2 = lambda v, fmt="{:.2f}": fmt.format(v) if v is not None else "—"  # noqa: E731
    tot = {"ht": 0, "hc": 0.0, "sb": 0}
    for se in sessions:
        hours = (se["end"] - se["start"]).total_seconds() / 3600
        tot["ht"] += se["harness_tokens"]; tot["hc"] += se["harness_cost"]; tot["sb"] += se["sim_billed"]
        out.append(
            f"| {se['id']} | {se['start']:%m-%d %H:%M} | {hours:.1f} | {se['exit']}"
            f"{'' if se['frozen'] else ' ⚠frozen'} | {se['harness_tokens']/1e6:.2f} | {se['harness_cost']:.2f}"
            f" | {se['sim_billed']/1e6:.2f} | {se['n_scored']}"
            f" | {f2(se['rho'])} | {f2(se['rwo'])} | {f2(se['rmse'])} | {f2(se['beta'])} |")
    out.append(f"| **total** | | | | **{tot['ht']/1e6:.2f}** | **{tot['hc']:.2f}** | **{tot['sb']/1e6:.2f}** | | | | | |")
    out.append("")
    (ROOT / "docs/progress-ledger.md").write_text("\n".join(out))
    print(f"{len(sessions)} sessions -> docs/progress-ledger.md "
          f"(harness {tot['ht']/1e6:.1f}M tok / ${tot['hc']:.0f}, simulator {tot['sb']/1e6:.1f}M billed)")


if __name__ == "__main__":
    main()
