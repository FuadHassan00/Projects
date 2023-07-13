import pprint
import requests
import csv
from datetime import datetime, timedelta
import numpy as np

header = ['City', 'Min 1', 'Max 1', 'Min 2', 'Max 2', 'Min 3', 'Max 3', 'Min 4', 'Max 4', 'Min Avg', 'Max Avg']

city = [\
    ['Bengaluru', 'India'], \
    ['Glasgow', 'Scotland'],\
    ['Gumi', 'South Korea'],\
    ['Lagos', 'Nigeria'],\
    ['Nanaimo', 'Canada'],\
    ['Niskayuna', 'New York'],\
    ['Nizhny Novgorod', 'Russia'],\
    ['Olongapo', 'Phillipines'],\
    ['Peshawar', 'Pakistan'],\
    ['Peterhead', 'Scotland'],\
    ['Quito', 'Ecuador'],\
    ['Simmern', 'Germany'],\
    ['Tainan', 'Taiwan'],\
    ['Tbilisi', 'Georgia'],\
    ['Vinh Long', 'Vietnam'],\
    ["Xi'an", 'China'],\
 ]

## Opening the csv to store value for each city

with open('temp.csv', 'w') as temp:
    print(*header, sep=',', file=temp)
    
    ## Looping through cities to output weather information for each city
    for i in city:
        api_key = '01403c6cdb7045862e6b373bd05357a7'
        URL = 'https://api.openweathermap.org/data/2.5/forecast?'
        URL = URL + 'q=' + i[0] + ',' + i[1] + '&units=metric&appid=' + api_key

        print(f'"{i[0]}, {i[1]}"', sep= ',', end=',', file=temp)

        response = requests.get(URL)
        if response.status_code == 200:  # Success
            data = response.json()

            printer = pprint.PrettyPrinter(width=80, compact=True)
            #printer.pprint(data['list'][0])
            

        else:  # Failure
            print('Error:', response.status_code)

        ## Grabbing the Date, Temp Min, Temp Max from the loop and appending it to the temp min and temp max empty list

        temp_min = []
        temp_max = []
        
        for date in data['list']:
            parsed_date = datetime.strptime(date['dt_txt'], '%Y-%m-%d %H:%M:%S')
            today = datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
            if parsed_date - today >= timedelta(days=1):
                temp_min.append(date['main']['temp_min'])
                temp_max.append(date['main']['temp_max'])
    
    ## Printing temp min aad temp max to the csv
        for index in range(0, 32, 8):
            temp1 = sorted(temp_min[index:index+8])[0]
            temp2 = sorted(temp_max[index:index+8], reverse=True)[0]
            
            print("{:.2f}".format(temp1),sep=',', end=',', file=temp)
            print("{:.2f}".format(temp2),sep=',', end=',', file=temp)
    
    ## Printing Min_Avg and Max_Avg from the for loop, appending it to the empty list and printing to the csv

        Min_Avg = []
        Max_Avg = []

        for avg in range(0,32,8):
            Min_Avg.append(np.sum(sorted(temp_min[avg:avg+8])[0] / 4))
            Max_Avg.append(np.sum(sorted(temp_max[avg:avg+8], reverse=True)[0] / 4))
        
        Min1 = round(sum(Min_Avg),2)
        Max1 = round(sum(Max_Avg),2)
        print("{:.2f}".format(Min1),sep=',', end=',', file=temp)
        print("{:.2f}".format(Max1),sep=',', end = '\n', file = temp)