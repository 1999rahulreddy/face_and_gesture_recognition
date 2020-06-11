import face_recognition
import os
import cv2
import pickle as p
import time
import sys
import imutils
from imutils.video import WebcamVideoStream



TRAINED_FACE_ENCODINGS='Trained_face_encodings.pkl'
TRAINED_FACE_NAMES='Trained_face_names.pkl'


KNOWN_FACES_DIR = 'known_faces'
###UNKNOWN_FACES_DIR = 'unknown_faces'

if sys.argv[1]=='-v':
    TOLERANCE = 0.4
else:
    TOLERANCE=0.5

FRAME_THICKNESS = 3
FONT_THICKNESS = 2
##MODEL = 'cnn'  # default: 'hog', other one can be 'cnn' - CUDA accelerated (if available) deep-learning pretrained model
MODEL="hog"
fps_time = 0    


'''
if len(sys.argv) == 2:
    if str(sys.argv[1])=='web':
        video = cv2.VideoCapture(0)
else:
    video=cv2.VideoCapture(0)
'''

#video=cv2.VideoCapture(0)
#video = WebcamVideoStream(src=0).start()
train=0

try:
    #UNKNOWN_FACES_DIR = f'{sys.argv[1]}'
    ck=sys.argv[1]
    if str(ck)=='-w':
        video = WebcamVideoStream(src=0).start()
        if len(sys.argv) > 2:
            train = int(sys.argv[2])
        else:
            train = 0
    elif str(ck)=='-v':
        video_loc = sys.argv[2]
        #video = cv2.VideoCapture(video_loc)
        video = WebcamVideoStream(src=video_loc).start()
        if len(sys.argv) > 3:
            train = int(sys.argv[3])
        else:
            train = 0

    print(train)
except :
    print(f'system arg  is  {sys.argv}')
    video=WebcamVideoStream(src=0).start()
    print("run again")
    #UNKNOWN_FACES_DIR='unknown_faces'




# Returns (R, G, B) from name
def name_to_color(name):
    # Take 3 first letters, tolower()
    # lowercased character ord() value rage is 97 to 122, substract 97, multiply by 8
    color = [(ord(c.lower())-97)*8 for c in name[:3]]
    return color



print('Loading known faces...')


known_faces = []
known_names = []
print(train)
if train:
    for name in os.listdir(KNOWN_FACES_DIR):
        for filename in os.listdir(f"{KNOWN_FACES_DIR}/{name}"):
            image = face_recognition.load_image_file(f"{KNOWN_FACES_DIR}/{name}/{filename}")
            encoding = face_recognition.face_encodings(image)
            if len(encoding)>0:
                known_faces.append(encoding[0])
                known_names.append(name)
                print(f'Filename {filename} --> found {len(encoding)} face(s)')
            else:
                print(f'Filename {filename} --> found {len(encoding)} face(s)')
    with open(f'{TRAINED_FACE_ENCODINGS}','wb') as f:
        p.dump(known_faces, f)
    with open(f'{TRAINED_FACE_NAMES}','wb') as f:
        p.dump(known_names, f)
else:
    known_faces = []
    with open(f'{TRAINED_FACE_ENCODINGS}','rb') as f:
        known_faces=p.load(f)
    with open(f'{TRAINED_FACE_NAMES}','rb') as f:
        known_names=p.load(f)




print('Processing unknown faces...')
# Now let's loop over a folder of faces we want to label
while True:

    # Load image
    ##ret, image = video.read()
    '''
    if ck == '-w':
        image = imutils.resize(video.read(),width=500)
    else:
        #ret, image = video.read()
        image = imutils.resize(video.read(),width=500)'''
    a=video.read()
    image = imutils.resize(a,width=400)

    # This time we first grab face locations - we'll need them to draw boxes
    locations = face_recognition.face_locations(image, model=MODEL)


    # Now since we know loctions, we can pass them to face_encodings as second argument
    # Without that it will search for faces once again slowing down whole process
    encodings = face_recognition.face_encodings(image, locations)
    ###print("\n printing encoding for -> ",filename,face_recognition.face_encodings(image)[0])

    # We passed our image through face_locations and face_encodings, so we can modify it
    # First we need to convert it from RGB to BGR as we are going to work with cv2
    #####image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    # But this time we assume that there might be more faces in an image - we can find faces of dirrerent people
    print(f', found {len(encodings)} face(s)')
    for face_encoding, face_location in zip(encodings, locations):

        # We use compare_faces (but might use face_distance as well)
        # Returns array of True/False values in order of passed known_faces

        results = face_recognition.compare_faces(known_faces, face_encoding, TOLERANCE)
        match = None

        # Since order is being preserved, we check if any face was found then grab index
        # then label (name) of first matching known face withing a tolerance
        if True in results:
            match = known_names[results.index(True)]
            print(f' - {match} identified ')

            top_left = (face_location[3], face_location[0])
            bottom_right = (face_location[1], face_location[2])

            color = name_to_color(match)

            cv2.rectangle(image, top_left, bottom_right, color, FRAME_THICKNESS)
            ###cv2.rectangle(image, top_left, bottom_right, color, cv2.FILLED)

            top_left = (face_location[3], face_location[2])
            bottom_right = (face_location[1], face_location[2]+22)

            cv2.rectangle(image, top_left, bottom_right, color, cv2.FILLED)
            cv2.putText(image, match, (face_location[3], face_location[2]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), FONT_THICKNESS)

    cv2.namedWindow('filename',cv2.WINDOW_NORMAL)
    cv2.resizeWindow('filename', 600,600)
    cv2.putText(image,
                    "FPS: %f" % (1.0 / (time.time() - fps_time)),
                    (10, 10),  cv2.FONT_HERSHEY_SIMPLEX, 0.5,
                    (0, 255, 0), 2)
    cv2.imshow('filename', image)
    fps_time = time.time()
    if cv2.waitKey(1) == 27:
        break