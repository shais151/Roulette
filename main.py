import random

class Outcome:
	"""
	Each number has a variety of outcomes i.e. ("Red" 1:1)
	Test: test = Outcome("test",5), then test.winAmount(5) = 25
	Chapter5, pages 37-43
	"""
	def __init__(self, name:str, odds:int):
		self.name:str = str(name)
		self.odds:int = int(odds)

	def winAmount(self, amount:float) -> float:
		return self.odds * amount

	def __eq__(self, other) -> bool:
		return self.name == other.name

	def __ne__(self, other) -> bool:
		return not self.name == other.name

	def __hash__(self) -> int:
		return hash(self.name)

	def __str__(self) -> str:
		return f"{self.name} ({self.odds}:1)"
	
	def __repr__(self) -> str:
		return f"{self.__class__.__name__}({self.name}, {self.odds})"

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
		self.bins:tuple = tuple(Bin() for _ in range(38))
		self.rng = random.Random()
		self.rng.seed(4)
		self.all_outcomes:set = set()
		bb = BinBuilder()                   
		bb.buildBins(self)  

	def addOutcome(self, number, outcome):
		self.all_outcomes.add(outcome)
		self.bins[number] = Bin(self.bins[number] | Bin([outcome]))

	def next(self):
		return self.bins[self.rng.randint(0,37)]

	def get(self, bin) -> Bin:
		return self.bins[bin]

	def getOutcome(self, outcomeName):
		for outcome in self.all_outcomes:
			if outcome.name == outcomeName:
				return outcome

class BinBuilder:
	"""
	Creates all of the winning Outcomes and adds them to each bin on the wheel
	Each bin has 12-14 different ways that it can be a winner e.g. 1 can be straight, street, corner...
	Chapter 8, pages 53-58
	"""
	def buildBins(self, wheel):
		outcomes = self.straightBets() + self.splitBets() + self.streetBets() + self.cornerBets()
		outcomes += self.lineBets() + self.dozenBets() + self.outsideBets()

		for outcome in outcomes:
			wheel.addOutcome(outcome[0], outcome[1])

	def straightBets(self) -> list:
		"""
		Bet on a single number paying at 35:1
		38 bets / 38 outcomes
		""" 
		outcomes:list = []
		for n in range(0,37):
			outcomes.append((n, Outcome(str(n), 35)))
		outcomes.append((37, Outcome("00", 35)))
		return outcomes
  
	def splitBets(self) -> list:
		"""
		Adjacent pair of numbers (column or row) paying at 17:1
		114 bets / 114 outcomes
		"""
		outcomes:list = []
		plusone = list(range(1,35,3)) + list(range(2,36,3))
		plusthree = list(range(1,34))
		for i in plusone:
			string = f"Split {str(i)}-{str(i+1)}"
			outcomes.append((i, Outcome(string,17)))
			outcomes.append((i+1, Outcome(string,17)))
		for i in plusthree:
			string = f"Split {str(i)}-{str(i+3)}"
			outcomes.append((i, Outcome(string,17)))
			outcomes.append((i+3, Outcome(string,17)))
		return outcomes
  
	def streetBets(self) -> list:
		"""
		3 numbers in a single row paying at 11:1
		12 possible bets / 36 outcomes
		"""
		outcomes:list = []
		for r in range(0,12):
			n = 3*r+1
			street = [n, n+1,n+2]
			for i in range(0,3):
				outcomes.append((street[i], Outcome(f"Street {street[0]}-{street[1]}-{street[2]}", 11)))
		return outcomes

	def lineBets(self) -> list:
		"""
		A 6 number block (2 street bets) paying at 5:1
		11 possible bets
		"""
		outcomes:list = []
		return outcomes

	def dozenBets(self) -> list:
		"""
		Each number is member of one of three dozens paying at 2:1
		3 possible bets
		"""
		outcomes:list = []
		for d in range(0, 3): #TODO
			for m in range(0, 12):
				break
		return outcomes
	
	def cornerBets(self) -> list:
		"""
		A square of 4 numbers paying at 8:1
		22 possible bets / 88 outcomes
		"""
		outcomes:list = []
		return outcomes

	def outsideBets(self) -> list:
		"""
		All other bets e.g. Red/Black, Low/High, Even/Odd
		"""
		outcomes:list = []
		return outcomes

class Bet:
	def __init__(self, amount: int, outcome):
		self.amountBet:int = int(amount)
		self.outcome = outcome
	
	def winAmount(self) -> int:
		return self.outcome.winAmount(self.amount) + self.amount
	
	def loseAmount(self) -> int:
		return self.amountBet

	def __str__(self) -> str:
		return f"{self.amountBet} on {self.outcome}"

	def __repr__(self) -> str:
		return f"{self.__class__.__name__}({self.amountBet}, {self.outcome})"

class Table:
	"""
	A table is where bets can be placed
	Chapter 10, pages 63-68
	"""
	def __init__(self, limit, minimum, wheel):
		pass

	def placeBet(self, bet):
		pass

	def __iter__(self) -> iter:
		return self.bets[:].__iter__()
	
	def __str__(self) -> str:
		pass

	def __repr__(self) -> str:
		pass
	
	def isValid(self, bet):
		pass

	def clearBets(self):
		self.bets.clear()

class Invalidbet(Exception):
	def __init__(self, expression):
		self.expression = expression