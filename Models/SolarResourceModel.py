import numpy as np
import math
import urllib.request
import json
from types import SimpleNamespace
from Constants import Declination


def model(lat, lon):
    declinations_list = Declination.get_declination_list()
    hourly_angles_of_sunset = get_hourly_angle_of_the_sunset(int(lat), declinations_list)
    hours_with_sunlight_list = get_hours_with_sunlight_list(hourly_angles_of_sunset)
    coldest_day_of_year = hours_with_sunlight_list.index(min(hours_with_sunlight_list))
    total_hourly_radiation = get_total_hourly_radiation(lat, lon, coldest_day_of_year,
                                                        hourly_angles_of_sunset, hours_with_sunlight_list)

    return coldest_day_of_year, total_hourly_radiation, hours_with_sunlight_list


def get_hourly_angle_of_the_sunset(latitude, declinations_list):
    hourly_angle_of_sunset_list = []
    for declination in declinations_list:
        hourly_angle_of_sunset_list.append((math.acos((-math.tan(math.radians(latitude))
                                                       * (math.tan(math.radians(declination)))))))
    return hourly_angle_of_sunset_list


def get_hours_with_sunlight_list(hourly_angle_of_sunset_list):
    hours_with_sunlight_list = []
    for hourly_angle_of_sunset in hourly_angle_of_sunset_list:
        hours_with_sunlight_list.append((2 / 15) * math.degrees(hourly_angle_of_sunset))
    return hours_with_sunlight_list


def get_total_hourly_radiation(lat, long, coldest_day_of_year, hourly_angles_of_sunset, hours_with_sunlight_list):
    angle = hourly_angles_of_sunset[coldest_day_of_year]

    daily_extraterrestrial_irradiation = get_daily_extraterrestrial_irradiation(int(lat), coldest_day_of_year, angle)
    average_daily_extraterrestrial_irradiation = get_average_daily_extraterrestrial_irradiation(
        daily_extraterrestrial_irradiation, hours_with_sunlight_list, coldest_day_of_year, lat, long)

    c = 0.409 + 0.5016 * math.sin(angle - math.radians(60))
    d = 0.6609 - 0.4767 * math.sin(angle - math.radians(60))

    hourly_angle_of_sun_list = []
    total_hourly_radiation_list = []

    for hour in range(0, 24):
        angle = (hour - 12) * 15
        hourly_angle_of_sun_list.append(angle)

    for hourly_angle_of_sun in hourly_angle_of_sun_list:
        x = (0.1308997 * (c + d * math.cos(math.radians(hourly_angle_of_sun))))
        y = (math.cos(math.radians(hourly_angle_of_sun)) - math.cos(hourly_angles_of_sunset[coldest_day_of_year]))
        z = (math.sin(hourly_angles_of_sunset[coldest_day_of_year]) - (hourly_angles_of_sunset[coldest_day_of_year])
             * math.cos(hourly_angles_of_sunset[coldest_day_of_year]))

        total_hourly_radiation_list.append(average_daily_extraterrestrial_irradiation * x * (y / z))

    for i in range(0, 24):
        if 6 < i < 18:
            if total_hourly_radiation_list[i] < 0:
                total_hourly_radiation_list[i] = 0
        else:
            total_hourly_radiation_list[i] = 0

    return total_hourly_radiation_list


def get_daily_extraterrestrial_irradiation(latitude, N, angle):
    declination_list = Declination.get_declination_list()

    extraterrestrial_irradiation = (
            10443.1107 * (1 + 0.033 * math.cos(math.radians(0.98630137 * N))) * ((math.cos(math.radians(latitude))
                                                                                  * math.cos(
                math.radians(declination_list[N - 1])) * math.sin(angle)) + (0.01745329 *
                                                                             math.degrees(angle)) * math.sin(
        math.radians(latitude)) *
                                                                                 math.sin(math.radians(
                                                                                     declination_list[N - 1]))))
    return extraterrestrial_irradiation


def get_average_daily_extraterrestrial_irradiation(daily_extraterrestrial_irradiation, hours_with_sunlight_list,
                                                   n, lat, long):
    try:
        x = get_data_from_solar_atlas(lat, long)

        if hasattr(x.annual.data, 'GHI'):
            average_hours_of_month = (x.annual.data.GHI / 365)
        else:
            average_hours_of_month = 3

        N = get_average_daily_duration_of_month(hours_with_sunlight_list)
        a = average_hours_of_month / N

        average_daily_extraterrestrial_irradiation = daily_extraterrestrial_irradiation * (
                0.16 + 0.87 * a - 0.61 * math.pow(a, 2) + 0.34 * math.pow(a, 3))
        return average_daily_extraterrestrial_irradiation
    except:
        return 0


def get_data_from_solar_atlas(lat, long):
    try:
        contents = urllib.request.urlopen(
            "https://api.globalsolaratlas.info/data/lta?loc=" + str(lat) + ',' + str(long)).read()
        return json.loads(contents, object_hook=lambda d: SimpleNamespace(**d))
    except:
        print("Problema ao consultar Global Solar Atlas")
        return {}


def get_average_daily_duration_of_month(hours_with_sunlight_list):
    n = hours_with_sunlight_list.index(min(hours_with_sunlight_list))

    date = get_date_by_day_number(n)
    a = date[0]
    b = date[1]
    list_of_hours = hours_with_sunlight_list[a:b + 1]
    average = np.mean(list_of_hours)

    return average


def get_date_by_day_number(day_number):
    month = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October',
             'November', 'December']

    number_of_days_by_month = [31, 59, 90, 120, 151, 181, 212, 243, 273, 304, 334, 365]
    date = []

    for value in number_of_days_by_month:
        if value >= day_number:
            if value > 31:
                date.append(number_of_days_by_month[number_of_days_by_month.index(value) - 1])
                date.append(number_of_days_by_month[number_of_days_by_month.index(value)])
                date.append((day_number - number_of_days_by_month[number_of_days_by_month.index(value) - 1]))
            else:
                date.append(1)
                date.append(number_of_days_by_month[number_of_days_by_month.index(value)])
                date.append(day_number)

            date.append(month[number_of_days_by_month.index(value)])

            return date


def get_elevation(lat, long):
    try:
        x = get_data_from_solar_atlas(lat, long)

        if hasattr(x.annual.data, 'ELE'):
            return x.annual.data.ELE
        else:
            return 0
    except:
        return 0
