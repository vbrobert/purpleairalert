import requests
import json

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

def avgSet(inSet):
    total = 0
    for item in inSet:
        total += item
    return total / len(inSet)

r = requests.get('https://www.purpleair.com/json?show=18189')
rJSON = json.loads(r.text)
aqis = set()
for reading in rJSON['results']:
    pm25Reading = float(reading['PM2_5Value'])
    aqi = pm25ToAQI(pm25Reading)
    aqis.add(aqi)

avgAQI = round(avgSet(aqis))

if avgAQI >= 250:
    pass #Condition 1 met for alarm
