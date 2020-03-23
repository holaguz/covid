import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as pyp
import sys


if len(sys.argv) > 1:
    country = sys.argv[1]
else:
    country = "argentina"

if country == "argentina":
    base_address = "./"
    confirmed = pd.read_excel(base_address + "confirmed.xlsx")
    deaths = pd.read_excel(base_address + "deaths.xlsx")
    recovered = pd.read_excel(base_address + "recovered.xlsx")
else:
    base_address = "https://api.covid19api.com/total/dayone/country/"
    confirmed = pd.read_json(base_address + country + "/status/confirmed")
    confirmed.set_index("Date", inplace=True)
    deaths = pd.read_json(base_address + country + "/status/deaths")
    deaths.set_index("Date", inplace=True)
    recovered = pd.read_json(base_address + country + "/status/recovered")
    recovered.set_index("Date", inplace=True)


if confirmed.empty: raise Exception('No hay datos rey')

any_dead = True
if deaths.empty: any_dead = False
any_recovered = True
if recovered.empty: any_recovered = False

print(confirmed)
print(deaths)
print(recovered)

active_cases = confirmed.copy()
if any_dead:
    active_cases['Cases'] = active_cases['Cases'] - deaths['Cases']
if any_recovered:
    active_cases['Cases'] = active_cases['Cases'] - recovered['Cases']

N = 44E6


susceptible = confirmed.copy()
susceptible.Cases = N - susceptible.Cases

infected = active_cases.fillna(confirmed)

recovered.Cases = (recovered.Cases + deaths.Cases).fillna(recovered.Cases)

print(susceptible['Cases'].tolist())
print(infected['Cases'].tolist())
print(recovered['Cases'].tolist())
