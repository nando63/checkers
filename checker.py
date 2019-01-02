# Enter your code here. Read input from STDIN. Print output to STDOUT
from random import choice
from copy import deepcopy
import sys

try:
	raw_input
except:
	raw_input = input

def getOpposite(pawn):
	if pawn == 'w' or pawn == 'W':
		return ['b','B']
	return ['w','W']

def getJumps(r,c,board):
	dir = {
		'b':[(1,-1),(1,1)],
		'B':[(1,-1),(1,1),(-1,-1),(-1,1)],
		'w':[(-1,-1),(-1,1)],
		'W':[(1,-1),(1,1),(-1,-1),(-1,1)],
	}
	b = deepcopy(board)
	p = board.board[r][c]
	opposite = getOpposite(p)
	jumps = []
	for d in dir[p]:
		newr = r + d[0]
		newc = c + d[1]
		if newr >= 0 and newr < b.size_board:
			if newc >= 0 and newc < b.size_board:
				if b.board[newr][newc] in opposite:
					newrr = newr + d[0]
					newcc = newc + d[1]
					if newrr >= 0 and newrr < b.size_board:
						if newcc >= 0 and newcc < b.size_board:
							if b.board[newrr][newcc] == "_":
								b.board[r][c] = '_'
								otmp = b.board[newr][newc]
								b.board[newr][newc] = '_'
								newp = p
								if p == 'w' and newrr == 0:
									newp = 'W'
								elif p == 'b' and newrr == b.size_board-1:
									newp = 'B'
								b.board[newrr][newcc] = newp
								arrJump = getJumps(newrr,newcc,b)
								if len(arrJump) > 0:
									for jump in arrJump:
										jumps.append([r,c,newrr,newcc,]+jump[2:])
								else:
									jumps.append([r,c,newrr,newcc])
								b.board[r][c] = p
								b.board[newr][newc] = otmp
								b.board[newrr][newcc] = '_'
	return jumps

def getMoves(r,c,board):
	dir = {
		'b':[(1,-1),(1,1)],
		'B':[(1,-1),(1,1),(-1,-1),(-1,1)],
		'w':[(-1,-1),(-1,1)],
		'W':[(1,-1),(1,1),(-1,-1),(-1,1)],
	}
	moves = []
	p = board.board[r][c]
	for d in dir[p]:
		newr = r + d[0]
		newc = c + d[1]
		if newr >= 0 and newr < board.size_board:
			if newc >= 0 and newc < board.size_board:
				if board.board[newr][newc] == "_":
					moves.append((r,c,newr,newc))
	return moves

def nextMoves(board):
	pawns = [board.player,board.player.upper()]
	size_board = board.size_board
	
	moves = []
	for r in range(size_board):
		for c in range(1-r%2,size_board,2):
			if board.board[r][c] in pawns:
				j = getJumps(r,c,board)
				if len(j) > 0:
					moves += j
	if len(moves) == 0:
		for r in range(size_board):
			for c in range(1-r%2,size_board,2):
				if board.board[r][c] in pawns:
					m = getMoves(r,c,board)
					if len(m) > 0:
						moves += m
	return moves

def getValue(board):
	value = 0
	valori = {'_':0, 'w':10, 'W':50, 'b':-10, 'B':-50}
	pawn = getOpposite(board.player)
	for r in range(board.size_board):
		for c in range(1-r%2,board.size_board,2):
			value += valori.get(board.board[r][c],0)
	if board.player == 'w':
		return value
	return -value

def bestMove(moves,board):
	value = -9999
	bestMoves = []
	for move in moves:
		b = deepcopy(board)
		doMove(move,b)
		newValue = getValue(b)
		if (newValue > value):
			value = newValue
			bestMoves = [move]
		elif newValue == value:
			bestMoves.append(move)
	return choice(bestMoves)
	
def doMove(move,board):
	for i in range(0,len(move)-2,2):
		pawn = board.board[move[i]][move[i+1]]
		board.board[move[i]][move[i+1]] = "_"
		if pawn == 'w' and move[i+2] == 0:
			pawn = "W"
		elif pawn == 'b' and move[i+2] == board.size_board-1:
			pawn = "B"
		board.board[move[i+2]][move[i+3]] = pawn
		if abs(move[i] - move[i+2]) > 1:
			r = (move[i] + move[i+2]) // 2
			c = (move[i+1] + move[i+3]) // 2
			board.board[r][c] = "_"
	board.player = "b" if board.player == "w" else "w"
	
class chessboard:
	def __init__(self):
		self.player = 'w'
		self.size_board = 8
		self.board = [
			['_', 'b', '_', 'b', '_', 'b', '_', 'b'],
			['b', '_', 'b', '_', 'b', '_', 'b', '_'],
			['_', 'b', '_', 'b', '_', 'b', '_', 'b'],
			['_', '_', '_', '_', '_', '_', '_', '_'],
			['_', '_', '_', '_', '_', '_', '_', '_'],
			['w', '_', 'w', '_', 'w', '_', 'w', '_'],
			['_', 'w', '_', 'w', '_', 'w', '_', 'w'],
			['w', '_', 'w', '_', 'w', '_', 'w', '_']
		]
	
if __name__ == "__main__":
	board = chessboard()
	board.player = raw_input()
	board.size_board = int(raw_input().strip())
	board.board = []
	for _ in range(board.size_board):
		board.board.append(list(raw_input().strip()))
	moves = nextMoves(board)
	if len(moves) > 0:
		move = bestMove(moves,board)
		print ((len(move) // 2) - 1)
		for i in range(0,len(move),2):
			print ("%d %d" % (move[i],move[i+1]))