import os
import sys
import argparse
import datetime
import glob
import csv

class DayReport:
  def __str__(self):
    print(self.date)

  def __init__(self, date, maxtemp, meantemp, mintemp, dew, meandew, mindew, maxhumidity, meanhumidity, minhumidity, maxsealevel, meansealevel, minsealevel, maxvisibility, meanvisibility, minvisibility, maxwind, meanwind, maxgust, precipitaion, cloudcover, events, winddirdegrees):
    self.date = date
    self.maxtemp = maxtemp
    self.meantemp = meantemp
    self.mintemp = mintemp
    self.dew = dew
    self.meandew = meandew
    self.mindew = mindew
    self.maxhumidity = maxhumidity
    self.meanhumidity = meanhumidity
    self.minhumidity = minhumidity
    self.maxsealevel = maxsealevel
    self.meansealevel = meansealevel
    self.minsealevel = minsealevel
    self.maxvisibility = maxvisibility
    self.meanvisibility = meanvisibility
    self.minvisibility = minvisibility
    self.maxwind = maxwind
    self.meanwind = meanwind
    self.maxgust = maxgust
    self.precipitaion = precipitaion
    self.cloudcover = cloudcover
    self.events = events
    self.winddirdegrees = winddirdegrees
    
  

def populate_readings():
  dayslist = []
  dayscount = 0
  path = sys.argv[1]
  path += r"\*.txt"
  files = glob.glob(path)
  for csv_file in files:
    with open(csv_file) as file:
      reader = csv.DictReader(file, delimiter = ",")
      line_count = 0
      for row in reader:
        if("PKT" in row):
          l = row["PKT"].split('-')
          d = datetime.date(int(l[0]), int(l[1]), int(l[2]))
          dayslist.append(DayReport(d, row["Max TemperatureC"], row["Mean TemperatureC"], row["Min TemperatureC"], row["Dew PointC"], row["MeanDew PointC"], row["Min DewpointC"], row["Max Humidity"], row[" Mean Humidity"], row[" Min Humidity"], row[" Max Sea Level PressurehPa"], row[" Mean Sea Level PressurehPa"], row[" Min Sea Level PressurehPa"], row[" Max VisibilityKm"], row[" Mean VisibilityKm"], row[" Min VisibilitykM"], row[" Max Wind SpeedKm/h"], row[" Mean Wind SpeedKm/h"], row[" Max Gust SpeedKm/h"], row["Precipitationmm"], row[" CloudCover"], row[" Events"], row["WindDirDegrees"]))
        else:
          l1 = row["PKST"].split('-')
          d1 = datetime.date(int(l1[0]), int(l1[1]), int(l1[2]))
          dayslist.append(DayReport(d1, row["Max TemperatureC"], row["Mean TemperatureC"], row["Min TemperatureC"], row["Dew PointC"], row["MeanDew PointC"], row["Min DewpointC"], row["Max Humidity"], row[" Mean Humidity"], row[" Min Humidity"], row[" Max Sea Level PressurehPa"], row[" Mean Sea Level PressurehPa"], row[" Min Sea Level PressurehPa"], row[" Max VisibilityKm"], row[" Mean VisibilityKm"], row[" Min VisibilitykM"], row[" Max Wind SpeedKm/h"], row[" Mean Wind SpeedKm/h"], row[" Max Gust SpeedKm/h"], row["Precipitationmm"], row[" CloudCover"], row[" Events"], row["WindDirDegrees"]))
        dayscount += 1
        line_count += 1
  return dayslist

def finding_values1(list):
  maxtemp = -9999999
  mintemp = 9999999
  maxmeanhumidity = -9999999
  daycount = 0
  for day in list:
    if(day.maxtemp != ""):
      if(int(day.maxtemp) > maxtemp):
        maxtemp = int(day.maxtemp)
        maxtempday = daycount
    if(day.mintemp != ""):
      if(int(day.mintemp) < mintemp):
        mintemp = int(day.mintemp)
        mintempday = daycount
    if(day.meanhumidity != ""):
      if(int(day.meanhumidity) > maxmeanhumidity):
        maxmeanhumidity = int(day.meanhumidity)
        maxhumidday = daycount
    daycount += 1
  result = [list[maxtempday], list[mintempday], list[maxhumidday]]
  return result

def finding_values2(list):
  avgmaxtemp = 0
  avgmintemp = 0
  avgmaxmeanhumidity = 0
  daycount = 0
  for day in list:
    if(day.maxtemp != ""):
      avgmaxtemp += int(day.maxtemp)
    if(day.mintemp != ""):
      avgmintemp += int(day.mintemp)
    if(day.meanhumidity != ""):
      avgmaxmeanhumidity += int(day.meanhumidity)
    daycount += 1
  avgmaxtemp /= daycount
  avgmintemp /= daycount
  avgmaxmeanhumidity /= daycount
  result = [[avgmaxtemp], [avgmintemp], [avgmaxmeanhumidity]]
  return result


def display1(result):
  print("The max temprature is:", result[0].maxtemp, "on", result[0].date)
  print("The min temprature is:", result[1].mintemp, "on", result[1].date)
  print("The most humid day is:", result[2].meanhumidity, "on", result[2].date)

def display2(result):
  print("The avg max temprature is:", result[0])
  print("The avg min temprature is:", result[1])
  print("The avg humidity is:", result[2])  

def display3(result):
  daycount = 1
  for day in result:
    print(daycount, ":")
    count1 = 0
    count2 = 0
    if(day.maxtemp != ""):
      count1 = int(day.maxtemp)
    if(day.mintemp != ""):
      count2 = int(day.mintemp)
    if(count1 != 0):
      for i in range(count1):
        print("+", end = " ")
      print(count1, "C")
    if(count2 != 0):
      for i in range(count2):
        print("+", end = " ")
      print(count2, "C\n\n")
    daycount += 1
    

def parse(days_list):
  parser = argparse.ArgumentParser()
  parser.add_argument("path", type = str, help = "path to weather files")
  parser.add_argument("-e", "--year", type = int, help = "Insert year to see its weather extremes", nargs = "+")
  parser.add_argument("-a", "--date1", type = str, help = "Insert year with its month to see its weather extremes", nargs = "+")
  parser.add_argument("-c", "--date2", type = str, help = "Insert year with its month to see its bar chart", nargs = "+")
  args = parser.parse_args()
  temp = []
  i = 2
  loop_count = len(sys.argv) - 2
  loop_count /= 2
  while(loop_count != 0):
    if (sys.argv[i] == '-e'):
      y = int(sys.argv[i+1])
      for day in days_list:
        if(day.date.year == y):
          temp.append(day)
      result = finding_values1(temp)
      display1(result)
    if (sys.argv[i] == '-a'):
      a = sys.argv[i+1].split("/")
      tyear = int(a[0])
      tmonth = int(a[1])
      for day in days_list:
        if(day.date.year == tyear and day.date.month == tmonth):
          temp.append(day)
      result = finding_values2(temp)
      display2(result)
    if (sys.argv[i] == '-c'):
      a = sys.argv[i+1].split("/")
      tyear1 = int(a[0])
      tmonth1 = int(a[1])
      for day in days_list:
        if(day.date.year == tyear1 and day.date.month == tmonth1):
          temp.append(day)
      display3(temp)
    loop_count -= 1
    i += 2
    temp = []
    result = []

days_list = populate_readings()
parse(days_list)