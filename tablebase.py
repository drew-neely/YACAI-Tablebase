from timer import Timer
from big_array import BigArray
import chess
import unmove_generator # add unmove functions to chess.Board

loaded_tables = {}

class BaseTablebase(BigArray) :

	def __init__(self, comp) :
		self.comp = comp
		if self.name in loaded_tables :
			raise ValueError(f"Tablebase '{comp.comp_str}' has already been loaded")
		super().__init__(comp.comp_str, 20000, 1) # !!! # These numbers are wrong
		# self.table = BigArray(self.name, self.len, self.bytes_per_entry)
		loaded_tables[self.name] = self

	def build(self) :
		raise NotImplementedError("Tablebase.build()")

	# returns ([< white won positions >], [< black won positions >])
	def checkmate_positions(self) :
		raise NotImplementedError("Tablebase.checkmate_positions()")

	def index(self, board) :
		raise NotImplementedError("Tablebase.index(board)")

	def set_dtm(self, index, winner, depth_to_mate) :
		raise NotImplementedError("Tablebase.set_dtm(board)")

	# returns (winner, dtm)
	def get_dtm(self, index) :
		raise NotImplementedError("Tablebase.get_dtm(board)")

	def __getitem__(self, index):
		if isinstance(index, chess.Board) :
			return super().__getitem__(self.index(index))
		elif isinstance(index, int) :
			return super().__getitem__(index)
		else :
			raise ValueError()

	def __setitem__(self, index, value):
		if isinstance(index, chess.Board) :
			super().__setitem__(self.index(index), value)
		elif isinstance(index, int) :
			super().__setitem__(index, value)
		else :
			raise ValueError()

class PawnTablebase(BaseTablebase) :
	pass

# class for drawn compositions
class NullTablebase(BaseTablebase) :
	def __init__(self, name) :
		self.name = name
		self.table = None

	def build(self) :
		raise NotImplementedError("NullTablebase.build()")

	def index(self, board) :
		return 0

	def get_dtm(self, index) :
		return (None, 0)

	@property
	def len(self) :
		return 0

	@property
	def bytes_per_entry(self) :
		return 0

	@property
	def writable(self) :
		return False

	def __getitem__(self, index):
		return 0

	def __setitem__(self, index, value):
		raise NotImplementedError("NullTablebase.__setitem__(index, value)")

	def flush(self) :
		raise NotImplementedError("NullTablebase.flush()")