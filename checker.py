# Enter your code here. Read input from STDIN. Print output to STDOUT
from random import choice
from copy import deepcopy
import sys, os

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
		self.size_board = 8
		self.player = 'w'
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
		if False:
			self.player = 'b'
			self.board = [
				['_', '_', '_', '_', '_', '_', '_', '_'],
				['_', '_', '_', '_', '_', '_', 'W', '_'],
				['_', '_', '_', '_', '_', '_', '_', '_'],
				['_', '_', '_', '_', 'B', '_', '_', '_'],
				['_', '_', '_', '_', '_', '_', '_', '_'],
				['_', '_', '_', '_', '_', '_', '_', '_'],
				['_', '_', '_', '_', '_', '_', '_', '_'],
				['_', '_', '_', '_', '_', '_', '_', '_'],
			]
		self.pawn = {'w':0,'W':0,'b':0,'B':0}
		for r in range(self.size_board):
			for c in range(1-r%2, self.size_board,2):
				pawn = self.get(r,c)
				if pawn != '_':
					self.pawn[self.get(r,c)] += 1
	
	def getAllMoves(self):
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
	
	debug = False
	def bestMove(self):
		moves = self.getAllMoves()
		bestValue = -9999
		bestMoves = []
		
		if len(moves) > 1:
			for move in moves:
				b = deepcopy(self)
				b.doMove(move)
				newValue = b.minimax(4,-10000,10000,True)
				if self.player == 'b':
					newValue = -newValue
				if self.debug:
					b.printMove(move)
					print(newValue, end=" \n")
				if newValue > bestValue:
					bestValue = newValue
					bestMoves = [move]
				elif newValue == bestValue:
					bestMoves.append(move)
			if self.debug:
				print("premi invio")
				input()
		else:
			bestMoves = moves
		return choice(bestMoves)
	
	def minimax(self, depth, alpha, beta, isMaximising):
		moves = self.getAllMoves()
		if depth == 0 or len(moves) == 0:
			return self.getValue()
		if isMaximising:
			bestMove = -9999
			for move in moves:
				b = deepcopy(self)
				b.doMove(move)
				#self.show()
				#b.show(False)
				bestMove = max(bestMove,b.minimax(depth - 1,  alpha, beta, not isMaximising))
				#print (isMaximising,bestMove)
				#input()
				alpha = max(alpha, bestMove);
				if (beta <= alpha):
					return bestMove
		else:
			bestMove = 9999
			for move in moves:
				b = deepcopy(self)
				b.doMove(move)
				#self.show()
				#b.show(False)
				bestMove = min(bestMove,b.minimax(depth - 1,  alpha, beta, not isMaximising))
				#print (isMaximising,bestMove)
				#input()
				beta = min(beta, bestMove);
				if (beta <= alpha):
					return bestMove
		return bestMove

	OPENING = 19
	MIDDLE_GAME = 9
	MAN_VALUE = [ 100, 100, 100 ];
	KING_VALUE = [ 250, 250, 300 ];
	def getValue(self):
		n = self.contaPedine()
		if n >= self.OPENING:
			game_phase = 0
		elif n >= self.MIDDLE_GAME:
			game_phase = 1
		else:
			game_phase = 2
		value = (self.pawn['w'] - self.pawn['b']) * self.MAN_VALUE[game_phase] + (self.pawn['W'] - self.pawn['B']) * self.KING_VALUE[game_phase]
		return value

	def printMove(self,move):
		for i in range(0,len(move),2):
			print ("%d %d, " % (move[i],move[i+1]),end="")
	
	def doMove(self,move):
		for i in range(0,len(move)-2,2):
			pawn = self.get(move[i],move[i+1])
			self.set(move[i],move[i+1],"_")
			if pawn == 'w' and move[i+2] == 0:
				pawn = "W"
				self.pawn['w'] -= 1
				self.pawn['W'] += 1
			elif pawn == 'b' and move[i+2] == self.size_board-1:
				pawn = "B"
				self.pawn['b'] -= 1
				self.pawn['B'] += 1
			self.set(move[i+2],move[i+3],pawn)
			if abs(move[i] - move[i+2]) > 1:
				r = (move[i] + move[i+2]) // 2
				c = (move[i+1] + move[i+3]) // 2
				self.pawn[self.get(r,c)] -= 1
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

	def contaPedine(self):
		n = self.pawn['w'] + self.pawn['W'] + self.pawn['b'] + self.pawn['B']
		return n
	
	def show(self,clear=True):
		if clear:
			print ("\x1b[1;1H")
			os.system("cls")
		for r in range(len(self.board)):
			riga = self.board[r]
			print (r,end=" ")
			for c in range(len(riga)):
				print (riga[c],end="")
			print ("")
		print (self.pawn)

	
if __name__ == "__main__":
	board = chessboard()
	board.player = raw_input()
	board.size_board = int(raw_input().strip())
	board.board = []
	for _ in range(board.size_board):
		board.board.append(list(raw_input().strip()))
	moves = board.getAllMoves()
	if len(moves) > 0:
		move = board.bestMove()
		print ((len(move) // 2) - 1)
		for i in range(0,len(move),2):
			print ("%d %d" % (move[i],move[i+1]))