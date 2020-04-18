import sys
import cv2
import json
from optimize_json import tracklets

video_cam01 = "videos/0105CAM01.mp4"
video_cam02 = "videos/0105CAM02.mp4"


class Player:
    def __init__(self):
        self.cap01 = cv2.VideoCapture(video_cam01)
        self.cap02 = cv2.VideoCapture(video_cam02)
        # with open("result_nomerge.json", 'r') as f:
        #     self.socker_data = json.load(f)
        self.socker_data = tracklets
        self.frame_count = 0
        self.bboxes01 = []
        self.bboxes02 = []

    def put_retangle(self, frame, bboxes, color, tracklet, player, cam):
        height, width, _ = frame.shape
        p1x = round(width * bboxes[0])
        p1y = round(height * bboxes[1])
        p2x = bboxes[0] + bboxes[2]
        p2x = round(p2x * width)
        p2y = bboxes[1] + bboxes[3]
        p2y = round(p2y * height)
        cv2.putText(frame, cam, (85, 0), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 1)
        cv2.putText(frame, str(self.frame_count), (0, 50), cv2.FONT_HERSHEY_COMPLEX, 2, (255, 0, 0), 1)
        cv2.rectangle(frame, (p1x, p1y), (p2x, p2y), color, 2, 1)
        cv2.putText(frame, str(tracklet), (p1x, p1y), 1, 1, (255, 255, 0), 1)
        cv2.putText(frame, str(player), (p1x, p2y), 1, 1, (255, 255, 0), 1)

    def run(self):
        while (self.cap01.isOpened() and self.cap02.isOpened()):
            self.frame_count += 1
            success1, frame1 = self.cap01.read()
            success2, frame2 = self.cap02.read()

            if not (success1 and success2):
                break

            frame1 = cv2.resize(frame1, (0, 0), fx=0.25, fy=0.25, interpolation=cv2.INTER_LINEAR)
            frame2 = cv2.resize(frame2, (0, 0), fx=0.75, fy=0.75, interpolation=cv2.INTER_LINEAR)
            for tracklet in self.socker_data:
                print(self.socker_data[tracklet]['tracklet_id'])
                for frame in self.socker_data[tracklet]['trails']:
                    if self.frame_count == frame['frame_lable'] and 'cam01' in frame.keys():
                        # self.bboxes01 = frame['cam01']['body']['pos']
                        self.put_retangle(frame1, frame['cam01']['body']['pos'], (0, 0, 255), self.socker_data[tracklet]['tracklet_id'], self.socker_data[tracklet]['player_id'], cam='cam01')
                        print("cam01 ", "frame:", self.frame_count, "tracklet:", tracklet)
                        break
                    if self.frame_count == frame['frame_lable'] and 'cam02' in frame.keys():
                        # self.bboxes02 = frame['cam02']['body']['pos']
                        self.put_retangle(frame2, frame['cam02']['body']['pos'], (0, 0, 255), self.socker_data[tracklet]['tracklet_id'], self.socker_data[tracklet]['player_id'], cam='cam02')
                        print("cam02 ", "frame:", self.frame_count, "tracklet:", tracklet)
                        break
            cv2.imshow('WINDOW1', frame1)
            cv2.imshow('WINDOW2', frame2)
            if cv2.waitKey(0) & 0xFF == 27:  # Esc pressed
                break


if __name__ == '__main__':
    player = Player()
    player.run()
