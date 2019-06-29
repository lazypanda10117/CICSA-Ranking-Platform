# To get the League Score Json, run 'python LeagueTableParser.py > destination_file.json'

import csv
import json


class LeagueTableParser:
	TABLE_GROUP_DISTANCE = 2

	def __init__(self):
		self.csvToRead = [
			('A', 'Rank_A_Event_Score_Map.csv'),
			('B', 'Rank_B_Event_Score_Map.csv')
		]

	def parse(self):
		result = dict()
		for csvTuple in self.csvToRead:
			parsedTable = dict()
			
			csvCategory = csvTuple[0]
			csvFile = csvTuple[1]
			
			with open(csvFile, newline='') as csvfile:
				tableReader = csv.reader(csvfile, delimiter=',', quotechar='|')
				maxTeamNum = self.getMaxTeam()
				rowNum = 0

				for row in tableReader:
					teamIndex = maxTeamNum
					tempDistance = 0
					
					if rowNum == 0:
						rowNum += 1
						continue

					for col in row:
						if tempDistance < self.TABLE_GROUP_DISTANCE:
							if tempDistance == 1:
								if teamIndex not in parsedTable:
									parsedTable[teamIndex] = dict()
								try:
									score = float(col)
								except:
									score = 0.0
								parsedTable[teamIndex][rowNum] = score
							tempDistance += 1
						else:
							teamIndex -= 1
							tempDistance = 0
					rowNum += 1

			result[csvCategory] = self.pruneData(parsedTable)

		print(json.dumps(result, indent=4, sort_keys=True))

	def pruneData(data):
		response = dict()
		for rankScores in data:
			for score in rankScores:
				

	def getMaxTeam(self):
		with open('WomenA.csv', newline='') as csvfile:
			tableReader = csv.reader(csvfile, delimiter=' ', quotechar='|')
			counter = 0
			for row in tableReader:
				counter += 1
			return counter - 1 if counter > 0 else 0					

LeagueTableParser().parse()