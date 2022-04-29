import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import re
import datetime
from datetime import date
pd.options.mode.chained_assignment = None  # default='warn'

#5001 Medellín #2 569 007
#76001 Cali #2 445 281
#11 Bogotá


df = pd.read_csv('Casos_positivos_de_COVID-19_en_Colombia.csv')


city = df[df['Código DIVIPOLA municipio'] == "5,001"]
city = city.reset_index(level=0, drop=True)

pop=2569007

city['total_casos']=city.index+1

city.dtypes

time = city['fecha reporte web'].values

day=[]
month=[]
year=[]
d_time=[]

for date in time:
    date=re.split('[-: ]', date)
    d_day=int(date[2])
    day.append(d_day)
    d_month=int(date[1])
    month.append(d_month)
    d_year=int(date[0])
    year.append(d_year)
    d_time.append(datetime.date(d_year, d_month, d_day))
    
city['Date']=d_time

test=city.groupby('Date').count()
#test.sum()


start = min(city["Date"])
end = max(city["Date"])

seqDates = []

d = start
while d <= end:
    seqDates.append(d)
    d += datetime.timedelta(days=1)

dff=pd.DataFrame(seqDates)
dff.columns=['Date']
dff.dtypes

n_cases=[]

for row in dff['Date']:
    if row in city['Date'].values:
        x=(test[test.index == row])
        n_cases.append(x['ID de caso'][0])
    else:
        n_cases.append(0)

x_len=len(n_cases)
x_axis=np.linspace(0,x_len-1,x_len)

plt.plot(x_axis, n_cases, label='New cases')


# function to show the plot
#plt.xlim([350, 434])
#plt.ylim([0, 4000])
plt.legend()
plt.grid()
plt.savefig('DailyCases.png', dpi=600)
plt.show()


time=[]

for t in city['Fecha de recuperación']:
    if type(t) == str:
        time.append(t)
    else:
        time.append(city['Fecha de muerte'][len(time)])


day=[]
month=[]
year=[]
d_time=[]

for date in time:
    if type(date) == str:
        date=re.split('[-: ]', date)
        d_day=int(date[2])
        day.append(d_day)
        d_month=int(date[1])
        month.append(d_month)
        d_year=int(date[0])
        year.append(d_year)
        d_time.append(datetime.date(d_year, d_month, d_day))
    else:
        d_time.append('')
    
city['date_r']=d_time

test2=city.groupby('date_r').count()

n_recovered=[]

for row in dff['Date']:
    if row in city['date_r'].values:
        x=(test2[test2.index == row])
        n_recovered.append(x['ID de caso'][0])
    else:
        n_recovered.append(0)

x2_len=len(n_recovered)
x2_axis=np.linspace(0,x2_len-1,x2_len)

plt.plot(x2_axis, n_recovered, label='New recovered')
# function to show the plot
#plt.xlim([350, 434])
#plt.ylim([0, 500000])
plt.legend()
plt.show()

dff['New cases']=n_cases
dff['New recovered']=n_recovered

t_cases=[]
i=1

while i <= len(dff['New cases']):
    tot = dff.iloc[0:i, 1:2].sum()
    t_cases.append(tot[0])
    i=i+1

t_recovered=[]
i=1

while i <= len(dff['New recovered']):
    tot = dff.iloc[0:i, 2:3].sum()
    t_recovered.append(tot[0])
    i=i+1

t_susc=[]
i=0

while i < len(dff['New recovered']):
    t_susc.append(pop-t_cases[i])
    i=i+1
    
c_act=[]
i=0

while i < len(dff['New recovered']):
    c_act.append(t_cases[i]-t_recovered[i])
    i=i+1

dff['Total sucseptible']=t_susc
dff['Total cases']=t_cases
dff['Total recovered']=t_recovered
dff['Active cases']=c_act


test2.columns

Deaths=test2['Fecha de muerte']
Deaths.sum()




with pd.ExcelWriter(r'Data.xlsx') as writer:
    dff.to_excel(writer, sheet_name='City')

