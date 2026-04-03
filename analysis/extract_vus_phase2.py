import json
import sys
import math
from datetime import datetime

STAGES = [
    ("1 VU",   60),
    ("10 VU",  60),
    ("50 VU",  60),
    ("100 VU", 60),
    ("200 VU", 60),
]
RAMP_GRACE = 5


def percentile(sv, p):
    if not sv:
        return None
    n = len(sv)
    idx = (p / 100) * (n - 1)
    lo = int(idx)
    hi = lo + 1
    if hi >= n:
        return sv[-1]
    return sv[lo] + (idx - lo) * (sv[hi] - sv[lo])


def stats(values):
    if not values:
        return {"mean": None, "p50": None, "p95": None, "p99": None, "std_dev": None, "count": 0}
    n = len(values)
    mean = sum(values) / n
    variance = sum((v - mean) ** 2 for v in values) / (n - 1) if n > 1 else 0.0
    sv = sorted(values)
    return {
        "mean":    round(mean, 3),
        "p50":     round(percentile(sv, 50), 3),
        "p95":     round(percentile(sv, 95), 3),
        "p99":     round(percentile(sv, 99), 3),
        "std_dev": round(math.sqrt(variance), 3),
        "count":   n,
    }


def extract(filepath):
    points = []
    with open(filepath) as fh:
        for line in fh:
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            if obj.get("type") == "Point" and obj.get("metric") == "http_req_duration":
                ts = datetime.fromisoformat(obj["data"]["time"].replace("Z", "+00:00"))
                points.append((ts, float(obj["data"]["value"])))

    if not points:
        return []

    points.sort(key=lambda x: x[0])
    run_start = points[0][0]

    windows, offset = [], 0
    for label, dur in STAGES:
        windows.append((label, offset + RAMP_GRACE, offset + dur))
        offset += dur

    buckets = {label: [] for label, _, _ in windows}
    for ts, value in points:
        elapsed = (ts - run_start).total_seconds()
        for label, s, e in windows:
            if s <= elapsed < e:
                buckets[label].append(value)
                break

    return [{"stage": label, **stats(buckets[label])} for label, _, _ in windows]


def main():
    if len(sys.argv) < 2:
        sys.exit(1)

    results = []
    for filepath in sys.argv[1:]:
        name = filepath.replace("\\", "/").split("/")[-1]
        stages = extract(filepath)
        if stages:
            results.append({"file": name, "stages": stages})

    out_path = "./phase2_vus_results.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)

if __name__ == "__main__":
    main()