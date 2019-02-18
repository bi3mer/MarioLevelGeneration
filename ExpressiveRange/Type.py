from .CoinRewards import coin_rewards
from .Linearity import linearity
from .Enemies import enemies
from .Rewards import rewards

from enum import Enum

import sys

class Type(Enum):
	CoinReward = 0
	Enemies = 1
	Linearity = 2
	Rewards = 3

	def evaluate(self, level_map):
		if self == Type.CoinReward:
			return coin_rewards(level_map)
		elif self == Type.Enemies:
			return enemies(level_map)
		elif self == Type.Linearity:
			return linearity(level_map)
		elif self == Type.Rewards:
			return rewards(level_map)

		print('A horrible error has occurred where the type does not match any type defined.')
		print(f'{self} ?????')
		sys.exit(0)