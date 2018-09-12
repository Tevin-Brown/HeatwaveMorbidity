'''This is the revamped program for the heatwave project led by Drew Shindell of Duke University. Coded by Tevin Brown'''
'''Dates: Fall 2016 - present'''
import numpy as np
import array
import numpy.ma as ma
import sys
import math
import netCDF4 as netcdf



#grab the data from 1987-2005
# f = netcdf.Dataset('C:\Users\\tevin\EOS393\\1987-2005\\tmax.1987.nc', 'r', format="NETCDF4")
# tmax = f.variables['tmax']
# f = netcdf.Dataset('C:\Users\\tevin\EOS393\\1987-2005\\tmin.1987.nc', 'r', format="NETCDF4")
# tmin = f.variables['tmin']

#grab data for decade 80s
f = netcdf.Dataset('C:\Users\\tevin\EOS393\Hadley\HadGHCND_TXTN_acts_1981-1990_15102015.nc', 'r', format="NETCDF3")
tmin = f.variables['tmin']
tmax = f.variables['tmax']
print tmin[0][30][10]
print tmax[0][30][10]


# def tmean(tmin,tmax):
#     globaltmean = np.zeros_like(tmin)
#     for i in range(len(tmin)): #corresponds to time
#         for j in range(25-54): #corresponds to lat (N/S)
#             for k in range(235,294): #corresponds to lon (E/W)
#                 globaltmean[i][j][k] = (tmin[i][j][k] + tmax[i][j][k])/2 
#     return globaltmean
# tmean = tmean(tmin,tmax)
# print tmean[0][300][500]

# def reformat(tmean):
#     globaltemps = np.zeros(len(tmean[0]),len(tmean[0][0]),153,dtype=np.float64)
#     for i in range(153): #corresponds to time
#         for j in range(len(tmean[0])): #corresponds to lat
#             for k in range(len(tmean[0][0])): #corresponds to lon
#                 globaltemps[j][k][i] = tmean[-245+i][j][k] 
#     return globaltemps
#     
# summeravtemps = reformat(tmean)
# print summeravtemps[0][0]



