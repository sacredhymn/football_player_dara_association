import random
import datetime
import json
import pandas as pd
from segments import get_segment_tracklet

with open("result_nomerge_20200416.json", 'r') as f:
    socker_data = json.load(f)


class solve_threshold:
    def __init__(self, segments, start_frame, end_frame):
        self.segments = segments
        self.start_frame = start_frame
        self.end_frame = end_frame
        self.cluster1 = []
        self.cluster2 = []

    def compute_cost(self, tuple1, tuple2):
        tracklet1, tracklet2 = tuple1[0], tuple2[0]
        f1, f2 = tuple1[1], tuple2[1]
        x1, y1, c1 = tuple1[2][0], tuple1[2][1], tuple1[3]
        x2, y2, c2 = tuple2[2][0], tuple1[2][1], tuple2[3]
        distance = ((x1 - x2) ** 2.0 + (y1 - y2) ** 2.0) ** 0.5
        frame_distance = 1.0
        if f1 < f2:
            frame_distance = 0.0
        color_distance = 1.0
        if c1 == c2:
            color_distance = 0.0
        tracklet_distance = 1.0
        if tracklet1 == tracklet2:
            tracklet_distance = 0.0
        return (distance + frame_distance + color_distance) * tracklet_distance

    def pre_process(self):
        cluster1 = self.cluster1
        cluster2 = self.cluster2
        for tracklet in self.segments:
            index1 = self.segments[tracklet]['trails'][-1]
            index2 = self.segments[tracklet]['trails'][0]
            if index1['frame_lable'] < self.end_frame:
                cluster1.append((tracklet, index1['frame_lable'],
                                 (index1['pitch']['x'], index1['pitch']['y']), index1['pitch']['color']))
            if index2['frame_lable'] > self.start_frame:
                cluster2.append((tracklet, index2['frame_lable'],
                                 (index2['pitch']['x'], index2['pitch']['y']), index2['pitch']['color']))
        return cluster1, cluster2

    def generate_cost_mat(self):
        cluster1, cluster2 = self.cluster1, self.cluster2
        columns = [element1[0] for element1 in cluster1]
        rows = [element2[0] for element2 in cluster2]
        mat = pd.DataFrame(index=rows, columns=columns)
        for tuple1 in cluster1:  # 横着的索引
            for tuple2 in cluster2:  # 竖着的索引
                mat[tuple1[0]][tuple2[0]] = self.compute_cost(tuple1, tuple2)
        return mat

    def link(self, mat):
        rows, columns = mat.shape
        link_list = {}
        while rows > 0 and columns > 0:
            min_index = mat.stack().astype('float64').idxmin()  # 先是行索引，再是列索引
            value = mat[min_index[1]][min_index[0]]
            mat = mat.drop(min_index[0], axis=0, inplace=False)  # 删除行, min_index[0]对应segments2
            mat = mat.drop(min_index[1], axis=1, inplace=False)  # 删除列, min_index[1]对应segments1
            if min_index[1] != min_index[0] and value < 1.0:
                print(min_index[1], "->", min_index[0])
                link_list[min_index[1]] = min_index[0]
            rows, columns = mat.shape
        return mat, link_list


if __name__ == "__main__":
    i = -15
    link_lists = {}
    while i < 1600:
        i += 15
        start_frame = i
        end_frame = start_frame + 15
        segments = get_segment_tracklet(start_frame, end_frame)
        Solver = solve_threshold(segments, start_frame, end_frame)
        Solver.pre_process()
        mat = Solver.generate_cost_mat()
        # print(mat)
        mat, link_list = Solver.link(mat)
        for key in link_list.keys():
            link_lists[key] = link_list[key]
        # print(mat)
        # print(link_list)
    str_link_list = json.dumps(link_lists)
    with open('data_association_nomerge.json', 'w') as f:
        f.write(str_link_list)
    f.close()