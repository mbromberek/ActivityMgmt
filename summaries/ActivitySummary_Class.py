from summaries.ExerciseInfo_Class import ExerciseInfo

class ActivitySummary:
	totDays = ''

	totSteps = ''
	avgSteps = ''
	
	totDist = ''
	avgDist = ''
	
	totActiveCal = ''
	avgActiveCal = ''
	
	totFloors = ''
	avgFloors = ''
	
	def __init__(self, startDate, endDate):
		self.startDate = startDate
		self.endDate = endDate
		self.exRun = ExerciseInfo('Running')
	
	def __str__(self):
		return '{:%Y-%m-%d}'.format(self.startDate) + ' to ' + '{:%Y-%m-%d}'.format(self.endDate)
	
	def __repr__(self):
		return (f'{self.__class__.__name__}(Range('
				f'{self.startDate!r}, {self.endDate!r}))'
				)

	def printSummary(self):
		print('Activity Summary for ' + '{:%Y-%m-%d}'.format(self.startDate) + ' to ' + '{:%Y-%m-%d}'.format(self.endDate) + ':')
		print('\tTotal Steps: ' + str(self.totSteps))
		print('\tTotal Miles: ' + '{0:.{1}f}'.format(self.totDist,2))
		print('\tTotal Calories: ' + str(self.totActiveCal))