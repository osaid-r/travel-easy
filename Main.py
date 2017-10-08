# import the necessary packages
from __future__ import print_function
from imutils.object_detection import non_max_suppression
from imutils import paths
import numpy as np
import argparse
import imutils
import cv2
import time
from operator import eq
from flask import Flask, request, render_template, redirect, session, flash
from flask_mysqldb import MySQL
import MySQLdb

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'temp'
app.config['MYSQL_PASSWORD'] = 'temporary'
app.config['MYSQL_DB'] = 'counter'
mysql = MySQL(app)

@app.route('/index', methods=['GET'])
@app.route('/', methods=['GET'])
def index():
	# initialize the HOG descriptor/person detector
	hog = cv2.HOGDescriptor()
	hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())

	cap = cv2.VideoCapture(0)
	prev = time.time()
	people = 0
	centres = []
	speed = 0

	people += 1
	ret, frame = cap.read()

	# image = cv2.imread(imagePath)
	image = imutils.resize(frame, width=min(400, frame.shape[1]))
	orig = image.copy()

	# detect people in the image
	(rects, weights) = hog.detectMultiScale(image, winStride=(4, 4), padding=(8, 8), scale=1.05)

	# draw the original bounding boxes
	for (x, y, w, h) in rects:
		cv2.rectangle(orig, (x, y), (x + w, y + h), (0, 0, 255), 2)

	# apply non-maxima suppression to the bounding boxes using a
	# fairly large overlap threshold to try to maintain overlapping
	# boxes that are still people
	rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
	pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)

	for (xA, yA, xB, yB) in pick:
		cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)
		centres.append(((xA+xB)/2,  (yA+yB)/2))

	try:

		while 1:
			epochs = 1
			people += 1
			ret, frame = cap.read()

			# image = cv2.imread(imagePath)
			image = imutils.resize(frame, width=min(400, frame.shape[1]))
			orig = image.copy()

			# detect people in the image
			(rects, weights) = hog.detectMultiScale(image, winStride=(4, 4), padding=(8, 8), scale=1.05)

			# draw the original bounding boxes
			for (x, y, w, h) in rects:
				cv2.rectangle(orig, (x, y), (x + w, y + h), (0, 0, 255), 2)

			# apply non-maxima suppression to the bounding boxes using a
			# fairly large overlap threshold to try to maintain overlapping
			# boxes that are still people
			rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
			pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)

			temp = []
			# draw the final bounding boxes
			for (xA, yA, xB, yB) in pick:
				cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)
				temp.append(((xA+xB)/2,  (yA+yB)/2))


			for i in range(min(len(centres), len(temp))):
				# print('here')
				if temp[i][0]!=centres[i][0] or temp[i][1]!=centres[i][1]:
					pres = time.time()
					print(people, time.time()-prev)
					prev = pres
					speed = ((speed * (people-1)) + time.time()-prev)/people


			print(speed)
			avg += (speed/100)

			# show the output images
			cv2.imshow("After NMS", image)

			if cv2.waitKey(1) & 0xFF == ord('q'):
				break

			if epochs % 100 == 0:
				q = '''INSERT IGNORE INTO Counters (speed) VALUES("{0}")'''.format(avg)
				avg = 0

			epochs += 1

		cap.release()
		cv2.destroyAllWindows()

	except KeyboardInterrupt:
		print('closing...')
		cap.release()
		cv2.destroyAllWindows()


if __name__ == '__main__':
	app.secret_key = 'somerandomkey'
	app.run(debug=True)