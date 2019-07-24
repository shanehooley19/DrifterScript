#Drifter Smart RTL
#
#Python 2.7.16
#
#Created by Shane Hooley
#
# This code allows for an autonomous aquatic drone to
# drift along with currents, collecting data, and
# return home along the path it drifted along.

import sys
import time
import clr
import math
import MissionPlanner
clr.AddReference("MissionPlanner.Utilities")

#Gets the current GPS lat and long position and appends
#it to the LIFO stack
def setPos() :
    lat.append(cs.lat)
    lng.append(cs.lng)
    print(cs.lat)
    print(cs.lng)

def getPos() :
    return [cs.lat,cs.lng]

def setCurrentPos(currentPos) :
    lat.append(currentPos[0])
    lng.append(currentPos[1])

def peekPos() :
    holdLat = lat.pop()
    holdLng = lng.pop()
    lat.append(holdLat)
    lng.append(holdLng)
    return [holdLat,holdLng]

def popPos() :
    return [lat.pop(),lng.pop()]

def dist(thisPos) :
    comparePos = peekPos()
    deltaLat = comparePos[0] - thisPos[0]
    deltaLng = comparePos[1] - thisPos[1]
    dist = math.sqrt(deltaLat**2 + deltaLng**2)
    return dist

def degreesToRadians(degrees) :
  return degrees * math.pi / 180

def distance(lat1, lon1, lat2, lon2) :
  earthRadiusM = 6371000

  dLat = degreesToRadians(lat2-lat1)
  dLon = degreesToRadians(lon2-lon1)

  lat1 = degreesToRadians(lat1)
  lat2 = degreesToRadians(lat2)

  a = math.sin(dLat/2) * math.sin(dLat/2) + math.sin(dLon/2) * math.sin(dLon/2) * math.cos(lat1) * math.cos(lat2)
  c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
  return earthRadiusM * c
    
    
nextWPDist = 5     #Distance between new waypoints
timeoutTime = 2    #Time in minutes until timeout

lat = []
lng = []

print 'Starting Drifter Sequence'

modeChange = Script.ChangeMode('Hold')

if(modeChange == True) :
    print 'Hold Mode' 
else :
    print 'Error: Mode not changed!'

setPos()
timeoutTime = timeoutTime*60 + time.time()

while (True) :
    if(cs.DistToHome > 15) :
        print 'Geofence Reached!'
        break
    if(time.time() > timeoutTime) :
        print 'Timeout!'
        break
    currentPos = getPos()
    oldPos = peekPos()
    if(distance(currentPos[0],currentPos[1], oldPos[0], oldPos[1]) > nextWPDist) :
        setCurrentPos(currentPos)
        print 'Position Set'


print 'Returning to Home'
modeChange = Script.ChangeMode('Guided')

if (modeChange == True) :
    print 'Guided Mode, Returning to Launch'
else :
    print 'Error: Mode not changed!'

while (lat) :
    goToPos = popPos()
    item = MissionPlanner.Utilities.Locationwp()
    MissionPlanner.Utilities.Locationwp.lat.SetValue(item,goToPos[0])
    MissionPlanner.Utilities.Locationwp.lng.SetValue(item,goToPos[1])
    MAV.setGuidedModeWP(item)
    print 'Going to next position.'
    print distance(goToPos[0], goToPos[1], cs.lat, cs.lng)
    while(distance(goToPos[0], goToPos[1], cs.lat, cs.lng) > 1) :
        time.sleep(0.1)

print "Returned to Home"






