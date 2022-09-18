import pyrealsense2 as rs
import numpy as np
import time


# find tilt angle for x,y,z axis in degree using accelerometer data
def find_tilt_angle(accel):
    x_angle = np.arctan2(accel[1], accel[2]) * 180 / np.pi
    y_angle = np.arctan2(accel[0], accel[2]) * 180 / np.pi
    z_angle = np.arctan2(accel[0], accel[1]) * 180 / np.pi
    return x_angle, y_angle, z_angle


def initialize_camera():
    # start the frames pipe
    p = rs.pipeline()
    conf = rs.config()
    conf.enable_stream(rs.stream.accel)
    conf.enable_stream(rs.stream.gyro)
    prof = p.start(conf)
    return p


def gyro_data(gyro):
    return np.asarray([gyro.x, gyro.y, gyro.z])


def accel_data(accel):
    return np.asarray([accel.x, accel.y, accel.z])

p = initialize_camera()
try:
    while True:
        f = p.wait_for_frames()
        accel = accel_data(f[0].as_motion_frame().get_motion_data())
        gyro = gyro_data(f[1].as_motion_frame().get_motion_data())
        print("accelerometer: ", accel)
        # print("gyro: ", gyro)
        # print("find_tilt_angle", find_tilt_angle(gyro))
        time.sleep(1)

finally:
    p.stop()