from optimize_json import tracklets
import pandas as pd
import json


class cost_mat:
    def __init__(self, tracklets):
        self.tracklets = tracklets
        self.cluster1 = []
        self.cluster2 = []

    def pre_process(self):
        cluster1 = self.cluster1
        cluster2 = self.cluster2
        for tracklet in self.tracklets:
            frame_x_y = {}
            for frame in self.tracklets[tracklet]['trails']:
                frame_x_y[frame['frame_lable']] = (frame['pitch']['x'], frame['pitch']['y'])
            start = self.tracklets[tracklet]['trails'][0]
            end = self.tracklets[tracklet]['trails'][-1]
            if 'cam01' in start.keys():
                cluster1.append((tracklet, (start['frame_lable'], end['frame_lable']), frame_x_y, start['pitch']['color']))
            elif 'cam02' in start.keys():
                cluster2.append((tracklet, (start['frame_lable'], end['frame_lable']), frame_x_y, start['pitch']['color']))
        return cluster1, cluster2

    def compute_cost(self, tuple1, tuple2):
        f1_start, f1_end, f2_start, f2_end = tuple1[1][0], tuple1[1][1], tuple2[1][0], tuple2[1][1]
        frame_x_y1, frame_x_y2 = tuple1[2], tuple2[2]
        c1, c2 = tuple1[3], tuple2[3]
        color_distance = 1.0
        if c1 == c2:
            color_distance = 0.0
        frame_distance = 1.0
        distance = 0.0
        count_start_frame = max(f1_start, f2_start)
        count_end_frame = min(f1_end, f2_end)
        intersect = count_end_frame - count_start_frame
        if intersect > 0.0:
            frame_distance = 0.0
            frame_count = count_start_frame
            while frame_count <= count_end_frame:
                if frame_count not in frame_x_y1 or frame_count not in frame_x_y2:
                    frame_count += 1
                    continue
                distance += ((frame_x_y1[frame_count][0] - frame_x_y2[frame_count][1]) ** 2 +
                             (frame_x_y1[frame_count][0] - frame_x_y2[frame_count][1]) ** 2) ** 0.5
                frame_count += 1
            distance = distance / intersect
        cost = distance + color_distance + frame_distance
        return cost

    def get_cost_mat(self):
        columns = [element1[0] for element1 in self.cluster1]
        rows = [element2[0] for element2 in self.cluster2]
        mat = pd.DataFrame(index=rows, columns=columns)
        for tuple1 in self.cluster1:
            for tuple2 in self.cluster2:
                mat[tuple1[0]][tuple2[0]] = self.compute_cost(tuple1, tuple2)
        mat.to_csv("mat.csv")
        return mat

    def link(self, mat):
        rows, columns = mat.shape
        link_list = {}
        while rows > 0 and columns > 0:
            min_index = mat.stack().astype('float64').idxmin()  # 先是行索引，再是列索引
            value = mat[min_index[1]][min_index[0]]
            mat = mat.drop(min_index[0], axis=0, inplace=False)  # 删除行, min_index[0]对应segments2
            mat = mat.drop(min_index[1], axis=1, inplace=False)  # 删除列, min_index[1]对应segments1
            if value < 1.0:
                print(min_index[1], "->", min_index[0])
                link_list[min_index[1]] = min_index[0]
            rows, columns = mat.shape
        return mat, link_list


if __name__ == "__main__":
    Solver = cost_mat(tracklets)
    Solver.pre_process()
    mat = Solver.get_cost_mat()
    mat, link_list = Solver.link(mat)
    json_link_list = json.dumps(link_list)
    with open("spatial.json", 'w') as f:
        f.write(json_link_list)
    f.close()
