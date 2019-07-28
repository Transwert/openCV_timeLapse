### you can experiment with creating other resolution videos,
### as it might help in checking whether all combinations are working or not

import time
import datetime
from utils import CFEVideoConf, image_resize
import glob
import cv2
import os
import glob

# system_constants
cap = cv2.VideoCapture(0)
save_path = 'saved-media/timelapse.mp4'
frames_per_seconds = 24.0
config = CFEVideoConf(cap, filepath=save_path, res='480p')
out = cv2.VideoWriter(save_path, config.video_type,frames_per_seconds, config.dims)
seconds_duration = 24
timelapse_img_dir = "images/timelapse/"
seconds_between_shots = 1

# utility  for, if directory which being stated, doesn't exist, then it creates it
if not os.path.exists(timelapse_img_dir):
    os.mkdir(timelapse_img_dir)

now = datetime.datetime.now()
finish_time = now + datetime.timedelta(seconds=seconds_duration)

i = 0  # used for iteration for name

while datetime.datetime.now() < finish_time:
    # capture frame-by-frame
    ret, frame = cap.read()
    filename = timelapse_img_dir + "/" + str(i) + ".jpg"
    i += 1
    cv2.imwrite(filename, frame)
    # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # out.write(frame)
    # Display the resulting frame
    # cv2.imshow('frame', frame)
    time.sleep(seconds_between_shots)
    if cv2.waitKey(20) & 0xFF == ord('q'):
            break


#below process for adding all the captured images into one single timelapse video
images_list = glob.glob(timelapse_img_dir+"/"+"*.jpg")
sorted_images = sorted(images_list, key= os.path.getmtime)
for file in sorted_images:
	print(file)
	image_frame = cv2.imread(file)
	out.write(image_frame)

clear_images = False
# utility function, used if wanted to remove the images after processing for video
if clear_images:
	for file in images_list:
		os.remove(file)

# when everything done, release the capture
cap.release()
out.release()
cv2.destroyAllWindows()
