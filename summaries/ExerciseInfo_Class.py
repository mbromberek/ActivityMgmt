#! /Users/mikeyb/Applications/python3
from summaries.Weather_Class import WeatherInfo

METERS_TO_FEET = 3.28084

class ExerciseInfo:
	type = ''
	eDate = ''
	startTime = ''
	endTime = ''
	distTot = 0
	distUnit = ''
	
	durTot = 0
	hourTot = 0
	minTot = 0
	secTot = 0
	
	rating = ''
	
	calTot = 0
	avgHeartRate = ''
	userNotes = ''
	
	temperature = ''
	
	gear = ''
	category = ''
	
	source = ''
	
	# Filename the data came from or link to data
	originLoc = ''
	
	elevationGain = ''
	elevationLoss = ''
	
	startLat = ''
	startLon = ''
	endLat = ''
	endLon = ''
	
	startWeather = WeatherInfo()
	endWeather = WeatherInfo()
	
	

	def __init__(self, type):
		self.type = type
	
	def __str__(self):
		return self.type + ' {:%Y-%m-%d}'.format(self.startTime) + ' to ' + '{:%Y-%m-%d}'.format(self.endTime)


	def cycleDateTime():
		return self.runDate + ' ' + self.runTime

	def elevationChange(self):
		return '{0:.{1}f}'.format(self.elevationGain*METERS_TO_FEET,1) + '↑\n' + '{0:.{1}f}'.format(self.elevationLoss*METERS_TO_FEET,1) + '↓'
