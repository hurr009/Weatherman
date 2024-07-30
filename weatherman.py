from statistics import mean
import argparse
import datetime
import glob
import csv

class WeatherRecord:
    def __init__(self, row):
        raw_date = row.get("PKT") or row.get("PKST")
        self.date = datetime.datetime.strptime(raw_date, "%Y-%m-%d")
        self.maxtemp =  row["Max TemperatureC"] and int(row["Max TemperatureC"])
        self.mintemp = row["Min TemperatureC"] and int(row["Min TemperatureC"])
        self.maxhumidity = row["Max Humidity"] and int(row["Max Humidity"])
        self.meanhumidity = row[" Mean Humidity"] and int(row[" Mean Humidity"])


def valid_date(s: str):
    try:
        return datetime.datetime.strptime(s, "%Y/%m")
    except ValueError:
        raise argparse.ArgumentTypeError(f"not a valid date: {s!r}")


def get_readings(cmd_args):
    def is_valid_record(record):
       return all([record.get('Max TemperatureC'), record.get('Min TemperatureC'), record.get('Max Humidity')])
  
    weather_record = []

    for weather_file in glob.glob(rf'{cmd_args.path}\*.txt'):
        with open(weather_file) as filename:
            weather_readings = csv.DictReader(filename, delimiter=",")

            for row in weather_readings:
                if is_valid_record(row):
                    weather_record.append(WeatherRecord(row))

    return weather_record


def find_extremes(records):
   return max(records, key=lambda x: x.maxtemp), min(records, key=lambda x: x.mintemp), max(records, key=lambda x: x.maxhumidity)


def find_average(w_records):
    def get_avg(key):
        return mean([getattr(r, key) for r in w_records if getattr(r, key)])

    return get_avg("maxtemp"), get_avg("mintemp"), get_avg("meanhumidity")


def display_extremes(maxtemp_day, mintemp_day, maxhumid_day):
    print("The max temprature is:", maxtemp_day.maxtemp, "on", maxtemp_day.date)
    print("The min temprature is:", mintemp_day.mintemp, "on", mintemp_day.date)
    print("The most humid day is:", maxhumid_day.maxhumidity, "on", maxhumid_day.date)


def display_average(avg_max, avg_min, avg_mean_humidity):
    print("The avg max temprature is:", avg_max)
    print("The avg min temprature is:", avg_min)
    print("The avg humidity is:", avg_mean_humidity) 


def make_chart(result):
    for index, day in enumerate(result, 1):
        print(f"{index} :\n{"+" * day.maxtemp}C\n{"-" * day.mintemp}C")
        

def get_cmdline_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("path", help="path to weather files")
    parser.add_argument("-e", "--year", help="Insert year to see its weather extremes", nargs="+")
    parser.add_argument("-a", "--date1", type=valid_date, help="Insert year with its month to see its weather extremes", nargs="+")
    parser.add_argument("-c", "--date2", type=valid_date, help="Insert year with its month to see its bar chart", nargs="+")
    return parser.parse_args()
    

def calculate_data(cmd_args, weather_records):
    def get_records_by_date(target_year, target_month=None):
        target_months = [target_month] if target_month else list(range(1, 13))
        return [l for l in weather_records if l.date.year==target_year and l.date.month in target_months]

    for raw_year in cmd_args.year or []:
        target_records = get_records_by_date(int(raw_year))
        maxtemp_day, mintemp_day, maxhumid_day = find_extremes(target_records)
        display_extremes(maxtemp_day, mintemp_day, maxhumid_day)

    for arg in cmd_args.date1 or []:
        target_records = get_records_by_date(arg.year, arg.month)
        avg_max, avg_min, avg_mean_humidity = find_average(target_records)
        display_average(avg_max, avg_min, avg_mean_humidity)

    for arg in cmd_args.date2 or []:
        target_records = get_records_by_date(arg.year, arg.month)
        make_chart(target_records)


def main():
    cmd_args = get_cmdline_arguments()
    weather_records = get_readings(cmd_args)
    calculate_data(cmd_args, weather_records)


if __name__ == "__main__":
    main()
