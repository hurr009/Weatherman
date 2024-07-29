from statistics import mean
import argparse
import datetime
import glob
import csv


class DayReport:

  def __init__(self, row):
    self.date = datetime.datetime.strptime(row.get("PKT") or row.get("PKST"), "%Y-%m-%d")
    self.maxtemp =  row["Max TemperatureC"]
    self.mintemp = row["Min TemperatureC"]
    self.maxhumidity = row["Max Humidity"]
    self.meanhumidity = row[" Mean Humidity"]


def valid_date(s: str):
    try:
        return datetime.datetime.strptime(s, "%Y/%m")
    except ValueError:
        raise argparse.ArgumentTypeError(f"not a valid date: {s!r}")


def get_readings(parser):
  weather_record = []
  path = parser.path # Getting argument from agparse
  for weather_file in glob.glob(rf'{path}\*.txt'):
    with open(weather_file) as filename:
      weather_readings = csv.DictReader(filename, delimiter = ",")
      for row in weather_readings:
        weather_record.append(DayReport(row))

  return weather_record


def find_extremes(list):
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


def find_average(list):
  return mean([int(l.maxtemp) for l in list if l.maxtemp!=""]),\
        mean([int(l.mintemp) for l in list if l.mintemp!=""]),\
        mean([int(l.meanhumidity) for l in list if l.meanhumidity!=""])


def display_extremes(result):
  print("The max temprature is:", result[0].maxtemp, "on", result[0].date)
  print("The min temprature is:", result[1].mintemp, "on", result[1].date)
  print("The most humid day is:", result[2].meanhumidity, "on", result[2].date)


def display_average(avg_max, avg_min, avg_mean_humidity):
  print("The avg max temprature is:", avg_max)
  print("The avg min temprature is:", avg_min)
  print("The avg humidity is:", avg_mean_humidity) 

def make_chart(result):
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
    

def parse():
  parser = argparse.ArgumentParser()
  parser.add_argument("path", help="path to weather files")
  parser.add_argument("-e", "--year", help="Insert year to see its weather extremes", nargs = "+")
  parser.add_argument("-a", "--date1", type=valid_date, help="Insert year with its month to see its weather extremes", nargs = "+")
  parser.add_argument("-c", "--date2", type=valid_date, help="Insert year with its month to see its bar chart", nargs = "+")
  args = parser.parse_args()
  return args


def calculate_data(parser, days_list):  
  temp = []
  if parser.year is not None:
    for arg in parser.year:
      target_year = int(arg)
      for day in days_list:  
        if(day.date.year == target_year):
          temp.append(day)
      result = find_extremes(temp)
      display_extremes(result)
      temp = []
      result = []

  if parser.date1 is not None:
    for arg in parser.date1:
      for day in days_list:
        if(day.date.year == arg.year and day.date.month == arg.month):
          temp.append(day)
      avg_max, avg_min, avg_mean_humidity = find_average(temp)
      display_average(avg_max, avg_min, avg_mean_humidity)
      temp = []
      result = []

  if parser.date2 is not None:
    for arg in parser.date2:
      for day in days_list:
        if(day.date.year == arg.year and day.date.month == arg.month):
          temp.append(day)
      make_chart(temp)
      temp = []

parser = parse()
weather_record = get_readings(parser)
calculate_data(parser, weather_record)