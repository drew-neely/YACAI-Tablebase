from chess import *
from itertools import combinations_with_replacement
from tablebase import NullTablebase

all_compositions = {}
piece_values = {'Q': 9, 'R': 5, 'N': 3, 'B': 3.1, 'P': 1, 'q': -9, 'r': -5, 'n': -3, 'b': -3.1, 'p': -1, 'K': 0, 'k' : 0}

endgame_classes = {
	'Kk'   : NullTablebase,
	'KBk'  : NullTablebase,
	'KNk'  : NullTablebase,
	'KBkn' : NullTablebase,
	# 'KQk'  : KQk
}

class Composition :
	
	# composition should not be initialized outside of get_composition
	def __init__(self, comp_str) :
		self.comp_str = ''.join(sorted(list(comp_str), key=lambda x: 'KQBNRPkqbnrp'.index(x)))
		# print(f"creating: {comp_str}")
		if self.comp_str in all_compositions :
			raise ValueError(f"Composition '{self.comp_str}' already exists")
		self.pieces = [Piece.from_symbol(char) for char in comp_str if char not in ['K', 'k']]
		self.prereqs = []
		for i, p in enumerate(self.pieces) :
			if p.piece_type == PAWN :
				for np in [QUEEN, ROOK, KNIGHT, BISHOP] :
					nps = self.pieces[:i] + [Piece(np, p.color)] + self.pieces[i+1:]
					nps_str = ''.join([p.symbol() for p in nps]) + 'Kk'
					self.prereqs.append(Composition.get_composition(nps_str))
			nps = self.pieces[:i] + self.pieces[i+1:]
			nps_str = ''.join([p.symbol() for p in nps]) + 'Kk'
			self.prereqs.append(Composition.get_composition(nps_str))


	# use this to make/get a new composition
	@staticmethod
	def get_composition(comp_str) :
		if len(comp_str) > 8 :
			raise ValueError("compositions with more than 8 pieces not supported due to complexity")
		wc = sum([c.isupper() for c in comp_str])
		bc = sum([c.islower() for c in comp_str])
		if wc < bc or (wc == bc and sum([piece_values[c] for c in comp_str]) < 0) : # flip colors
			comp_str = ''.join([c.upper() if c.islower() else c.lower() for c in comp_str])
		comp_str = ''.join(sorted(list(comp_str), key=lambda x: 'KQBNRPkqbnrp'.index(x)))
		if comp_str in all_compositions :
			return all_compositions[comp_str]
		else :
			comp = Composition(comp_str)
			all_compositions[comp_str] = comp
			return comp

	@staticmethod
	def get_all_compositions(men, pawns=True) :
		if men < 2 :
			raise ValueError("Invalid number of men in get_all_compositions")
		elif men == 2 :
			Composition.get_composition('Kk')
		else :
			pieces = ['Q', 'R', 'B', 'N', 'q', 'r', 'b', 'n']
			if pawns :
				pieces += ['P', 'p']
			combos = combinations_with_replacement(pieces, men - 2)
			for combo in combos :
				combo = 'Kk' + ''.join(combo)
				Composition.get_composition(combo)
		
		
			

if __name__ == '__main__' :

	Composition.get_all_compositions(6, pawns=False)
	print(len(all_compositions))
	# print(list(sorted(all_compositions.keys(), key = lambda x: len(x))))

	# endgames = ['KPPPPk', 'KPPPkp', 'KPPkpp']
	# try :
	# 	for e in endgames :
	# 		comp = Composition.get_composition(e)
	# 		print(len(all_compositions))
	# except Exception as e :
	# 	print("~~~~~~~~~~~~~~~~~~~~~~~~~~~")
	# 	print(e)
	# print(f"total number of prereqs = {len(all_compositions.keys())}")
	# print()
	# print(list(all_compositions.keys()))
	# print([c.comp_str for c in comp.prereqs])