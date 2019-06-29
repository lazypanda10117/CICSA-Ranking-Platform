from misc.CustomElements import Dispatcher
from api.config.league_scoring import LeagueScoringConfig

class ConfigReader:
	def __init__(self, path):
		self.path = path
		self.config_dispatcher = self.setConfigDispatcher()

	def setConfigDispatcher(self):
		dispatcher = Dispatcher()
		dispatcher.add('league_scoring', LeagueScoringConfig)
		return dispatcher

	def getRootConfig():
		return self.config_dispatcher.get(self.path)