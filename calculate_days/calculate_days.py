import random as rd
import datetime
import time
import itertools
import os
import numpy as np
#from scipy.stats import norm
import math
import inspect
import matplotlib
import matplotlib.pyplot as plt

def perform_error_check(date_1,date_2):
	if date_1[0] > date_2[0]:
		raise ValueError('Second input date must be "larger" than first input date')
	elif date_1[0] == date_2[0]:
		if date_1[1] > date_2[1]:
			raise ValueError('Second input date must be "larger" than first input date')
		elif date_1[1] == date_2[1]:
			if date_1[2] > date_2[2]:
				raise ValueError('Second input date must be "larger" than first input date')
	if date_1[0] < 1582:
		raise ValueError('Input year must later than 1582')
	if date_1[1] > 12 or date_2[1] > 12:
		raise ValueError('Incorrect date format')
	else:
		dates = [date_1,date_2]
		for i in range(2):
			dpm = get_dpm(dates[i][0])
			if dates[i][2] > dpm[dates[i][1]-1]:
				raise ValueError('Incorrect date format. Number of days in input is ' + str(dates[i][2]) + ', but max input should be ' + str(dpm[dates[i][1]-1]))

def is_leap_year(year):
	"""
	These extra days occur in years which are multiples of four (with the exception of years divisible by 100 but not by 400)
	"""
	val = False;
	if year % 4 == 0:
		val = True
		if year % 100 == 0 and year % 400 != 0:
			val = False;
	return val

def get_dpm(year):
	tmp = [31,28,31,30,31,30,31,31,30,31,30,31]
	if is_leap_year(year):
		tmp[1] = 29
	return tmp

def number_of_days(m1,d1,m2,d2,year):
	dpm = get_dpm(year)
	num_of_days = []
	months = [m1,m2]
	days = [d1,d2]
	for i,month in enumerate(months):
		if month == 1:
			num_of_days.append(days[i])
		else:
			tmp_var = 0
			for k in range(month-1):
				#print('Adding ' + str(dpm[k]) + ' days for month ' + str(k+1))
				tmp_var += dpm[k]
			#print('Adding ' + str(days[i]) + ' days for last month ')	
			num_of_days.append(tmp_var+days[i])
	return num_of_days

def next_date(date):
	dpm = get_dpm(date[0])
	if date[2] == dpm[date[1]-1]:
		if date[1] == 12:
			date[0] += 1
			date[1] = 1
			date[2] = 1
		else:
			date[1] += 1
			date[2] = 1

	else:
		date[2] += 1
	return date

def is_before(date_1, date_2):
	# return True if date_1 is before date_2
	print('Date-1: ' + str(date_1))
	print('Date-2: ' + str(date_2))
	if date_1[0] > date_2[0]:
		return False
	elif date_1[0] == date_2[0]:
		if date_1[1] > date_2[1]:
			return False
		elif date_1[1] == date_2[1]:
			if date_1[2] >= date_2[2]:
				return False
	return True

def days_between_dates(date_1,date_2):
	perform_error_check(date_1,date_2)

	# Everything looks fine. Start the magic.
	nod = number_of_days(date_1[1],date_1[2],date_2[1],date_2[2],date_1[0])
	if date_1[0] == date_2[0]:
		return nod[1] - nod[0]
	else:
		tmp_var = 0
		for year in range(date_1[0],date_2[0]):
			if is_leap_year(year):
				tmp_var += 366
			else:
				tmp_var += 365
		nod[1] += tmp_var
		return nod[1]-nod[0]

def days_between_dates2(date_1,date_2):
	#perform_error_check(date_1,date_2)
	days = 0
	while is_before(date_1,date_2):
		print('A')
		days += 1
		date_1 = next_date(date_1)
	return days


start_date = [1985,7,24]
end_date = [1985,7,26]
iterations = 2

t0 = time.time()
for index in range(iterations):
	dx1 = days_between_dates(start_date,end_date)
dt1 = time.time() - t0

t0 = time.time()
for index in range(iterations):
	print('Iteration: ' + str(index))
	dx2 = days_between_dates2(start_date,end_date)
dt2 = time.time() - t0

print('D1: ' + str(dx1) + '. Time: ' + str(dt1))
print('D2: ' + str(dx2) + '. Time: ' + str(dt2))