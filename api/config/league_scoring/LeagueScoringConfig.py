from misc.CustomElements import Dispatcher
from api.config.GenericAppConfig import GenericAppConfig


class LeagueScoringConfig(GenericAppConfig):
	def getConfigFilesPath(self):
		return 'league_scoring/'

	def setConfigDispatcher(self):
		dispatcher = Dispatcher()
		dispatcher.add('league_rank_place_score_map', 'league_score_mapping.json')
		return dispatcher
