import cv2
import numpy as np


class football_filed:
    def __init__(self):
        self.scale = 10
        self.pitch_pad_w = 10
        self.pitch_pad_h = 5
        self.width = 105
        self.height = 68
        self.zone_width = 16.5
        self.zone_height = 40.32
        self.circle_radius = 9.15

    def get_football_details(self):
        return self.scale, self.pitch_pad_w, self.pitch_pad_h, self.width, self.height

    def get_football_filed(self):
        # 外扩
        blank_image = np.ones(((self.height + self.pitch_pad_h*2)*self.scale, (self.width + self.pitch_pad_w*2)*self.scale, 3), np.float32)
        blank_image[:, :] = (0, 255, 0)

        # 球场
        blank_image[5*self.scale-2:73*self.scale+2, 10*self.scale-2:115*self.scale+2] = (255, 255, 255)
        blank_image[5*self.scale:73*self.scale, 10*self.scale:115*self.scale] = (0, 255, 0)

        # 禁区
        zone1_height_top = (self.height/2 + self.pitch_pad_h - self.zone_height/2)*self.scale
        zone1_height_down = (self.height/2 + self.pitch_pad_h + self.zone_height/2)*self.scale
        blank_image[int(zone1_height_top)-2:int(zone1_height_down)+2,
                    int(self.pitch_pad_w*self.scale)-2:int((self.zone_width + self.pitch_pad_w)*self.scale)+2] = (255, 255, 255)
        blank_image[int((self.height/2 + self.pitch_pad_h - self.zone_height/2)*self.scale):int((self.height/2 + self.pitch_pad_h + self.zone_height/2)*self.scale),
                    int(self.pitch_pad_w*self.scale):int((self.zone_width + self.pitch_pad_w)*self.scale)] = (0, 255, 0)

        zone2_height_top = (self.height/2 + self.pitch_pad_h - self.zone_height/2)*self.scale
        zone2_height_down = (self.height/2 + self.pitch_pad_h + self.zone_height/2)*self.scale
        blank_image[int(zone2_height_top)-2:int(zone2_height_down)+2,
                    int((self.pitch_pad_w + self.width - self.zone_width)*self.scale)-2:int((self.width + self.pitch_pad_w)*self.scale)+2] = (255, 255, 255)
        blank_image[int(zone2_height_top):int(zone2_height_down),
                    int((self.pitch_pad_w + self.width - self.zone_width)*self.scale):int((self.width + self.pitch_pad_w)*self.scale)] = (0, 255, 0)

        # 中间线
        blank_image[5*self.scale-2:73*self.scale+2, int(self.pitch_pad_w + self.width/2)*self.scale - 1:int(self.pitch_pad_w + self.width/2)*self.scale + 1] = (255, 255, 255)

        # 画圆
        center = (int(self.pitch_pad_w + self.width/2)*self.scale), int((self.pitch_pad_h + self.height/2)*self.scale)
        cv2.circle(blank_image, center, radius = int(self.circle_radius*self.scale), color=(255, 255, 255), thickness=1)
        return blank_image


if __name__ == "__main__":
    football_filed = football_filed()
    blank_image = football_filed.get_football_filed()
    cv2.imshow("result", blank_image)
    cv2.waitKey(0)
