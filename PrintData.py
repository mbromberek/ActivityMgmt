from summaries.ActivitySummary_Class import ActivitySummary
from summaries.ExerciseInfo_Class import ExerciseInfo
from util.Util import Util

###############################################
# Gets list of activities
# Prints Activity details with comparison to 
#  previous week. 
###############################################
def printSummary(actvSummaryLst):
	for i in range(len(actvSummaryLst)-1):
		currWk = actvSummaryLst[i]
		prevWk = actvSummaryLst[i+1]
		print('Week of ' + '{:%Y-%m-%d}'.format(currWk.startDate) + 
			' to ' + '{:%Y-%m-%d}'.format(currWk.endDate) + ':')
		wkDiff = currWk.exRun.ct - prevWk.exRun.ct
		diffInd = ''
		if (wkDiff < 0):
			diffInd = 'less'
			wkDiff = abs(wkDiff)
		else:
			diffInd = 'more'		
		print('\tNumber of Runs: ' + '{0:.{1}f}'.format(currWk.exRun.ct,0) + 
			' (' + 
			'{0:.{1}f} '.format(wkDiff,0) + 
			diffInd + 
			' than previous week)')
		
		wkDiff = currWk.exRun.distTot - prevWk.exRun.distTot
		if (wkDiff < 0):
			diffInd = 'less'
			wkDiff = abs(wkDiff)
		else:
			diffInd = 'more'
		print('\tRan ' + '{0:.{1}f}'.format(currWk.exRun.distTot,2) + ' Miles' + 
			' (' + '{0:.{1}f} '.format(wkDiff,2) + diffInd + 
			' than previous week)'
			)

		wkDiff = currWk.exRun.durTot - prevWk.exRun.durTot
		if (wkDiff < 0):
			diffInd = 'less'
			wkDiff = abs(wkDiff)
		else:
			diffInd = 'more'
		print('\tRan for ' + Util.convertTimeFromSeconds(currWk.exRun.durTot) + 
			' (' + Util.convertTimeFromSeconds(wkDiff) + ' ' + diffInd + 
			' than previous week)'
			)
		

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



# def printWeeklySummary(w1_actSummary, w2_actSummary, w1_exSummary, w2_exSummary):
# 	print('')
# 	w1_actSummary.printSummary()
# 	printExerciseSummary(w1_exSummary)
# 	print('')
# 
# 	w2_actSummary.printSummary()		
# 	printExerciseSummary(w2_exSummary)
# 	print('')

def printWeeklySummary(acctSummaryLst, exSummaryLst):
	print('')
	for i in range(len(acctSummaryLst)):
		acctSummaryLst[i].printSummary()
# 		printExerciseSummary(exSummaryLst[i])
		printExerciseSummary(acctSummaryLst[i])
		print('')
