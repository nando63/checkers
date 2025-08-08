import subprocess
import os
from checker import *
import time
from copy import deepcopy
from random import choice,random
import numpy
from keras.models import Sequential
from keras.layers import Dense
from keras.models import load_model

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

model = create_model()

if not os.path.isfile('my_model.h5'):
    print("No model found. Generating data and training a new model...")
    X_train = []
    y_train = []

    GAMES_TO_PLAY = 500
    print(f"Playing {GAMES_TO_PLAY} games to generate data...")

    for i in range(GAMES_TO_PLAY):
        board = chessboard(model)
        history = []

        while True:
            moves = board.getAllMoves()
            if len(moves) == 0:
                winner = 'b' if board.player == 'w' else 'w'
                for h_board, h_player in history:
                    if winner == h_player:
                        y_train.append(1) # Win
                    else:
                        y_train.append(0) # Loss
                    X_train.append(changeBoard(h_board))
                break

            move = board.bestMove()
            history.append((deepcopy(board.board), board.player))
            board.doMove(move)

        print("Game %d/%d complete" % (i+1, GAMES_TO_PLAY))

    print("Data generation complete.")
    print("Generated %d training samples." % len(X_train))

    X_train = numpy.array(X_train)
    y_train = numpy.array(y_train)

    X_train = X_train.squeeze()

    model.fit(X_train, y_train, epochs=100, batch_size=128)

    model.save('my_model.h5')
    print("Model trained and saved as my_model.h5")


# Test the AI
print("\n\n--- Starting test match: Keras AI (w) vs Minimax AI (b) ---")
board = chessboard(model)
board.show()

while True:
    moves = board.getAllMoves()
    if len(moves) == 0:
        winner = 'b' if board.player == 'w' else 'w'
        print("Game over! Winner is: " + winner)
        break

    if board.player == 'w':
        print("Keras AI's turn (w)")
        move = board.bestMoveKeras()
    else:
        print("Minimax AI's turn (b)")
        move = board.bestMove()

    board.doMove(move)
    board.show()
    time.sleep(1)
