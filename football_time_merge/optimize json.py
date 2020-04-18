import json

with open("result_nomerge.json", 'r') as f:
    tracklets = json.load(f)

delete_tracklets = []
delete_tracklets2 = []
for tracklet in tracklets:
    for frame in tracklets[tracklet]['trails']:
        if 'x' not in frame['pitch']:
            delete_tracklets.append(tracklet)
            break

for tracklet in delete_tracklets:
    del tracklets[tracklet]

for tracklet in tracklets:
    if len(tracklets[tracklet]['trails']) <= 15:
        delete_tracklets2.append(tracklet)

for tracklet in delete_tracklets2:
    del tracklets[tracklet]

optimize_json = json.dumps(tracklets)
with open("result_nomerge_20200416.json", 'w') as f:
    f.write(optimize_json)
f.close()