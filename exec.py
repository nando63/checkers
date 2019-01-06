import subprocess
import os
from checker import *
import time
from copy import deepcopy
from random import choice,random
#from keras.models import Sequential
#from keras.layers import Dense
#import numpy
#from keras.models import load_model

def create_model():
	if os.path.isfile('my_model.h5'):
		model = load_model('my_model.h5')
	else:
		# create model
		model = Sequential()

		model.add(Dense(32, input_dim=32, activation="relu", kernel_initializer="uniform"))
		model.add(Dense(100, kernel_initializer='uniform', activation='relu'))
		model.add(Dense(1, kernel_initializer='uniform', activation='sigmoid'))
		# Compile model
		model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])
	return model

def changeBoard(board):
	conv = {"w":0.25, "b":-0.25, "W":0.5, "B":-0.5, "_":0}
	b = []
	for r in range(8):
		for c in range(1-r%2,8,2):
			b.append(conv[board[r][c]])
	return numpy.array([b])

	
#model = create_model()

os.system("cls")
limit = 10000
for t in range(limit):
	board = chessboard()
	nmoves = 0
	while True:
		board.show()
		moves = board.getAllMoves()
		if len(moves) == 0:
			time.sleep(1)
			break
		nmoves += 1
		print ("Numero mosse = %d " % nmoves)
		move = board.bestMove()
		board.doMove(move)
		time.sleep(0.01)
