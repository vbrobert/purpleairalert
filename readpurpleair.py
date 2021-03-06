import requests
import json
import argparse
import time

def pm25ToAQI(pm25):
    #AQI Formula per EPA: ((IndexHigh - IndexLow) / (concenstration high - concenstration low)) * (Concenstration - concenstration low) + index low 
    if pm25 > 350.5:
        return (99 / 149.9) * (pm25-350.5) + 401
    elif pm25 > 250.5:
        return (99 / 99.9) * (pm25-250.5) + 301
    elif pm25 > 150.5:
        return (99 / 99.9) * (pm25-150.5) + 201
    elif pm25 > 55.5:
        return (49 / 94.5) * (pm25-55.5) + 151
    elif pm25 > 35.5:
        return (49 / 19.9) * (pm25-35.5) + 101
    elif pm25 > 12.1:
        return (49 / 23.3) * (pm25-12.1) + 51
    elif pm25 >= 0:
        return (50 / 12) * pm25
    else:
        return False

class Station():
    def refresh(self):
        r = requests.get(self.url) #'https://www.purpleair.com/json?show=18189')
        rJSON = json.loads(r.text)
        total = 0
        for reading in rJSON['results']: #Some station has more than one reading
            total += float(reading['PM2_5Value'])
        self.pm25 = total / len(rJSON['results'])
        self.aqi = round(pm25ToAQI(self.pm25))
        
    def __init__(self, stationID):
        url = 'https://www.purpleair.com/json?show={}'.format(stationID)
        self.url = url
        self.refresh()

class Stations(): #Collection of station
    def __init__(self):
        self.stations = list()
        
    def update(self):
        for station in self.stations:
            station.refresh()

    def avgAQI(self):
        total = 0
        for station in self.stations:
            total += station.aqi
        return total / len(self.stations)
    def autoUpdate(self, t):
        while True:
            self.update()
            time.sleep(t)
    #Clean Outliers
    #Update interval


parser = argparse.ArgumentParser(description="Survery's the area's AQI on a specified interval")
parser.add_argument('-t', '--time', type=int,help='Set the number of seconds to wait before resampling stations.',default=60)
args = parser.parse_args()
print('Time to refresh in seconds:', args.time)




newStation = Stations()
newStation.stations.append(Station('18189')) #Cotati Sensor
newStation.stations.append(Station('18985')) #Cotati Sensor
newStation.autoUpdate(args.time)
