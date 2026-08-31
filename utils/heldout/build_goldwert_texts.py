#!/usr/bin/env python3
"""Rebuild idea_01/run/inputs/texts/goldwert2026_arms.json from the intervention docx files.

The original file was disk-only (license scrub 2026-08-24) and never committed; this script
re-derives it on a fresh clone following the recipe documented in the adapter's
`message_texts_source`: data/goldwert2026/downloads/intervention_docx/*.docx (18 files =
17 interventions + Neutral_Control_Condition), text extracted from word/document.xml.
Arms whose stimulus includes video content that is not on disk are marked inside their text.

Reconstruction note (Haiwen, 2026-08-27): filename -> condName mapping is by construction
(each docx title matches exactly one condName in downloads/advocacy_data.csv); the video
marker wording may differ from Tobi's original disk-only file, everything else is verbatim
docx text. Run: uv run utils/heldout/build_goldwert_texts.py
"""
from __future__ import annotations

import json
import re
import sys
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
DOCX_DIR = REPO / "data" / "goldwert2026" / "downloads" / "intervention_docx"
OUT = REPO / "idea_01" / "run" / "inputs" / "texts" / "goldwert2026_arms.json"

# docx basename -> condName in advocacy_data.csv (18 <-> 18, verified below)
NAME_MAP = {
    "Binding_Moral_Foundations": "BindingMorals",
    "Bipartisan_Elite_Cues": "BipartisanEliteCues",
    "Climate_Activist_Perspective_Taking": "ActivistPerspective",
    "Climate_Policy_Literacy": "ClimatePolicyLiteracy",
    "Co-Benefits": "CoBenefits",
    "Collective_Efficacy_and_Emotional_Benefit": "CollEfficacyEmoBenefit",
    "Connecting_to_Ecological_Disruptions": "EcologicalDisruptions",
    "Dynamic_Anger_Norm": "DynamicAngerNorm",
    "Global_Health_Threat": "GlobalHealthThreat",
    "Guilt-Based_Collective_Responsibility": "GuiltCollResponsibility",
    "Hope_and_Anger_Narratives": "HopeAngerNarratives",
    "Letter_to_Future_Generations": "LetterFuture",
    "Linking_Individual_and_Structural_Change": "IndStructuralChange",
    "Misperception_Correction_Risks": "MispCorrectionRisks",
    "Neutral_Control_Condition": "Control",
    "Shifting_Focus_from_Individual_to_Collective_Action": "ShiftFocusIndColl",
    "System_Justification": "SystemJustification",
    "Threat-Injustice-and-Efficacy": "ThreatInjustEfficacy",
}

VIDEO_RE = re.compile(r"\bvideos?\b|\bwatch\b|\bclip\b", re.IGNORECASE)
VIDEO_NOTE = ("\n\n[VIDEO CONTENT NOT ON DISK: this arm's stimulus includes video material "
              "that is not in the data deposit; the text above is the document's script/"
              "instructions only.]")


def docx_text(path: Path) -> str:
    with zipfile.ZipFile(path) as z:
        xml = z.read("word/document.xml").decode("utf-8")
    paras = []
    for pm in re.finditer(r"<w:p[ >].*?</w:p>", xml, re.S):
        block = pm.group(0)
        runs = re.findall(r"<w:t(?: [^>]*)?>(.*?)</w:t>", block, re.S)
        text = "".join(runs)
        for ent, ch in (("&amp;", "&"), ("&lt;", "<"), ("&gt;", ">"),
                        ("&quot;", '"'), ("&apos;", "'")):
            text = text.replace(ent, ch)
        if text.strip():
            paras.append(text.strip())
    return "\n\n".join(paras)


def main() -> int:
    files = sorted(DOCX_DIR.glob("*.docx"))
    stems = {f.stem for f in files}
    if stems != set(NAME_MAP):
        sys.exit(f"docx set does not match NAME_MAP:\n  extra: {stems - set(NAME_MAP)}"
                 f"\n  missing: {set(NAME_MAP) - stems}")
    out, video_arms = {}, []
    for f in files:
        arm = NAME_MAP[f.stem]
        text = docx_text(f)
        if not text:
            sys.exit(f"{f.name}: extracted no text")
        if VIDEO_RE.search(text):
            text += VIDEO_NOTE
            video_arms.append(arm)
        out[arm] = text
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, indent=1, ensure_ascii=False))
    words = {a: len(t.split()) for a, t in out.items()}
    print(f"wrote {OUT.relative_to(REPO)}: {len(out)} arms, "
          f"{min(words.values())}-{max(words.values())} words")
    print(f"video-marked arms ({len(video_arms)}): {', '.join(video_arms) or 'none'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
