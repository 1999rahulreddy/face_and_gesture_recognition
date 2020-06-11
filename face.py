import face_recognition
import os
import cv2
import numpy as np
import sys
import pickle as p
#import tensorflow as tf

KNOWN_FACES_DIR = 'known_faces'
train=0

##original face
##UNKNOWN_FACES_DIR = 'unknown_faces'

##new face
try:
	UNKNOWN_FACES_DIR = f'{sys.argv[1]}'
	train=int(sys.argv[2])
	print(UNKNOWN_FACES_DIR,train)
except :
	print("run again")
	UNKNOWN_FACES_DIR='unknown_faces'
	sys.exit()

TRAINED_FACE_ENCODINGS='Trained_face_encodings.pkl'
TRAINED_FACE_NAMES='Trained_face_names.pkl'


if not (os.path.isfile(TRAINED_FACE_ENCODINGS) and os.path.isfile(TRAINED_FACE_NAMES)) :
	print("files missing so training again")
	train=1
else:
	print("didnt do")

TOLERENCE = 0.5  ## higher this no more the cases of false negative tolerence
FRAME_THICKNESS = 3
FONT_THICKNESS = 2
MODEL = "hog"


def name_to_color(name):
    color = [(ord(c.lower())-97)*8 for c in name[:3]]
    return color

print("loading known faces")



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


#print(known_faces)
print("processing unknown faces")
#print("known faces",known_faces)



###original unknown faces
if(os.path.isdir(UNKNOWN_FACES_DIR)):
	for filename in os.listdir(UNKNOWN_FACES_DIR):
		#with tf.device('/device:GPU:0'):
		print("filename",filename,end='')
		image = face_recognition.load_image_file(f"{UNKNOWN_FACES_DIR}/{filename}")
		locations = face_recognition.face_locations(image, model=MODEL)
		encodings = face_recognition.face_encodings(image, locations)
		image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
		print(f', found {len(encodings)} face(s)')

		for face_encoding, face_location in zip(encodings, locations):
			results = face_recognition.compare_faces(known_faces, face_encoding, TOLERENCE)
			match = None
			####print(type(results),results)

			if True in results:
				match = known_names[results.index(True)]
				print(f' - {match} identified from {filename}')

				top_left = (face_location[3], face_location[0])
				bottom_right = (face_location[1], face_location[2])

				color = name_to_color(match)

				cv2.rectangle(image, top_left, bottom_right, color, FRAME_THICKNESS)
				###cv2.rectangle(image, top_left, bottom_right, color, cv2.FILLED)

				top_left = (face_location[3], face_location[2])
				bottom_right = (face_location[1], face_location[2]+22)

				cv2.rectangle(image, top_left, bottom_right, color, cv2.FILLED)
				cv2.putText(image, match, (face_location[3], face_location[2]+15), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (200, 200, 200), FONT_THICKNESS)

		cv2.namedWindow(filename,cv2.WINDOW_NORMAL)
		cv2.resizeWindow(filename, 600,600)
		cv2.imshow(filename, image)
		cv2.waitKey(5000)

elif(os.path.isfile(UNKNOWN_FACES_DIR)):
	####new modified face
	image = face_recognition.load_image_file(f"{UNKNOWN_FACES_DIR}")
	locations = face_recognition.face_locations(image, model=MODEL)
	encodings = face_recognition.face_encodings(image, locations)
	image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
	print(f', found {len(encodings)} face(s)')

	for face_encoding, face_location in zip(encodings, locations):
		results = face_recognition.compare_faces(known_faces, face_encoding, TOLERENCE)
		match = None
		####print(type(results),results)

		if True in results:
			match = known_names[results.index(True)]
			print(f' - {match} identified from {UNKNOWN_FACES_DIR}')

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
	cv2.imshow('filename', image)
	cv2.waitKey(5000)
	
else:
	sys.exit()