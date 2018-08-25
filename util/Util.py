import math
import datetime

class Util:
	'''
	Convert time passed in seconds to days, hours, minutes, seconds 
	to be returned as a string
	'''
	def convertTimeFromSeconds(t):
		if math.isnan(t) or t == 0:
			return '0h 0m 0s'

		SECONDS_IN_MINUTE = 60
		MINUTES_IN_HOUR = 60
		HOURS_IN_DATE = 24
	
		minHourDay = math.floor(t/SECONDS_IN_MINUTE)
		hourDay = math.floor(minHourDay/MINUTES_IN_HOUR)

		seconds = math.floor(t%SECONDS_IN_MINUTE)
		minutes = minHourDay%MINUTES_IN_HOUR
		hours = hourDay%HOURS_IN_DATE
		days = math.floor(hourDay/HOURS_IN_DATE)
	
		retTime = ''
	
		if days > 0:
			retTime = retTime + str(days) + 'd '

		if days > 0 or hours > 0:
			retTime = retTime + format(hours, '02d') + 'h '

		if minutes > 0 or days > 0 or hours > 0:
			retTime = retTime + format(minutes, '02d') + 'm '

		retTime = retTime + format(seconds, '02d') + 's'

		return retTime

	'''
	d1: datetime
	return: the Sunday before the passed date, 
	  if the passed date is a Sunday it will return the Sunday a week ago. 
	Take the passed in date as the weekday number and increment it by one.
	Then subtract the passed in date by the index to get the previous Sunday
	'''
	def getPreviousSunday(d1):
		idx = (d1.weekday() + 1)
		sun = d1 - datetime.timedelta(idx)
		return sun

