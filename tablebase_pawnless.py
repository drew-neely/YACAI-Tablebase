from chess import *

from tablebase import BaseTablebase
from indexing import get_kings_index_np

class PawnlessTablebase(BaseTablebase) :

	def index(self, board) :
		queen_index = None
		king_index, square_index_mat = get_kings_index_np(board)
		pieces = [(sq, board.piece_at(sq)) for sq in SQUARES]
		pieces = [(sq, piece) for (sq, piece) in pieces if piece is not None and piece.piece_type != KING]
		assert len(pieces) == 1
		assert pieces[0][1].piece_type == QUEEN
		queen_index = square_index_mat[pieces[0][0]]
		q_sub = 0
		for color in [WHITE, BLACK] :
			if square_index_mat[board.king(color)] < queen_index :
				q_sub += 1
		queen_index -= q_sub
		assert queen_index < 62
		turn_index = 0 if board.turn == WHITE else 1
		index = turn_index * 462 * 62 + king_index * 62 + queen_index
		return index


	
	def build(self) :
		raise NotImplementedError("Tablebase.build()")

	# returns ([< white won positions >], [< black won positions >])
	def checkmate_positions(self) :
		raise NotImplementedError("Tablebase.checkmate_positions()")

	def set_dtm(self, index, winner, depth_to_mate) :
		raise NotImplementedError("Tablebase.set_dtm(board)")

	# returns (winner, dtm)
	def get_dtm(self, index) :
		raise NotImplementedError("Tablebase.get_dtm(board)")
