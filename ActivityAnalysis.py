# pip3 install -r requirements.txt
# pip3 install --upgrade google-api-python-client

import os, platform
import datetime, time

import applescript
import GoogleConnection
from apiclient import discovery
import httplib2, base64
import math
import configparser, json
import pandas as pd

# Custom Classes
from summaries.ActivitySummary_Class import ActivitySummary
from summaries.ExerciseInfo_Class import ExerciseInfo
from util.Util import Util
import PrintData

# Column numbers for fields in spreadsheet
RANK_COL = 0
NAME_COL = 1
USERNAME_COL = 2
BRACKET_COL = 3
SCORE_COL = 4
PPR_COL = 5
CHAMPION_COL = 6

config = configparser.ConfigParser()

'''
Get activity details from Google Sheet
	Split out the header and data from results
Return: header and data
'''
def getActivities(service, spreadsheetId, sheetName):
	rangeName = sheetName+'!A:I'
	result = service.spreadsheets().values().get(
		spreadsheetId=spreadsheetId, range=rangeName).execute()
	values = result.get('values', [])
	
	# Convert headers to lowercase and replace spaces with _
	activityHdr = [x.lower().replace(' ','_') for x in values[0]]
	activityData = values[1:]
		
	return activityHdr, activityData

'''
Using past in header and data create DataFrame
	Convert columns to correct formats
	Generate Index

Return: generated DataFrame
'''
def generateActivityDataFrame(hdr, data):
	numericCols = ['distance', 'steps','floors_climbed', 'tot_cal_burned','active_calories', 'weight_(lb)']
	dateCols = ['date']
	df = pd.DataFrame(data,columns=hdr)
	
	# Set number and date columns to numeric and datetime formats
	df[numericCols] = df[numericCols].apply(pd.to_numeric, errors='coerce')
	df[dateCols] = df[dateCols].apply(pd.to_datetime, errors='coerce')

	# Create dateStr column as a string of the date column and make it the index
	df['dateStr'] = df['date'].dt.strftime('%Y-%m-%d')
	df = df.set_index('dateStr')
	
	return df

def generateExerciseDataFrame(exLst):
	numericCols = ['distanseVal', 'caloriesVal','durationVal', 'hrVal']
	dateCols = ['dateVal']

	exDf = pd.DataFrame(exLst)	
	
	exDf[numericCols] = exDf[numericCols].apply(pd.to_numeric, errors='coerce')
	exDf[dateCols] = exDf[dateCols].apply(pd.to_datetime, errors='coerce')

	# Create dateStr column as a string of the date column and make it the index
	exDf['dateStr'] = exDf['dateVal'].dt.strftime('%Y-%m-%d')
	exDf = exDf.set_index('dateStr')
	
	# Need to sort for the loc function to work in exSummary
	exDf = exDf.sort_values(by=['dateVal'])

	return exDf


def exSummary(df,  dtStart, dtEnd):
	dfRange = df.loc['{:%Y-%m-%d}'.format(dtStart):'{:%Y-%m-%d}'.format(dtEnd)]
	
	ex = {}
	ex['startDate'] = dtStart
	ex['endDate'] = dtEnd
	ex['totDays'] = (dtEnd - dtStart).days
# 	ex['run'] = {}
# 	ex['swim'] = {}
# 	ex['cycle'] = {}
		
# 	print('dfRange:')
# 	print('{:%Y-%m-%d}'.format(dtStart) + ' and ' + '{:%Y-%m-%d}'.format(dtEnd))
# 	print(dfRange)

	ex['run'] = ExerciseInfo('Running')
	ex['run'].startTime = dtStart
	ex['run'].endTime = dtEnd
	ex['run'].distTot = dfRange[dfRange['typeVal']=='Running'].sum()['distanseVal']
	ex['run'].durTot = dfRange[dfRange['typeVal']=='Running'].sum()['durationVal']

	ex['run'].ct = dfRange[dfRange['typeVal']=='Running'].count()['typeVal']
	ex['run'].avgEasyPace = dfRange[(dfRange['typeVal']=='Running') &	(dfRange['catVal']=='Easy')].mean()['paceVal']
	ex['run'].avgEasyHr = dfRange[(dfRange['typeVal']=='Running') &	(dfRange['catVal']=='Easy')].mean()['hrVal']

	ex['run'].avgLongDist = dfRange[(dfRange['typeVal']=='Running') &	(dfRange['catVal']=='Long Run')].mean()['distanseVal']
	ex['run'].avgLongPace = dfRange[(dfRange['typeVal']=='Running') &	(dfRange['catVal']=='Long Run')].mean()['paceVal']
	ex['run'].avgLongHr = dfRange[(dfRange['typeVal']=='Running') &	(dfRange['catVal']=='Long Run')].mean()['hrVal']
	ex['run'].avgLongDur = dfRange[(dfRange['typeVal']=='Running') &	(dfRange['catVal']=='Long Run')].mean()['durationVal']
	
	
	ct = dfRange[dfRange['typeVal']=='Swimming'].count()['typeVal']
	if (ct > 0):
		ex['swim'] = ExerciseInfo('Swimming')
		ex['swim'].distTot = dfRange[dfRange['typeVal']=='Swimming'].sum()['distanseVal']
		ex['swim'].durTot = dfRange[dfRange['typeVal']=='Swimming'].sum()['durationVal']
		ex['swim'].ct = ct

	ct = dfRange[dfRange['typeVal']=='Cycling'].count()['typeVal']
	if (ct > 0):
		ex['cycle'] = ExerciseInfo('Cycling')
		ex['cycle'].distTot = dfRange[dfRange['typeVal']=='Cycling'].sum()['distanseVal']
		ex['cycle'].durTot = dfRange[dfRange['typeVal']=='Cycling'].sum()['durationVal']
		ex['cycle'].ct = ct
	
	return ex


'''

'''
def calcSummary(actvDf, exDf, dtStart, dtEnd):
	dfRange = actvDf.loc['{:%Y-%m-%d}'.format(dtStart):'{:%Y-%m-%d}'.format(dtEnd)]
# 	print('calcSummary:')
# 	print(dfRange)
	
	activ = ActivitySummary(dtStart, dtEnd)
	
	activ.totDays = (dtEnd - dtStart).days
	
	activ.totSteps = dfRange['steps'].sum()
	activ.totDist = dfRange['distance'].sum()
	activ.totActiveCal = dfRange['active_calories'].sum()
	activ.totFloors = dfRange['floors_climbed'].sum()
	
	exerciseSummaries = exSummary(exDf, dtStart, dtEnd)
	if ('run' in exerciseSummaries):
		activ.exRun = exerciseSummaries['run']
	if ('swim' in exerciseSummaries):
		activ.exSwim = exerciseSummaries['swim']
	if ('cycle' in exerciseSummaries):
		activ.exCycle = exerciseSummaries['cycle']
	
	return activ




'''
'''
def sendEmail(service, message_text):
	message = MIMEText(message_text)
	message['to'] = to
	message['from'] = sender
	message['subject'] = subject
	
	emailMsg = {'raw': base64.urlsafe_b64encode(message.as_string().encode('utf-8'))}
	
	

#######################################################
# MAIN
#######################################################
def main():
	# Get config details
	progDir = os.path.dirname(os.path.abspath(__file__))	
	config.read(progDir + "/../configs/activityAnalysisConfig.txt")
	
	numWeeks = int(config['activity']['number_weeks'])
	if (numWeeks < 2):
		numWeeks = 2

	#Get start and end of previous week and week before that
	actvWeeks = []
	actvWeeks.append({})
	actvWeeks[0]['end'] = Util.getPreviousSunday(datetime.date.today())
	actvWeeks[0]['start'] = actvWeeks[0]['end'] - datetime.timedelta(days=6)
	for i in range(1,numWeeks):
		actvWeeks.append({})
		actvWeeks[i]['end'] = actvWeeks[i-1]['start'] - datetime.timedelta(days=1)
		actvWeeks[i]['start'] = actvWeeks[i]['end'] - datetime.timedelta(days=6)

	'''
	Pull details from Activity Spreadsheet
	'''
	gc = GoogleConnection
	credentials = gc.get_credentials()#might need to pass application name
	http = credentials.authorize(httplib2.Http())
	discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
					'version=v4')
	serviceSheet = discovery.build('sheets', 'v4', http=http,
							  discoveryServiceUrl=discoveryUrl)

	spreadsheetId = config['google_sheet']['spreadsheet_id']
	sheetId = config['google_sheet']['sheet_id']
	sheetName=config['google_sheet']['sheet_name']


	activityHdr, activityData = getActivities(serviceSheet, spreadsheetId, sheetName)	
	actvDf = generateActivityDataFrame(activityHdr, activityData)
	'''
	End Pull details from Activity Spreadsheet
	'''
	
	
	#End Google Sheet section

	'''
	Pull details from Exercise Spreadsheet
	'''	
	pathToAppleScript = config['applescript']['script_path']
	spreadsheetName = config['exercise']['spreadsheet_name']
	# ) Read applescript file for reading and updating exercise spreadseeht
	scptFile = open(pathToAppleScript + 'AddExercise.txt')
	scptTxt = scptFile.read()
	scpt = applescript.AppleScript(scptTxt)
	scpt.call('initialize',spreadsheetName)

	exLst = scpt.call('getExercises',config['exercise']['number_exercises_to_read'])
	#TODO Create function for setting up DataFrame and set key / datatypes like in generateActivties function
	exDf = generateExerciseDataFrame(exLst)
# 	print(exDf)
	'''
	End Pull details from Exercise Spreadsheet
	'''	
	
	
	actvSummaryLst = []
	exSummaryLst = []
	for i in range(len(actvWeeks)):
		actvSummaryLst.append(calcSummary(actvDf, exDf, actvWeeks[i]['start'], actvWeeks[i]['end']))
# 		exSummaryLst.append(exSummary(exDf, actvWeeks[i]['start'], actvWeeks[i]['end']))

	PrintData.printWeeklySummary(actvSummaryLst, exSummaryLst)
	
	PrintData.printSummary(actvSummaryLst)
	

	
# 	sendEmail
	


if __name__ == '__main__':
	main()

