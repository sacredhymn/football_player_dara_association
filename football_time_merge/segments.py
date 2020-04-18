import json
import copy

with open("result_nomerge_20200416.json") as f:
    tracklets = json.load(f)


# def get_segment_tracklet(start_frame, end_frame):
#     tracklets2 = copy.deepcopy(tracklets)
#     for tracklet in tracklets:
#         for frame in tracklets[tracklet]['trails']:
#             if int(tracklets[tracklet]['trails']["frame_lable"]) > start_frame or int(frame["frame_lable"]) < start_frame:
#                 tracklets2[tracklet]['trails'].remove(frame)
#     # 删除轨迹为空的
#     for tracklet in tracklets:
#         if not tracklets2[tracklet]['trails']:
#             del tracklets2[tracklet]
#     return tracklets2


def get_segment_tracklet(start_frame, end_frame):
    tracklets2 = {}
    for tracklet in tracklets:
        if start_frame <= tracklets[tracklet]['trails'][0]['frame_lable'] <= end_frame:
            tracklets2[tracklet] = tracklets[tracklet]
        if start_frame <= tracklets[tracklet]['trails'][-1]['frame_lable'] <= end_frame:
            tracklets2[tracklet] = tracklets[tracklet]
    return tracklets2