import json, os, math

def summarize(filename):
    values = []
    with open(filename) as f:
        for line in f:
            try:
                d = json.loads(line)
                if d.get('type') == 'Point' and d.get('metric') == 'http_req_duration':
                    values.append(d['data']['value'])
            except:
                continue
    if not values:
        return None
    values.sort()
    n = len(values)
    avg = sum(values)/n
    p50 = values[int(n*0.50)]
    p95 = values[int(n*0.95)]
    p99 = values[int(n*0.99)]
    mn = min(values)
    mx = max(values)
    std = math.sqrt(sum((x-avg)**2 for x in values)/n)
    return {'n':n,'avg':avg,'p50':p50,'p95':p95,'p99':p99,'min':mn,'max':mx,'std':std}

files = sorted([f for f in os.listdir('/home/ubuntu') if f.endswith('.json')])
results = {}
for f in files:
    s = summarize(f'/home/ubuntu/{f}')
    if s:
        results[f] = s

with open('/home/ubuntu/all_summaries.json', 'w') as f:
    json.dump(results, f, indent=2)
