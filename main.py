import random
import math

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
		self.bins:list[Bin] = list(Bin() for _ in range(38))
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
			outcomes.append((i, Outcome(f"Split {str(i)}-{str(i+1)}",17)))
			outcomes.append((i+1, Outcome(f"Split {str(i)}-{str(i+1)}",17)))
		for i in plusthree:
			outcomes.append((i, Outcome(f"Split {str(i)}-{str(i+3)}",17)))
			outcomes.append((i+3, Outcome(f"Split {str(i)}-{str(i+3)}",17)))
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
		for i in range(1, 33, 3):
			for j in range(0, 6):
				outcomes.append((i + j, Outcome(f"Line {i}-{i+1}-{i+2}-{i+3}-{i+4}-{i+5}", 5)))
		return outcomes

	def dozenBets(self) -> list:
		"""
		Each number is member of one of three dozens paying at 2:1
		3 possible bets
		"""
		outcomes:list = []
		for i in [1, 13, 25]:
			for j in range(0, 12):
				outcomes.append((i + j, Outcome(f"Dozen {i}-{i+11}", 2)))
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
		reds = [1, 3, 5, 7, 9, 12, 14, 16, 18, 19, 21, 23, 25, 27, 30, 32, 34, 36]
		for i in range(1, 37):
			if i < 19:
				outcomes.append((i, Outcome("Low", 1)))
			else:
				outcomes.append((i, Outcome("High", 1)))
			if i % 2 == 0:
				outcomes.append((i, Outcome("Even", 1)))
			else:
				outcomes.append((i, Outcome("Odd", 1)))
			if i in reds:
				outcomes.append((i, Outcome("Red", 1)))
			else:
				outcomes.append((i, Outcome("Black", 1)))
		return outcomes

class Bet:
	def __init__(self, amount: int, outcome:Outcome):
		self.amountBet:int = int(amount)
		self.outcome = outcome
	
	def winAmount(self) -> float:
		return self.outcome.winAmount(self.amountBet) + self.amountBet
	
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
	def __init__(self, limit, wheel:Wheel):
		self.limit = limit
		self.bets:list[Bet] = []
		self.wheel = wheel

	def placeBet(self, bet:Bet):
		self.bets.append(bet)
		if not self.isValid(bet):
			raise InvalidBet(f"The bet of {bet.amountBet} exceeds table limit of {self.limit}")

	def __iter__(self):
		return self.bets[:].__iter__()
	
	def __str__(self) -> str:
		pass

	def __repr__(self) -> str:
		return f"{self.__class__.__name__}({self.limit}, {self.wheel})"
	
	def isValid(self, bet):
		if sum(obj.amountBet for obj in self.bets) > self.limit:
			return False
		return True

	def clearBets(self):
		self.bets.clear()

class Player:
	"""
	This is a superclass from which each player specialisation inherits from.
	Chapter 13, pages 79-84
	"""
	def __init__(self, table):
		self.stake = 200
		self.roundsToGo = 30
		self.table = table
		self.initialBet = 10
		self.nextBet = self.initialBet

	def win(self, bet:Bet):
		amountWon = bet.winAmount()
		self.stake += amountWon

	def lose(self, bet:Bet):
		amountLost = bet.loseAmount()
		self.stake -= amountLost

	def isPlaying(self) -> bool:
		return (self.stake >= self.nextBet) and self.roundsToGo != 0

	def placeBets(self):
		if self.isPlaying():
			self.newBet = Bet(self.nextBet, self.specificBet)
			# print(self.roundsToGo, self.newBet, self.initialBet, self.betMultiple)
			try:
				self.table.placeBet(self.newBet)
			except (InvalidBet) as error:
				raise InvalidBet('Over table limit')

	def reset(self):
		pass

class PlayerRandom(Player):
	def __init__(self, table:Table):
		super().__init__(table)
		self.rng = random.Random()
		self.rng.seed(4)
	
	def placeBets(self):
		self.specificBet = self.table.wheel.bins[self.rng.randint(0,37)]
		return super().placeBets()

class PlayerFibonacci(Player):
	def __init__(self):
		self.recent:int = 1
		self.previous:int = 0
	
	def win(self, bet:Bet):
		super().win(bet)
		self.recent = 1
		self.previous = 0

	def lose(self, bet:Bet):
		super().lose(bet)
		self.next:int = self.recent + self.previous
		self.previous = self.recent
		self.recent = self.next

class Passenger57:
	"""
	Passenger57 is a player who always bets on black
	This class is used to test the game functionality, it's not a strategy used in the simulation (or much of a strategy anyway)
	Chapter 11, pages 69-73
	"""
	def __init__(self, table, wheel):
		self.wheel = wheel
		self.table = table

	def placeBets(self):
		self.black = Outcome("Black", 1)  # TODO - much later - remove duplication
		self.table.place_bet(Bet(1, self.black))

	def win(self, bet):
		print("Your bet was a winner, you won: {}".format(bet.winAmount()))

	def lose(self, bet):
		print("Your bet was a loser")

class Martingale(Player):
	"""
	This player doubles their bet on every loss and resets their bet on a win.
	Chapter 13, pages 79-84
	"""
	def __init__(self, table:Table):
		super().__init__(table)
		self.lossCount = 0
		self.betMultiple = 1
		self.specificBet = table.wheel.getOutcome('Black')

	def placeBets(self):
		self.nextBet = self.initialBet * self.betMultiple
		super().placeBets()

	def win(self, bet:Bet):
		super().win(bet)
		self.lossCount = 0
		self.betMultiple = 1

	def lose(self, bet:Bet):
		super().lose(bet)
		self.lossCount += 1
		self.betMultiple *= 2

	def reset(self):
		super().reset()
		self.lossCount = 0
		self.betMultiple = 1

class SevenReds(Martingale):
    """
    SevenReds is a Martingale player who places bets in Roulette.
    This player waits for seven red wins in a row before betting black.
    Chapter 15, pages 91-94
    """
    def __init__(self, table):
        super().__init__(table)
        self.redCount = 7

    def placeBets(self):
        if self.redCount == 0:
            self.nextBet = self.initialBet * self.betMultiple
            super().placeBets()

    def winners(self, outcomes):
        if self.table.wheel.getOutcome('Red') in outcomes:
            self.redCount -= 1
        else:
            self.redCount = 7

class InvalidBet(Exception):
	"""
	InvalidBet is raised when the Player attempts to place a bet which exceeds the table’s limit.
	Chapter 10, pages 66-67
	"""
	def __init__(self, expression):
		self.expression = expression

class RouletteGame:
	"""
	This class manages the game state through the cycle method (place a bet, spin the wheel, settle bets)
	Chapter 11, pages 69-73
	"""
	def __init__(self, wheel:Wheel, table:Table):
		self.wheel = wheel
		self.table = table

	def cycle(self, player:Player):
		self.table.clearBets()  # added
		player.placeBets()
		winning_bin:Bin = self.table.wheel.next()
		for betmade in self.table.bets:
			winner = False
			for winning_outcome in winning_bin:
				if betmade.outcome.name == winning_outcome.name:
					player.win(betmade)
					winner = True
					break
			if winner == False:
				player.lose(betmade)

		player.roundsToGo -= 1

class Simulator:
	"""
	Return statistics of a game with a given player and their betting strategy
	Chapter 18, pages 85-89
	"""
	def __init__(self, player:Player, game:RouletteGame):
		self.player = player
		self.game = game
		self.initDuration = 250
		self.initStake = 1000
		self.samples = 50

	def session(self):
		self.player.stake = self.initStake
		self.player.roundsToGo = self.samples
		self.player.initialBet = 10
		self.player.nextBet = 10
		stakeList = list()

		try:
			while self.player.isPlaying():
				self.game.cycle(self.player)
				stakeList.append(self.player.stake)
		except (InvalidBet) as error:
			return stakeList
		return stakeList

	def gather(self):
		durations = list()
		maxima = list()

		for _ in range(self.initDuration):
			self.player.reset()
			sessionStakes = self.session()
			durations.append(len(sessionStakes))
			maxima.append(max(sessionStakes))
		return maxima, durations

class IntegerStatistics(list):
	def mean(self):
		return sum(self) / len(self)

	def stdev(self):
		m = self.mean()
		return math.sqrt( sum( (x-m)**2 for x in self ) / (len(self)-1) )

rwheel = Wheel()
rtable = Table(100, rwheel)
rgame = RouletteGame(rwheel, rtable)
rsim = Simulator(PlayerRandom(rtable), rgame)
maxima, duration = rsim.gather()
print(maxima)
print(duration)
