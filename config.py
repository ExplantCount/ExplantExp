from easydict import EasyDict as edict

config = edict()

config.CROP_DIMS = (100, 140, 500, 440)
config.GRIDW = 4
config.GRIDH = 3
config.colormap = [
0, 0, 0,
128, 64, 128,
80, 50, 50,
70, 70, 70,
102, 102, 156,
190, 153, 153,
153, 153, 153,
250, 170, 30,
220, 220, 0,
107, 142, 35,
152, 251, 152,
70, 130, 180,
230, 230, 230,
]