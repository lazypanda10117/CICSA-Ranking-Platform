import json
from misc.CustomElements import Dispatcher


class LeagueScoringConfig:
	def __init__(self):
		self.config_dispatcher = self.setConfigDispatcher()

	def setConfigDispatcher(self):
		dispatcher = Dispatcher()
		dispatcher.add('league_rank_place_score_map', 'league_score_mapping.json')
		return dispatcher

	def getData(self, identifier):
		with open(self.config_dispatcher.get(identifier)) as config_json:
			config = json.load(config_json)
			return config
