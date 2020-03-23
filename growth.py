import pandas as pd
import numpy as np
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
	deaths = pd.read_json(base_address + country + "/status/deaths")
	recovered = pd.read_json(base_address + country + "/status/recovered")


if confirmed.empty: raise Exception('No hay datos rey')


confirmed.set_index("Date", inplace=True)

any_dead = True
if deaths.empty:
    any_dead = False

else: deaths.set_index("Date", inplace=True)
    
any_recovered = True
if recovered.empty:
    any_recovered = False

else: recovered.set_index("Date", inplace=True)


active_cases = confirmed.copy()
if any_dead:
    active_cases['Cases'] = active_cases['Cases'] - deaths['Cases']
if any_recovered:
    active_cases['Cases'] = active_cases['Cases'] - recovered['Cases']

active_cases = active_cases.fillna(confirmed)

growth_rate = active_cases.copy()
#growth_rate = (growth_rate.shift(periods=-1).Cases/growth_rate.Cases)#.fillna(0)
growth_rate = growth_rate.Cases/growth_rate.shift(periods=1).Cases#.fillna(0)


rate_ma = growth_rate * growth_rate.shift(periods=1) * growth_rate.shift(periods=2) * growth_rate.shift(periods=3) * growth_rate.shift(periods=4) 

print(rate_ma)

# In[57]:


from matplotlib import ticker

fig, ax1= pyp.subplots(1,1, figsize=(12,4), dpi=180)
fig.set_facecolor('white')
fig.autofmt_xdate()

ax1.xaxis_date()
ax1.spines['left'].set_visible(False)
ax1.spines['top'].set_visible(False)

ax1.yaxis.grid(color="gainsboro", linewidth=0.5, linestyle=(0, (5, 10)))
ax1.yaxis.tick_right()
ax1.set_yscale('log')
#ax1.set_xlim(confirmed.iloc[1].name, confirmed.iloc[-1].name)

#ax1.yaxis.set_major_locator(ticker.LogLocator(base=2, subs=(0.5,1.0,)))
ax1.yaxis.set_major_locator(ticker.MultipleLocator(base=0.25))
ax1.yaxis.set_major_formatter(ticker.ScalarFormatter())
ax1.yaxis.set_minor_formatter(ticker.ScalarFormatter())

#ax1.yaxis.set_minor_locator(ticker.LogLocator(base=2))


ax1.xaxis.set_major_locator(ticker.MaxNLocator(10))
ax1.xaxis.set_major_formatter(mpl.dates.DateFormatter('%d/%m'))


plot_params = {'marker' : "o",'linewidth' : 0.5, 'markersize':3, 'color' :"royalblue", 'label' : "c[n]/c[n-1]"}
ax1.plot(growth_rate.index, growth_rate.values, **plot_params)

fig.show()
fig.waitforbuttonpress(timeout=-1)

print(growth_rate)
