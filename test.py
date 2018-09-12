'''This is the revamped program for the heatwave project led by Drew Shindell of Duke University. Coded by Tevin Brown'''
'''Dates: Fall 2016 - present'''
import numpy as np
import array
import numpy.ma as ma
import sys
import math
import scipy.io.netcdf as netcdf
from scipy.io.netcdf import *
import csv

#grab the data from 1980-1990
f = netcdf.netcdf_file('C:\Users\\tevin\EOS393\Hadley\HadGHCND_TXTN_acts_1981-1990_15102015.nc', 'r')
time = f.variables['time']
lat = f.variables['latitude']
lon = f.variables['longitude']
tmax = f.variables['tmax']
tmin = f.variables['tmin']




