'''This is the revamped program for the heatwave project led by Drew Shindell of Duke University. Coded by Tevin Brown'''
'''Dates: Fall 2016 - present'''
import numpy as np
from netCDF4 import Dataset




#grab data for decade 80s
f = Dataset('C:\Users\\tmb51\OneDrive\EOS393\Hadley\HadGHCND_TXTN_acts_1981-1990_15102015.nc', 'r', format="NETCDF3")
tmin = f.variables['tmin'][:]
tmax = f.variables['tmax'][:]
lats = f.variables['latitude'][:]
lons = f.variables['longitude'][:]
# print tmin[0][30][10]
# print tmax[0][30][10]
f.close()

# tmax = [[[80,85,90,95],[70,75,80,85]],[[90,95,95,90],[80,90,100,100]],[[70,75,70,80],[85,75,85,95]]]    #3 days, 2 longitude 4 latitudes
# tmin = [[[2,3,4,5],[3,4,5,6]],[[4,5,6,7],[5,6,7,8]],[[6,7,8,9],[7,8,9,10]]]
# rh = [[[2,3,4,5],[3,4,5,6]],[[4,5,6,7],[5,6,7,8]],[[6,7,8,9],[7,8,9,10]]]


def reformat_mean(tmin,tmax):
    # print "hi"
    # use funtion to rearrange data into more usable format [lon][lat][day]
    ans = []
    for j in range(len(tmin[0])): #corresponds to lat
        temp = np.zeros((len(tmin[0][0]),1530),dtype=np.float)
        for k in range(len(tmin[0][0])): #corresponds to lon
            for i in range(153): #Change to 153 to get only summer temps (May - September)
                for year in range(10):
                    offset1 = year * 365 + 120
                    offset2 = year * 153
                    temp[k][i+offset2] = (tmin[i + offset1][j][k] + tmax[i + offset1][j][k] )/2.0 #Make i + 120 to start at May 1 for the year.
        ans.append(temp)
    # print "done"
    return ans
    
meantemps = reformat_mean(tmin,tmax)
# print meantemps[0][30][10]
# print


# def reformat_rh(rh):
#     # use funtion to rearrange data into more usable format [lat][lon][day]
#     ans = []
#     for j in range(len(rh[0])): #corresponds to lat
#         temp = np.zeros((len(rh[0][0]),len(rh)),dtype=np.float)
#         for k in range(len(rh[0][0])): #corresponds to lon
#             for i in range(len(rh)): #change to 153 to get only summerTemps (May - September)
#                 temp[k][i] = rh[i][j][k] #Make i + 120 to start at May 1 for the year.
#         ans.append(temp)
#     return ans
# 
# rhtemps = reformat_rh(rh)
# print rhtemps
# print
# 
# 
# def apparrent_Temp(rh,mt):
#     #returns apparent temperatures in the format we want
#     ans = np.zeros_like(rh)
#     for i in range(len(rh)):
#         for j in range(len(rh[0])):
#             for t in range(len(rh[0][0])):
#                 ans[i][j][t] = -42.379 + 2.04901523*mt[i][j][t] + 10.14333127*rh[i][j][t] - 0.22475541*mt[i][j][t]*rh[i][j][t] 
#                 - .00683783*(mt[i][j][t]**2) - .05481717*(rh[i][j][t]**2) + .00122874*(mt[i][j][t]**2)*rh[i][j][t] 
#                 + .00085282*mt[i][j][t]*(rh[i][j][t]**2) - .00000199*(mt[i][j][t]**2)*(rh[i][j][t]**2)
#                 
#     return ans
    
HItemps = meantemps
# print HItemps[0][30][10]
# print

def ninetyth_percentile(data):
    # Helper function that takes in the temps for an entire summer, returns the 90th percentile (assumes normal distribution of temps)
    ans = sorted(data)
    ind = int(len(data)*.9)
    return ans[ind]
    
def ninetyfifth_percentile(data):
    #helper Function to get the 95th percentile temperature over the decade
    ans = sorted(data)
    ind = int(len(data)*.95) # assumes normal distribution of temps
    return ans[ind]

def heatwaves(HItemps):
    #loops through the decade array and figures out if when there is a heat wave, and leave the temp in the slot, otherwise, replaces with a zero
    ans = np.zeros_like(HItemps)
    for i in range(len(HItemps)):
        for j in range(len(HItemps[0])):
            ninetyth = ninetyth_percentile(HItemps[i][j])
            ninetyfifth = ninetyfifth_percentile(HItemps[i][j])
            for t in range(len(HItemps[0][0])):
                if ninetyth < 85:
                    break
                if t == 0:
                    if ninetyfifth <= HItemps[i][j][t] and ninetyfifth <= HItemps[i][j][t+1]: #check for continuity (more than one day of heat)
                        ans[i][j][t] = HItemps[i][j][t]
                else:
                    if ninetyfifth <= HItemps[i][j][t] and (ninetyfifth <= HItemps[i][j][t-1] or ninetyfifth <= HItemps[i][j][t+1]): #check for continuity (more than one day of heat)
                        ans[i][j][t] = HItemps[i][j][t]
    return ans
    
heatwaves = heatwaves(HItemps)
# print heatwaves[0][30][10]
# print


#After having identified the heatwaves, I now need to asess the morbidity aspect that might be related to the heat waves.
#this requires grouping the heatwaves to see how long they last, timing in season, and  a 1F increase in summertime mean
def timing_mortality(heatwaves):
    #finds mortality over the season for a longitude and latitude
    ans = np.zeros((len(heatwaves),len(heatwaves[0])),dtype=np.float)
    for i in range(len(heatwaves)):
        for j in range(len(heatwaves[0])):
            for t in range(len(heatwaves[0][0])):
                if t == 0:
                    if heatwaves[i][j][t] != 0.0:
                        ans[i][j] += t*(-0.063) #heatwave factor for later timing
                else:
                    if heatwaves[i][j][t-1] == 0.0 and heatwaves[i][j][t] != 0.0:
                        ans[i][j] += t*(-0.063) #heatwave factor for later timing
    return ans
timing_mortality = timing_mortality(heatwaves)

def length_mortality(heatwaves):
    #finds mortality of heatwave due to the length of the heatwave
    ans = np.zeros((len(heatwaves),len(heatwaves[0])),dtype=np.float)
    for i in range(len(heatwaves)):
        for j in range(len(heatwaves[0])):
            count = 0 #since we are looking at the cumulative effect and not the effect of an individual heat wave, one count per location will suffice
            for t in range(1,len(heatwaves[0][0])):
                if heatwaves[i][j][t] != 0.0 and heatwaves[i][j][t-1] == 0.0:
                    temp = 0
                    ind = t
                    while heatwaves[i][j][ind] != 0.0:
                        temp += 1
                        ind += 1
                    count += temp - 2
            ans[i][j] = count * 0.38 # heatwave factor for increased length
    return ans
length_mortality = length_mortality(heatwaves)
    
def intensity_mortality(heatwaves,HItemps):
    #based on how a heatwave impacts the overall mean for the summer.
    ans = np.zeros((len(heatwaves),len(heatwaves[0])),dtype=np.float)
    for i in range(len(heatwaves)):
        for j in range(len(heatwaves[0])):
            for t in range(1,len(heatwaves[0][0])):
                if heatwaves[i][j][t] != 0.0 and heatwaves[i][j][t-1] == 0.0:
                    ind = t
                    while heatwaves[i][j][ind] != 0.0:
                        ind +=1
                    temps1 = HItemps[i][j][:t]
                    avg1 = sum(temps1)/len(temps1)
                    temps2 = HItemps[i][j][:ind+1]
                    avg2 = sum(temps2)/len(temps2)
                    CIA = avg2 - avg1
                    ans[i][j] = 2.49 * CIA # heatwave factor for increased intensity
    return ans
intensity_mortality = intensity_mortality(heatwaves,HItemps)

#create a funtion that is the overall change in mortality over the season
def overall_mortality(intensity,length, timing):
    ans = np.zeros_like(intensity)
    for i in range(len(intensity)):
        for j in range(len(intensity[0])):
            ans [i][j] = intensity[i][j] + timing[i][j] + length[i][j]
    return ans
    
overall_mortality = overall_mortality(intensity_mortality,length_mortality, timing_mortality)
    


#create netcdf to be used to display results in Canopy
ncOUTfile = Dataset("practice.nc", "a", format="NETCDF4") #change nameof outfile for each run
lon = ncOUTfile.createDimension("lon", len(lons))
lat = ncOUTfile.createDimension("lat", len(lats))
longitudes = ncOUTfile.createVariable("lon","f4",("lon",))
latitudes = ncOUTfile.createVariable("lat","f4",("lat",))
longitudes.units = "degrees East"
latitudes.units = "degrees North"
longitudes[:] = lons
latitudes[:] = lats
agrp = ncOUTfile.createGroup("analyses")
timing = agrp.createDimension("timing",None)
length = agrp.createDimension("length",None)
intensity = agrp.createDimension("intensity",None)
overall = agrp.createDimension("overall",None)
timings = agrp.createVariable("lon","f4",("lon",))
lengths = agrp.createVariable("lat","f4",("lat",))
intensities = agrp.createVariable("lon","f4",("lon",))
overalls = agrp.createVariable("lat","f4",("lat",))
timing.units = "percent increase in mortality"
length.units = "percent increase in mortality"
intensity.units = "percent increase in mortality"
overall.units = "percent increase in mortality"  
timings [:] = timing_mortality
lengths [:] = length_mortality
intensities [:] = intensity_mortality
overalls [:] = overall_mortality
ncOUTfile.close()
print "DONE"