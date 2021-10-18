import numpy as np
import cv2
from face_detection import detect_faces
from face_recog import Recognizer
from face_spoofing import spoof_detector
from face_land import detect_landmarks
from head_pose import headpose_est
from detect_open_mouth import main_open_mouth
# from eye_tracker import eye_tracking
# from detect_open_mouth import main_open_mouth
import utils

font = cv2.FONT_HERSHEY_SIMPLEX 
pTime = [0]

# count variables
mouth_cheat_count = [0]
head_cheat_count = [0]
facedet_cheat_count = [0]
facerec_cheat_count = [0]
spoof_cheat_count = [0]
# eye_cheat_count = [0]

# thresholds
mouth_cheat_threshold = 60
head_cheat_threshold = 30
facedet_cheat_threshold = 30
facerec_cheat_threshold = 30
spoof_cheat_threshold = 30
# eye_cheat_threshold = 30

segment_time = 20
fps_assumed = 5

#frame
frame_count = [0]
cheat_frame_count = [0]

#segment
segment_count=0
cheat_segment_count=0

# Face recognizer
fr = Recognizer(threshold = 0.8)

# Register User
fr.input_embeddings = utils.register_user(fr, num_pics = 5, skipr = False)

if __name__ == "__main__":
    cap = cv2.VideoCapture(0)
    cv2.namedWindow('PROCTORING ON')

    while(True):
        frame_count[0] = (frame_count[0]+1)%(segment_time*fps_assumed)
        ret, frame = cap.read()
        frame = utils.print_fps(cv2.flip(frame, 1), pTime)
        
        faces =  detect_faces(frame, confidence = 0.7)
        if faces:
            fr.verify_faces(faces)
            spoof_detector(faces)
            if len(faces)==1:
                hland = detect_landmarks(frame, faces) 
                if faces[0].landmarks:
                    faces[0].head = headpose_est(frame, faces, hland)
                    # eye_tracking(frame, faces[0].shape, threshold = 75)
                    faces[0].mouth = main_open_mouth(frame, faces)

            frame = utils.print_faces(frame, faces, mouth_cheat_count, head_cheat_count, facerec_cheat_count, spoof_cheat_count, cheat_frame_count)
        else :
            cv2.putText(frame, "CHEATING",(30, 150), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,255), 2)
            facedet_cheat_count[0]+=1
            cheat_frame_count[0]+=1
            
            
        if (frame_count[0])%(segment_time*fps_assumed)==0:
            segment_count+=1
            if((mouth_cheat_count[0]>=mouth_cheat_threshold) or (head_cheat_count[0]>=head_cheat_threshold) or (facedet_cheat_count[0]>=facedet_cheat_threshold) or (facerec_cheat_count[0]>=facerec_cheat_threshold) or (spoof_cheat_count[0]>=spoof_cheat_threshold)):
                cheat_segment_count+=1
            mouth_cheat_count[0] = 0
            head_cheat_count[0] = 0
            facedet_cheat_count[0] = 0
            facerec_cheat_count[0] = 0
            spoof_cheat_count[0] = 0
            # eye_cheat_count[0] = 0
            
        cv2.imshow('PROCTORING ON',  frame)
                
        if cv2.waitKey(1) & 0xFF == 27: 
            break
    cap.release()
    cv2.destroyAllWindows()
    
print(" ")
print("segment_count = ", segment_count)
print(" ")
print("cheat_segment_count = ", cheat_segment_count)


#    DO NOT DELETE THIS!
# C:\Users\Anirudh\mini_project_iiita\eye_tracker.py:39: RuntimeWarning: divide by zero encountered in long_scalars
#   y_ratio = (cy - end_points[1])/(end_points[3] - cy)

# Rough:
        # outputs: detreg_out, landeye_out, head_out
#         head_out = cv2.copyMakeBorder(head_out, 0, 0, 320, 320, cv2.BORDER_CONSTANT, (0,0,0))
#         horiz = np.concatenate((horiz, head_out), axis = 1)