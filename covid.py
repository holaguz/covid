import sys
import datetime
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as pp

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
else:
	deaths.set_index("Date", inplace=True)
   
any_recovered = True
if recovered.empty:
    any_recovered = False
else:
	recovered.set_index("Date", inplace=True)


active_cases = confirmed.copy()
if any_dead:
    active_cases['Cases'] = active_cases['Cases'] - deaths['Cases']
if any_recovered:
    active_cases['Cases'] = active_cases['Cases'] - recovered['Cases']

start_date = '2020-03-08'

active_cases = active_cases.fillna(confirmed)
new_cases = confirmed['Cases'].diff().copy()

active_cases = active_cases[active_cases.index >= start_date]
new_cases = new_cases[new_cases.index >= start_date]

duplication_time = int(round(confirmed['5 days'].iloc[-1]))
print(duplication_time)

from matplotlib import ticker
from matplotlib import rcParams

rcParams['font.sans-serif'] = 'BentonSans-Book'
rcParams['text.color'] = '#eeeeee'

rcParams['figure.facecolor'] = '#222831'
rcParams['savefig.facecolor'] = '#222831'

rcParams['patch.facecolor'] = '#222831'

rcParams['axes.facecolor'] = '#222831'
rcParams['axes.labelcolor'] = '#eeeeee'
rcParams['axes.edgecolor'] = '#eeeeee'

rcParams['xtick.color'] = '#eeeeee'
rcParams['ytick.color'] = '#eeeeee'

rcParams['grid.color'] = '#4F555F'

fig, ax1 = pp.subplots(1, 1, figsize=(12, 4), dpi=120)

fig.autofmt_xdate()


ax1.spines['left'].set_visible(False)
#ax1.spines['right'].set_visible(False)
ax1.spines['top'].set_visible(False)
#ax1.spines['bottom'].set_visible(False)

ax1.yaxis.grid(which="both", linewidth=.5, linestyle='-')
ax1.xaxis.grid(which="both", linewidth=.5, linestyle='-')

ax1.tick_params(which='both', direction='in')

ax1.set_ylabel("Numero de casos", fontsize=12)
ax1.set_ylim((1, 2.5*active_cases.Cases.max()))
ax1.yaxis.tick_right()


#ax1.yaxis.set_minor_locator(ticker.AutoMinorLocator(n=2))
#ax1.yaxis.set_minor_formatter(ticker.NullFormatter())


##### PLOTTING 

ax1.semilogy(active_cases.index, active_cases.Cases, linewidth=1, marker="o", markersize=3, color='#ff2e63', label="Casos activos", nonposy='clip')
ax1.semilogy(new_cases, linewidth=1, marker="o", markersize=3, color="#00adb5", label="Nuevos casos", nonposy='clip')
ax1.legend(loc='upper left')


ax1.xaxis.set_minor_locator(mpl.dates.DayLocator(interval=1))
ax1.xaxis.set_major_formatter(mpl.dates.DateFormatter('%d/%m'))

ax1.yaxis.set_minor_locator(ticker.LogLocator(base=10, subs=(0.1,0.5,0.2)))
ax1.yaxis.set_minor_formatter(ticker.EngFormatter())


ax1.yaxis.set_major_formatter(ticker.EngFormatter())


last_entry_text = "{} casos".format(active_cases.iloc[-1].Cases.astype('int32'))
last_entry_text_args = {'ha':'right',
			            'va':'bottom',
			            'textcoords':'offset points',
			            'xytext':(-4, -2),
			            'fontsize':'12',
			            'fontname':'BentonSans-Book',
			            'weight':'regular'}

ax1.annotate(last_entry_text, (active_cases.tail(1).index, active_cases.iloc[-1].Cases), **last_entry_text_args)

flavor_dict = {'date' : confirmed.iloc[-1].name.strftime("%d/%m/%Y"),
				'confirmed' : confirmed.iloc[-1].Cases.astype('int32'),
				'recovered' : 0 if recovered.empty else recovered.iloc[-1].Cases.astype('int32'),                             
				'dead' : 0 if deaths.empty else deaths.iloc[-1].Cases.astype('int32'),
				'new_cases' : new_cases.iloc[-1].astype('int32'),
				'duplication_time' : duplication_time}
flavor_text_args = {'ha':'left',
                    'va':'top',
                    'textcoords':'offset points',
                    'xytext':(0,-36),
                    'fontsize':'12',
                    'fontname':'BentonSans-Book',
                    'weight':'regular'}

flavor_text = "{} — {} casos en total — {} recuperados — {} fallecidos — {} nuevos casos — Tiempo de duplicación (5d) {} días".format(flavor_dict['date'],
                                                                                                 flavor_dict['confirmed'],
                                                                                                 flavor_dict['recovered'],
                                                                                                 flavor_dict['dead'],
                                                                                                 flavor_dict['new_cases'],#duplication_time = confirmed['']
                                                                                                 flavor_dict['duplication_time'])
xmin, xmax = ax1.get_xlim()

start_date = mpl.dates.date2num(datetime.date.fromisoformat(start_date))
ax1.set_xlim((start_date, xmax))
xmin, xmax = ax1.get_xlim()

ax1.annotate(flavor_text, (xmin, 1), **flavor_text_args)

print(flavor_text)

fig.tight_layout()

pp.savefig('test.png', Transparent=False)
fig.show()
fig.waitforbuttonpress(timeout=-1)
