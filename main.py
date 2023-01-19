import random

class Outcome:
	"""
	Each number has a variety of outcomes i.e. ("Red" 1:1)
	Test: test = Outcome("test",5), then test.winAmount(5) = 25
	Chapter5, pages 37-43
	"""
	def __init__(self, name:str, odds:int):
		self.name = str(name)
		self.odds = int(odds)

	def winAmount(self, amount:float) -> float:
		return self.odds * amount

	def __eq__(self, other) -> bool:
		return self.name == other.name

	def __ne__(self, other) -> bool:
		return not self.name == other.name

	def __hash__(self) -> int:
		return hash(self.name)

	def __str__(self) -> str:
		return "{name:s} ({odds:d}:1)".format_map(vars(self))
	
	def __repr__(self) -> str:
		return "{class_:s}({name!r}, {odds!r})".format(
			class_=type(self).__name__, **vars(self)
		)

class Bin(frozenset):
	"""
	Each bin will have 12-14 Outcomes
	Frozenset means a unique values, fixed once created
	Extended (inherits all methods from frozenset e.g. .add())
	Chapter 6, pages 45-48
	"""
	pass

class Wheel:
	"""
	Contains 38 bins
	Responsible for Random Number Generation (RNG)
	Chapter 7, pages 49-52
	"""
	def __init__(self):
		self.bins = tuple(Bin() for _ in range(38))
		self.rng = random.Random()
		self.rng.seed(4)

	def addOutcome(self, number, outcome):
		self.bins[number] = Bin(self.bins[number] | Bin([outcome]))

	def next(self):
		return self.rng.randint(0, 37) #TODO

	def get(self, bin) -> Bin:
		return self.bins[bin]