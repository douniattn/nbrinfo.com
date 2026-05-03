#!/usr/bin/env python3
"""Parse nuerburgring.de/open-hours HTML and extract Nordschleife TF status."""

import re, html, json, sys, os
from datetime import datetime, timezone

def main():
    html_path = sys.argv[1]
    out_path = sys.argv[2]

    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    result = {"status": "unknown", "detail": "Could not parse", "time": now, "periods": []}

    if not os.path.exists(html_path) or os.path.getsize(html_path) < 1000:
        result["detail"] = "Fetch failed"
        with open(out_path, "w") as f:
            json.dump(result, f, indent=2)
        print(json.dumps(result, indent=2))
        return

    with open(html_path, "r", errors="replace") as f:
        data = f.read()

    # Find event-inline-12 (Touristenfahrten Nordschleife) and its data-schedule
    pattern = r'event-inline-12">(.*?)</a>.*?data-schedule="([^"]+)"'
    match = re.search(pattern, data, re.DOTALL)

    if match:
        schedule_raw = html.unescape(match.group(2))
        schedule = json.loads(schedule_raw)
        day_data = schedule.get(today, {})

        # Handle exclusion wrapper (used for special events on TF days)
        if isinstance(day_data, dict) and "exclusion" in day_data:
            day_data = day_data["exclusion"]

        opened = day_data.get("opened", False) if isinstance(day_data, dict) else False
        periods = day_data.get("periods", []) if isinstance(day_data, dict) else []
        message = day_data.get("message", {}) if isinstance(day_data, dict) else {}
        msg_en = (message.get("en") or message.get("de") or "").strip()

        if opened and periods:
            result["status"] = "open"
            result["detail"] = f"Open {periods[0]['start']}\u2013{periods[-1]['end']}"
            if msg_en:
                result["detail"] += f" ({msg_en})"
        elif opened:
            result["status"] = "open"
            result["detail"] = msg_en if msg_en else "Open"
        else:
            result["status"] = "closed"
            result["detail"] = msg_en if msg_en else "Closed today"

        result["periods"] = periods
    else:
        # Fallback: look for status keywords near Touristenfahrten
        tf_idx = data.find("Touristenfahrten Nordschleife")
        if tf_idx > -1:
            nearby = data[tf_idx:tf_idx+500].upper()
            if "GESCHLOSSEN" in nearby:
                result["status"] = "closed"
                result["detail"] = "Closed"
            elif "GEÖFFNET" in nearby or "OPENED" in nearby:
                result["status"] = "open"
                result["detail"] = "Open"

    result["time"] = now
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
