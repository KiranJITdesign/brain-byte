import json
import logging
import os
from google import genai

log = logging.getLogger("ecowatt.ai")
MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
_key = os.getenv("GEMINI_API_KEY")
_client = genai.Client(api_key=_key) if _key else None

SYSTEM = (
    "You are EcoWatt, an energy-efficiency advisor for a 5-floor college campus digital twin. "
    "Use ONLY the data provided. Be specific: name floors, rooms, kWh figures and rupee savings (tariff Rs 8 per kWh)."
)


def _fallback(ctx: dict) -> str:
    if not ctx.get("alerts"):
        return "No major energy wastage detected right now."
    top = ctx["alerts"][0]
    return f"(offline summary) {top['message']} Recommended action: switch equipment off outside occupied hours."


def ask(ctx: dict, question: str | None = None, mode: str = "chat") -> str:
    if mode == "report":
        task = "Write a concise 5-floor campus energy-saving report with: Summary, Top 3 issues, Recommended actions, Estimated savings."
    else:
        task = question or "Explain the biggest anomaly and what to do about it."
    prompt = f"{SYSTEM}\n\nCAMPUS DATA (JSON):\n{json.dumps(ctx)}\n\nTASK: {task}"
    if _client is None:
        return _fallback(ctx)
    try:
        return _client.models.generate_content(model=MODEL, contents=prompt).text
    except Exception:
        log.exception("Gemini call failed; using fallback")
        return _fallback(ctx)
