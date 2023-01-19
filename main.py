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

	def __eq__(self, other) -> boolean:
		return self.name == other.name

	def __ne__(self, other) -> boolean:
		return not self.name == other.name

	def __hash__(self) -> int:
		return hash(self.name)

	def __str__(self) -> str:
		return