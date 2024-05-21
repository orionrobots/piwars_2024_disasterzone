from pyinfra import local
local.include("robot/services/camera_stream/install.py")
local.include("robot/services/launcher/install.py")
local.include("robot/services/line_following/install.py")
# local.include("robot/services/pimoroni_yukon/install.py")
local.include("robot/services/ps4_joypad/install.py")
