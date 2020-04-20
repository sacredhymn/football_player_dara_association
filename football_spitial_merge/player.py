import cv2
import json
from optimize_json import tracklets
from football_field import football_filed

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


class filed_player:
    def __init__(self, tracklets, football_filed, get_details):
        self.cap01 = cv2.VideoCapture(video_cam01)
        self.cap02 = cv2.VideoCapture(video_cam02)
        self.frame_count = 0
        self.tracklets = tracklets
        self.football_filed = football_filed
        self.get_details = get_details

    def put_circle(self, football_filed, frame, center, tracklet_id, cam):
        color = (255, 0, 0)
        if cam == "cam02":
            color = (0, 0, 255)
        cv2.putText(football_filed, str(frame), (0,85), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 1)
        cv2.circle(football_filed, center, radius=3, color=color, thickness=-1)
        cv2.putText(football_filed, str(tracklet_id), center, 1, 1, (125, 125, 125), 1)

    def run(self):
        scale, pitch_pad_w, pitch_pad_h, width, height = self.get_details()
        while (self.cap01.isOpened() and self.cap02.isOpened()):
            self.frame_count += 1
            football_filed = self.football_filed.copy()
            success1, frame1 = self.cap01.read()
            success2, frame2 = self.cap02.read()

            if not (success1 and success2):
                break

            for tracklet in self.tracklets:
                for frame in self.tracklets[tracklet]['trails']:
                    if self.frame_count == frame['frame_lable'] and 'cam01' in frame.keys():
                        self.put_circle(football_filed, self.frame_count, (int(frame['pitch']['x']*width*scale), int(frame['pitch']['y']*height*scale)),
                                                           self.tracklets[tracklet]['tracklet_id'], "cam01")
                        break
                    if self.frame_count == frame['frame_lable'] and 'cam02' in frame.keys():
                        self.put_circle(football_filed, self.frame_count, (int(frame['pitch']['x']*width*scale), int(frame['pitch']['y']*height*scale)),
                                                           self.tracklets[tracklet]['tracklet_id'], "cam02")
                        break
            cv2.imshow('WINDOW', football_filed)
            if cv2.waitKey(0) & 0xFF == 27:  # Esc pressed
                break


if __name__ == '__main__':
    # player = Player()
    # player.run()
    filed =football_filed()
    football_filled_image = filed.get_football_filed()
    filed_player = filed_player(tracklets, football_filled_image, filed.get_football_details)
    filed_player.run()
    #
