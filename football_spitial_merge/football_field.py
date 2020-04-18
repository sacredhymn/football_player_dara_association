import matplotlib.pyplot as plt
import matplotlib.patches as mpathes
import numpy as np
import cv2

# 球场外扩pad
std_pitch_pad_w = 10
std_pitch_pad_h = 5

# 球场宽度、高度
std_pitch_width = 105
std_pitch_height = 68

# 标准禁区宽度、高度
std_zone_width = 16.5
std_zone_height = 40.32

# 中圈半径
std_circle_radius = 9.15

# 缩放比例
scale = 15

fig, ax = plt.subplots()

#长方形
rect = mpathes.Rectangle((0, 0), std_pitch_width + std_pitch_pad_w*2, std_pitch_height + std_pitch_pad_h*2)
rect2 = mpathes.Rectangle((std_pitch_pad_w, std_pitch_pad_h), std_pitch_width, std_pitch_height)
ax.add_patch(rect)
ax.add_patch(rect2)
plt.show()