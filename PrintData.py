from summaries.ActivitySummary_Class import ActivitySummary
from summaries.ExerciseInfo_Class import ExerciseInfo
from util.Util import Util

###############################################
# Gets list of activities
# Prints Activity details with comparison to 
#  previous week. 
###############################################
# def printSummary(actvSummaryLst):
# 	for i in range(len(actvSummaryLst)-1):
# 		currWk = actvSummaryLst[i]
# 		prevWk = actvSummaryLst[i+1]
# 		
# 		print('Week of ' + '{:%Y-%m-%d}'.format(currWk.startDate) + 
# 			' to ' + '{:%Y-%m-%d}'.format(currWk.endDate) + ':')
# 		wkDiff = currWk.exRun.ct - prevWk.exRun.ct
# 		diffInd = ''
# 		if (wkDiff < 0):
# 			diffInd = 'less'
# 			wkDiff = abs(wkDiff)
# 		else:
# 			diffInd = 'more'		
# 		print('\tNumber of Runs: ' + '{0:.{1}f}'.format(currWk.exRun.ct,0) + 
# 			' (' + 
# 			'{0:.{1}f} '.format(wkDiff,0) + 
# 			diffInd + 
# 			' than previous week)')
# 		
# 		wkDiff = currWk.exRun.distTot - prevWk.exRun.distTot
# 		if (wkDiff < 0):
# 			diffInd = 'less'
# 			wkDiff = abs(wkDiff)
# 		else:
# 			diffInd = 'more'
# 		print('\tRan ' + '{0:.{1}f}'.format(currWk.exRun.distTot,2) + ' Miles' + 
# 			' (' + '{0:.{1}f} '.format(wkDiff,2) + diffInd + 
# 			' than previous week)'
# 			)
# 
# 		wkDiff = currWk.exRun.durTot - prevWk.exRun.durTot
# 		if (wkDiff < 0):
# 			diffInd = 'less'
# 			wkDiff = abs(wkDiff)
# 		else:
# 			diffInd = 'more'
# 		print('\tRan for ' + Util.convertTimeFromSeconds(currWk.exRun.durTot) + 
# 			' (' + Util.convertTimeFromSeconds(wkDiff) + ' ' + diffInd + 
# 			' than previous week)'
# 			)

###############################################
# Gets list of activities
# Generate Activity details with comparison to 
#  previous week. 
# Creates a list of Strings that will be joined together to create summary to return	
###############################################
def generateSummary(actvSummaryLst):
	strLst = []

	for i in range(len(actvSummaryLst)-1):
		currWk = actvSummaryLst[i]
		prevWk = actvSummaryLst[i+1]

		# Generate Header for Week
		strLst.append('\n')
		strLst.append('Week of ')
		strLst.append('{:%Y-%m-%d}'.format(currWk.startDate))
		strLst.append(' to ')
		strLst.append('{:%Y-%m-%d}'.format(currWk.endDate) + ':')
		strLst.append('\n')

		strLst.append(generateGenericActivitySummary(currWk, prevWk))

		if ('exRun' in vars(currWk)):
			strLst.append(generateRunSummary(currWk, prevWk))
		
		if ('exSwim' in vars(currWk)):
			strLst.append(generateSwimSummary(currWk.exSwim))

		if ('exCycle' in vars(currWk)):
			strLst.append(generateCycleSummary(currWk.exCycle))
		
		strLst.append('\n')
	
	return ''.join(strLst)

###############################################
# Generate text to display using passed currWk
# and getting difference compared with passed 
# prevWk.
# Stats used in summary
#  - steps
#  - distance
#  - Calories
# Return text to display as a String
###############################################
def generateGenericActivitySummary(currWk, prevWk):

	strLst = []
	
	wkDiffSteps = currWk.totSteps - prevWk.totSteps
	diffIndSteps = ''
	if (wkDiffSteps < 0):
		diffIndSteps = ' down'
		wkDiffSteps = abs(wkDiffSteps)
	else:
		diffIndSteps = ' up'
	strLst.append('\tSteps: ')
	strLst.append('{0:,.{1}f}'.format(currWk.totSteps,0))
	strLst.append(' (')
	strLst.append('{0:,.{1}f}'.format(wkDiffSteps,0))
	strLst.append(diffIndSteps)
	strLst.append(')')

	wkDiffDist = currWk.totDist - prevWk.totDist
	diffIndDist = ''
	if (wkDiffDist < 0):
		diffIndDist = ' down'
		wkDiffDist = abs(wkDiffDist)
	else:
		diffIndDist = ' up'
	strLst.append('\n\tMiles: ')
	strLst.append('{0:,.{1}f}'.format(currWk.totDist,2))
	strLst.append(' (')
	strLst.append('{0:,.{1}f}'.format(wkDiffDist,2))
	strLst.append(diffIndDist)
	strLst.append(')')

	wkDiffActvCal = currWk.totActiveCal - prevWk.totActiveCal
	diffIndActvCal = ''
	if (wkDiffActvCal < 0):
		diffIndActvCal = ' down'
		wkDiffActvCal = abs(wkDiffActvCal)
	else:
		diffIndActvCal = ' up'
	strLst.append('\n\tActive Calories: ')
	strLst.append('{0:,.{1}f}'.format(currWk.totActiveCal,0))
	strLst.append(' (')
	strLst.append('{0:,.{1}f}'.format(wkDiffActvCal,0))
	strLst.append(diffIndActvCal)
	strLst.append(')')
	strLst.append('\n')
	return ''.join(strLst)

###############################################
# Generate text to display for Runs using passed 
# currWk and getting difference compared with 
# passed prevWk.
# Stats used in summary
#  - Count
#  - Distance
#  - Times
#  - Details on currWk Easy Runs
#  - Details on currWk Long Run
# Return text to display as a String
###############################################
def generateRunSummary(currWk, prevWk):
	strLst = []
	
	currEx = currWk.exRun
	prevEx = ''
	if 'exRun' in vars(prevWk):
		prevEx = prevWk.exRun
	else:
		prevEx = ExerciseInfo('Running')
	
	# Count of Runs
	wkDiff = currEx.ct - prevEx.ct
	diffInd = ''
	if (wkDiff < 0):
		diffInd = 'down'
		wkDiff = abs(wkDiff)
	else:
		diffInd = 'up'				
	strLst.append('\tRuns Count: ')
	strLst.append('{0:.{1}f}'.format(currEx.ct,0))
	strLst.append(' (')
	strLst.append('{0:.{1}f} '.format(wkDiff,0))
	strLst.append(diffInd)
	strLst.append(')')
	strLst.append('\n')
	
	# Run Distances
	wkDiff = currEx.distTot - prevEx.distTot
	if (wkDiff < 0):
		diffInd = 'down'
		wkDiff = abs(wkDiff)
	else:
		diffInd = 'up'
	strLst.append('\tRan ')
	strLst.append('{0:.{1}f}'.format(currEx.distTot,2))
	strLst.append(' Miles')
	strLst.append(' (')
	strLst.append('{0:.{1}f} '.format(wkDiff,2))
	strLst.append(diffInd)
	strLst.append(')')
	strLst.append('\n')

	# Run Times
	wkDiff = currEx.durTot - prevEx.durTot
	if (wkDiff < 0):
		diffInd = ' down'
		wkDiff = abs(wkDiff)
	else:
		diffInd = ' up'
	strLst.append('\tRan for ')
	strLst.append(Util.convertTimeFromSeconds(currEx.durTot))
	strLst.append(' (')
	strLst.append(Util.convertTimeFromSeconds(wkDiff))
	strLst.append(diffInd)
	strLst.append(')')
	strLst.append('\n')

	strLst.append('\tEasy Runs avg pace was ')
	strLst.append(Util.convertTimeFromSeconds(currEx.avgEasyPace))
	strLst.append(' with avg heart rate of ')
	strLst.append(str(round(currEx.avgEasyHr,2)))
	strLst.append('\n')
	
	if ('avgLongDur' in vars(currEx)):
		strLst.append('\tLong run: ')
		strLst.append(Util.convertTimeFromSeconds(currEx.avgLongDur))
		strLst.append(' for ')
		strLst.append(str(currEx.avgLongDist))
		strLst.append(' miles, with avg pace ')
		strLst.append(Util.convertTimeFromSeconds(currEx.avgLongPace))
		strLst.append(', and avg heart rate ')
		strLst.append(str(currEx.avgLongHr))
		strLst.append('\n')


	return ''.join(strLst)
	
###############################################
# Generate text to display for Runs using passed 
# currWk and getting difference compared with 
# passed prevWk.
# Stats used in summary
#  - Count
#  - Distance
#  - Times
# Return text to display as a String
###############################################
def generateSwimSummary(ex):
	strLst = []
	
	strLst.append('\tSwim Count: ')
	strLst.append(str(ex.ct))
	strLst.append('\n')
	strLst.append('\tSwam ')
	strLst.append(str(ex.distTot))
	strLst.append(' yards')
	strLst.append('\n')
	strLst.append('\tSwam for ')
	strLst.append(Util.convertTimeFromSeconds(ex.durTot))
	strLst.append('\n')
	
	return ''.join(strLst)

###############################################
# Generate text to display for Runs using passed 
# currWk and getting difference compared with 
# passed prevWk.
# Stats used in summary
#  - Count
#  - Distance
#  - Times
# Return text to display as a String
###############################################
def	generateCycleSummary(ex):
	strLst = []
	strLst.append('\tBike ride Count: ')
	strLst.append(str(ex.ct))
	strLst.append('\n')
	strLst.append('\tBiked ')
	strLst.append(str(ex.distTot))
	strLst.append(' Miles')
	strLst.append('\n')
	strLst.append('\tBiked for ')
	strLst.append(Util.convertTimeFromSeconds(ex.durTot))
	strLst.append('\n')
	
	return ''.join(strLst)


def printExerciseSummary(actv):
	print('Exercise Summary for ' + '{:%Y-%m-%d}'.format(actv.startDate) + 
		' to ' + 
		'{:%Y-%m-%d}'.format(actv.endDate) + ':')

	if ('exRun' in vars(actv)):
		ex = actv.exRun
		print('\tNumber of Runs: ' + '{0:.{1}f}'.format(ex.ct,0))
		print('\tRan ' + '{0:.{1}f}'.format(ex.distTot,2) + ' Miles')
		print('\tRan for ' + Util.convertTimeFromSeconds(ex.durTot))
		print('\t' +
			'Easy Runs avg pace was ' + 
			Util.convertTimeFromSeconds(ex.avgEasyPace) + 
			' with avg heart rate of ' + str(round(ex.avgEasyHr,2))
		)
		print('\t' +
			'Ran long run in ' + Util.convertTimeFromSeconds(ex.avgLongDur) +
			' for ' + str(ex.avgLongDist) + ' miles,' +
			' with an avg pace of ' + 
			Util.convertTimeFromSeconds(ex.avgLongPace) +
			', and avg heart rate of ' + str(ex.avgLongHr)
		)

		print('\tTotal Duration: ' + str(ex.durTot))

	if ('exSwim' in vars(actv)):
		ex = actv.exSwim
		print('\tNumber of swims: ' + str(ex.ct))
		print('\tSwam ' + str(ex.distTot) + ' yards')
		print('\tSwam for ' + Util.convertTimeFromSeconds(ex.durTot))
	if ('exCycle' in vars(actv)):
		ex = actv.exCycle
		print('\tNumber of bike rides: ' + str(ex.ct))
		print('\tBiked ' + str(ex.distTot) + ' Miles')
		print('\tBiked for ' + Util.convertTimeFromSeconds(ex.durTot))



# def printWeeklySummary(acctSummaryLst, exSummaryLst):
# 	print('')
# 	for i in range(len(acctSummaryLst)):
# 		acctSummaryLst[i].printSummary()
# 		printExerciseSummary(acctSummaryLst[i])
# 		print('')
