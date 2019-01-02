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
	
	def nextMoves(self):
		pawns = [self.player,self.player.upper()]
		
		moves = []
		for r in range(self.size_board):
			for c in range(1-r%2,self.size_board,2):
				if self.get(r,c) in pawns:
					j = self.getJumps(r,c)
					if len(j) > 0:
						moves += j
		if len(moves) == 0:
			for r in range(self.size_board):
				for c in range(1-r%2,self.size_board,2):
					if self.get(r,c) in pawns:
						m = self.getMoves(r,c)
						if len(m) > 0:
							moves += m
		return moves
	
	def minimax(self, depth, isMaximising):
		if depth == 0:
			return -self.getValue()
		moves = self.nextMoves()
		if isMaximising:
			bestValue = -9999
			for i in range(len(moves)):
				move = moves[i]
				b = deepcopy(self)
				b.doMove(move)
				newValue = b.minimax(depth - 1,  not isMaximising)
				if newValue > bestValue:
					bestValue = newValue
			return bestValue
		else:
			bestValue = 9999
			for i in range(len(moves)):
				move = moves[i]
				b = deepcopy(self)
				b.doMove(move)
				newValue = b.minimax(depth - 1,  not isMaximising)
				if newValue < bestValue:
					bestValue = newValue
			return bestValue
	
	def bestMove(self):
		moves = self.nextMoves()
		bestValue = -9999
		bestMoves = []
		for move in moves:
			b = deepcopy(self)
			newValue = self.minimax(3,True)
			if self.player == 'w':
				newValue = -newValue
			if newValue > bestValue:
				bestValue = newValue
				bestMoves = [move]
			elif newValue == bestValue:
				bestMoves.append(move)
			self = b
		return choice(bestMoves)
	
	def doMove(self,move):
		for i in range(0,len(move)-2,2):
			pawn = self.get(move[i],move[i+1])
			self.set(move[i],move[i+1],"_")
			if pawn == 'w' and move[i+2] == 0:
				pawn = "W"
			elif pawn == 'b' and move[i+2] == self.size_board-1:
				pawn = "B"
			self.set(move[i+2],move[i+3],pawn)
			if abs(move[i] - move[i+2]) > 1:
				r = (move[i] + move[i+2]) // 2
				c = (move[i+1] + move[i+3]) // 2
				self.set(r,c,"_")
		self.player = "b" if self.player == "w" else "w"
	
	def set(self,r,c,value):
		self.board[r][c] = value

	def get(self,r,c):
		return self.board[r][c]
	
	def getJumps(self,r,c):
		dir = {
			'b':[(1,-1),(1,1)],
			'B':[(1,-1),(1,1),(-1,-1),(-1,1)],
			'w':[(-1,-1),(-1,1)],
			'W':[(1,-1),(1,1),(-1,-1),(-1,1)],
		}
		b = deepcopy(self)
		p = self.get(r,c)
		opposite = getOpposite(p)
		jumps = []
		for d in dir[p]:
			newr = r + d[0]
			newc = c + d[1]
			if newr >= 0 and newr < b.size_board:
				if newc >= 0 and newc < b.size_board:
					if b.get(newr,newc) in opposite:
						newrr = newr + d[0]
						newcc = newc + d[1]
						if newrr >= 0 and newrr < b.size_board:
							if newcc >= 0 and newcc < b.size_board:
								if b.get(newrr,newcc) == "_":
									b.set(r,c,'_')
									otmp = b.get(newr,newc)
									b.set(newr,newc,'_')
									newp = p
									if p == 'w' and newrr == 0:
										newp = 'W'
									elif p == 'b' and newrr == b.size_board-1:
										newp = 'B'
									b.set(newrr,newcc,newp)
									arrJump = b.getJumps(newrr,newcc)
									if len(arrJump) > 0:
										for jump in arrJump:
											jumps.append([r,c,newrr,newcc,]+jump[2:])
									else:
										jumps.append([r,c,newrr,newcc])
									b.set(r,c,p)
									b.set(newr,newc,otmp)
									b.set(newrr,newcc,'_')
		return jumps

	def getMoves(self,r,c):
		dir = {
			'b':[(1,-1),(1,1)],
			'B':[(1,-1),(1,1),(-1,-1),(-1,1)],
			'w':[(-1,-1),(-1,1)],
			'W':[(1,-1),(1,1),(-1,-1),(-1,1)],
		}
		moves = []
		p = self.get(r,c)
		for d in dir[p]:
			newr = r + d[0]
			newc = c + d[1]
			if newr >= 0 and newr < self.size_board:
				if newc >= 0 and newc < self.size_board:
					if self.get(newr,newc) == "_":
						moves.append((r,c,newr,newc))
		return moves

	def getValue(self):
		value = 0
		valori = {'_':0, 'w':10, 'W':50, 'b':-10, 'B':-50}
		for r in range(self.size_board):
			for c in range(1-r%2,self.size_board,2):
				value += valori.get(self.get(r,c),0)
		return value

	def show(self,clear=True):
		if clear:
			print ("\x1b[1;1H")
		for riga in self.board:
			for cell in riga:
				print (cell,end="")
			print ("")

	
if __name__ == "__main__":
	board = chessboard()
	board.player = raw_input()
	board.size_board = int(raw_input().strip())
	board.board = []
	for _ in range(board.size_board):
		board.board.append(list(raw_input().strip()))
	moves = board.nextMoves()
	if len(moves) > 0:
		move = board.bestMove()
		print ((len(move) // 2) - 1)
		for i in range(0,len(move),2):
			print ("%d %d" % (move[i],move[i+1]))