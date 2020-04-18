import json

all_lenth = []
with open("data_result_20200413_result.json") as f:
    tracklets = json.load(f)

# 一共有556条轨迹
for tracklet in tracklets:
    all_lenth.append(len(tracklets[tracklet]['trails']))
print(all_lenth)
all_lenth.sort()
print(all_lenth)
