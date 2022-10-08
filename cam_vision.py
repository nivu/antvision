import pyrealsense2 as rs
import numpy as np
import cv2
 
# We want the points object to be persistent so we can display the 
#last cloud when a frame drops

#points = rs.points()
 
# Create a pipeline
pipeline = rs.pipeline()
#Create a config and configure the pipeline to stream
config = rs.config()

#cfg_left.enable_stream(rs.stream.infrared, 2, 1280, 720, rs.format.y8, 30)
#cfg_rgt.enable_stream(rs.stream.infrared, 1, 1280, 720, rs.format.y8, 30)

config.enable_stream(rs.stream.infrared, 1, 640, 480, rs.format.y8, 15)
config.enable_stream(rs.stream.infrared, 2, 640,480, rs.format.y8, 15)
config.enable_record_to_file('cam_vision.bag')

# Start streaming
profile = pipeline.start(config)

#pipeline_wrapper = rs.pipeline_wrapper(pipeline)
#pipeline_profile = config.resolve(pipeline_wrapper)


####################################################################################################################


# Streaming loop
try:
    while True:
        # Get frameset of color and depth
        frames = pipeline.wait_for_frames()

        ir1_frame_rgt = frames.get_infrared_frame(2) # Left IR Camera, it allows 1, 2 or no input

        ir1_frame_left = frames.get_infrared_frame(1)

        image_2 = np.asanyarray(ir1_frame_rgt.get_data())

        image_1 = np.asanyarray(ir1_frame_left.get_data())

        images = np.concatenate((image_1,image_2) , axis =1)
        image = np.concatenate((image_1,image_2) , axis =0)

        cv2.namedWindow('IR', cv2.WINDOW_AUTOSIZE)

        #cv2.namedWindow('IR Example Left', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('IR', images)
        #cv2.imshow('IR Example Right', image_2)
        key = cv2.waitKey(1)
        # Press esc or 'q' to close the image window
        if key & 0xFF == ord('q') or key == 27:
            cv2.destroyAllWindows()
            break
finally:
    pipeline.stop()
