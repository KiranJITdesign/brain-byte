"""Pure energy calculation module."""


def daily_kwh(eq) -> float:
    if not eq.is_on:
        return 0.0
    return eq.power_kw * max(0, eq.end_hour - eq.start_hour)


def wasted_hours(eq, room) -> int:
    if not eq.is_on or eq.kind in ("cctv", "electrical"):
        return 0
    on_hours = max(0, eq.end_hour - eq.start_hour)
    overlap = max(0, min(eq.end_hour, room.occupied_to) - max(eq.start_hour, room.occupied_from))
    return max(0, on_hours - overlap)


def room_stats(room) -> dict:
    total = sum(daily_kwh(e) for e in room.equipment)
    wasted = sum(e.power_kw * wasted_hours(e, room) for e in room.equipment)
    return {"daily_kwh": round(total, 2), "wasted_kwh": round(wasted, 2)}


def room_status(stats: dict) -> str:
    if stats["wasted_kwh"] >= 18:
        return "critical"
    if stats["wasted_kwh"] >= 5:
        return "warning"
    return "ok"
