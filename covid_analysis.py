import numpy as np
import pandas as pd
import io
import requests
import matplotlib.pyplot as plt
import datetime
from pandas.io import gbq
import os
from fbprophet import Prophet

# set the starting time to calculate the eslapsing time
start_time = datetime.datetime.now()

"""## Create the DAILY DATA and LOAD it to the Datawarehouse"""

# Auto update data source from csv to dataframe - daily data in global

# previous_Date in string with format YYYY-MM-DD HH:MM:SS.ffffff
def process_daily_data(n):
    previous_Date = datetime.datetime.today() - datetime.timedelta(days=n)
    previous_Date = str(previous_Date)
    #print('The latest update of daily data is the current date: {} \nThe date which is named in the url, has the previous date: {}\n So I create the url with the previous date form'.format(datetime.datetime.today(), previous_Date))

    get_year = previous_Date[:4]
    get_month = previous_Date[5:7]
    get_day = previous_Date[8:10]

    # change into this format: MM-DD-YYYY
    date_right_format = get_month + '-' + get_day + '-' + get_year + '.csv'
    url_daily_source = 'https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_daily_reports/'
    url_daily_source_full = url_daily_source + date_right_format
    daily = requests.get(url_daily_source_full).content
    daily_data = pd.read_csv(io.StringIO(daily.decode('utf-8')))
    # even the new day has come, the date in the url is stil far away at least 1 or 2 days from the current day
    # But in case the updated data from JHU comes so late - over 2 days!
    # So I use the recursion here
    if str(daily_data) == 'Empty DataFrame\nColumns: [404: Not Found]\nIndex: []' :
        return process_daily_data(n+1)
    return daily_data, url_daily_source_full, get_month + '/' + get_day + '/' + get_year[2:]

daily_data, available_latest_url, date_format_in_dataset = process_daily_data(1)
list_daily_data_source = 'https://github.com/CSSEGISandData/COVID-19/tree/master/csse_covid_19_data/csse_covid_19_daily_reports'
print('Available latest url: {} \n which is in the list of this source: {}\n'.format(available_latest_url, list_daily_data_source))
print('date format in dataset - use for the query {}'.format(date_format_in_dataset))

# need to change the name of the dataframe
daily_data = daily_data.rename(columns = {'Case-Fatality_Ratio':"Case_Fatality_Ratio"})

daily_data.to_gbq(destination_table='covid19data.covid19dailydata', project_id='covid19ds', if_exists='replace')

query = '''SELECT * FROM `covid19ds.covid19data.covid19dailydata`
WHERE Country_Region = 'Vietnam'
'''

project_id='covid19ds'

daily_data_query1 = gbq.read_gbq(query, project_id)

daily_data_query1['Country_Region'].iloc[0]

"""## Create the TIME SERIES dataset and LOAD it to the Datawarehouse"""

# fix url
url_confirmed_global = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv"
url_death_global = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv"
url_recovered_global = "https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv"
confirmed = requests.get(url_confirmed_global).content
death = requests.get(url_death_global).content
recovered =requests.get(url_recovered_global).content
data_crfm = pd.read_csv(io.StringIO(confirmed.decode('utf-8')))
data_dead = pd.read_csv(io.StringIO(death.decode('utf-8')))
data_reco = pd.read_csv(io.StringIO(recovered.decode('utf-8')))
bar_chart_race_data = data_crfm

data_crfm.to_csv('test2.csv')

#What I am doing here is aloting the previous value to next date if the cumulative count is less on next date!
def modifier(x):
    return(x[0] if x[0]>x[1] else x[1])

def data_correctr(data):
    total_cols = data.shape[1]
    cols = data.columns
    for i in range(5,total_cols):
        data[cols[i]] = data[[cols[i-1], cols[i]]].apply(modifier, 1)
    return data

# df_t.rename(columns=df_t.iloc[0]).drop(df_t.index[0])

#getting corrected data set!
data_crfm_c = data_correctr(data_crfm)
data_dead_c = data_correctr(data_dead)
data_reco_c = data_correctr(data_reco)

total_cols = data_crfm_c.shape[1]

data_crfm_d = data_crfm_c.copy()
data_dead_d = data_dead_c.copy()
data_reco_d = data_reco_c.copy()

# this is done to calculate the percentage for every day (initalising day 1 to zero)
data_crfm_p = data_crfm_c.copy()
data_crfm_p.iloc[:,4] = 0
data_dead_p = data_dead_c.copy()
data_dead_p.iloc[:,4] = 0
data_reco_p = data_reco_c.copy()
data_reco_p.iloc[:,4] = 0


for i in range(5,total_cols):

    #converting cumulative to daily count
    data_crfm_d.iloc[:, i] = data_crfm_d.iloc[:, i] - data_crfm_c.iloc[:, i-1]
    data_dead_d.iloc[:, i] = data_dead_d.iloc[:, i] - data_dead_c.iloc[:, i-1]
    data_reco_d.iloc[:, i] = data_reco_d.iloc[:, i] - data_reco_c.iloc[:, i-1]

    #percentage change: I will store the previous day cumulative and apply percentage change later
    data_crfm_p.iloc[:, i] = data_crfm_c.iloc[:, i-1]
    data_dead_p.iloc[:, i] = data_dead_c.iloc[:, i-1]
    data_reco_p.iloc[:, i] = data_reco_c.iloc[:, i-1]

# Here I am storing previous day daily count I will need this to calculate percentage change metric: the 6 small box in the dashboard
data_crfm_dp = data_crfm_d.copy()
data_crfm_dp.iloc[:,4] = 0
data_dead_dp = data_dead_d.copy()
data_dead_dp.iloc[:,4] = 0
data_reco_dp = data_reco_d.copy()
data_reco_dp.iloc[:,4] = 0

for i in range(5,total_cols):
    #percentage change: I will store the previous day daily and apply percentage change later
    data_crfm_dp.iloc[:, i] = data_crfm_d.iloc[:, i-1]
    data_dead_dp.iloc[:, i] = data_dead_d.iloc[:, i-1]
    data_reco_dp.iloc[:, i] = data_reco_d.iloc[:, i-1]



# Here comes the melt funtion of pandas. One line and your columns turns into rows!
df_crfm = pd.melt(data_crfm_d, id_vars = ['Province/State', 'Country/Region', 'Lat', 'Long'], var_name = 'Time').rename(columns = {'value':"Daily_Confirmed"})



# continue with other columns and
# must rename for suitable with form of Google Big Query
df_dead = pd.melt(data_dead_d, id_vars = ['Province/State', 'Country/Region', 'Lat', 'Long'], var_name = 'Time').rename(columns = {'value':"Daily_Death"})
df_reco = pd.melt(data_reco_d, id_vars = ['Province/State', 'Country/Region', 'Lat', 'Long'], var_name = 'Time').rename(columns = {'value':"Daily_Recovered"})

df_crfm_c = pd.melt(data_crfm_c, id_vars = ['Province/State', 'Country/Region', 'Lat', 'Long'], var_name = 'Time').rename(columns = {'value':"Cum_Confirmed"})
df_dead_c = pd.melt(data_dead_c, id_vars = ['Province/State', 'Country/Region', 'Lat', 'Long'], var_name = 'Time').rename(columns = {'value':"Cum_Death"})
df_reco_c = pd.melt(data_reco_c, id_vars = ['Province/State', 'Country/Region', 'Lat', 'Long'], var_name = 'Time').rename(columns = {'value':"Cum_Recovered"})

df_crfm_p = pd.melt(data_crfm_p, id_vars = ['Province/State', 'Country/Region', 'Lat', 'Long'], var_name = 'Time').rename(columns = {'value':"PCum_Confirmed"})
df_dead_p = pd.melt(data_dead_p, id_vars = ['Province/State', 'Country/Region', 'Lat', 'Long'], var_name = 'Time').rename(columns = {'value':"PCum_Death"})
df_reco_p = pd.melt(data_reco_p, id_vars = ['Province/State', 'Country/Region', 'Lat', 'Long'], var_name = 'Time').rename(columns = {'value':"PCum_Recovered"})

df_crfm_dp = pd.melt(data_crfm_dp, id_vars = ['Province/State', 'Country/Region', 'Lat', 'Long'], var_name = 'Time').rename(columns = {'value':"dPCum_Confirmed"})
df_dead_dp = pd.melt(data_dead_dp, id_vars = ['Province/State', 'Country/Region', 'Lat', 'Long'], var_name = 'Time').rename(columns = {'value':"dPCum_Death"})
df_reco_dp = pd.melt(data_reco_dp, id_vars = ['Province/State', 'Country/Region', 'Lat', 'Long'], var_name = 'Time').rename(columns = {'value':"dPCum_Recovered"})

print(df_crfm.shape, df_dead.shape, df_reco.shape, df_crfm_c.shape, df_dead_c.shape, df_reco_c.shape, df_crfm_p.shape, df_dead_p.shape, df_reco_p.shape)

#Collecting the metric into 1 data frame
df = df_crfm.merge(df_dead[['Country/Region','Lat','Long', 'Time', 'Daily_Death']], how = 'left', on = ['Country/Region','Lat', 'Long', 'Time'])
df = df.merge(df_reco[['Country/Region','Lat','Long', 'Time', 'Daily_Recovered']], how = 'left', on = ['Country/Region','Lat', 'Long', 'Time'])

df = df.merge(df_crfm_c[['Country/Region','Lat','Long', 'Time', 'Cum_Confirmed']], how = 'left', on = ['Country/Region','Lat', 'Long', 'Time'])
df = df.merge(df_dead_c[['Country/Region','Lat','Long', 'Time', 'Cum_Death']], how = 'left', on = ['Country/Region','Lat', 'Long', 'Time'])
df = df.merge(df_reco_c[['Country/Region','Lat','Long', 'Time', 'Cum_Recovered']], how = 'left', on = ['Country/Region','Lat', 'Long', 'Time'])

df = df.merge(df_crfm_p[['Country/Region','Lat','Long', 'Time', 'PCum_Confirmed']], how = 'left', on = ['Country/Region','Lat', 'Long', 'Time'])
df = df.merge(df_dead_p[['Country/Region','Lat','Long', 'Time', 'PCum_Death']], how = 'left', on = ['Country/Region','Lat', 'Long', 'Time'])
df = df.merge(df_reco_p[['Country/Region','Lat','Long', 'Time', 'PCum_Recovered']], how = 'left', on = ['Country/Region','Lat', 'Long', 'Time'])

df = df.merge(df_crfm_dp[['Country/Region','Lat','Long', 'Time', 'dPCum_Confirmed']], how = 'left', on = ['Country/Region','Lat', 'Long', 'Time'])
df = df.merge(df_dead_dp[['Country/Region','Lat','Long', 'Time', 'dPCum_Death']], how = 'left', on = ['Country/Region','Lat', 'Long', 'Time'])
df = df.merge(df_reco_dp[['Country/Region','Lat','Long', 'Time', 'dPCum_Recovered']], how = 'left', on = ['Country/Region','Lat', 'Long', 'Time'])



#last datatype corrections before feeding to data studio
df['Lat_Long'] = df['Lat'].astype(str)+","+df['Long'].astype(str)

df['Death_Rate'] = ((df['Cum_Death'] *100) /df['Cum_Confirmed']).replace([np.inf, -np.inf], np.nan).fillna(0)
df['Recovered_Rate'] = ((df['Cum_Recovered'] *100) /df['Cum_Confirmed']).replace([np.inf, -np.inf], np.nan).fillna(0)

tsd = df.rename(columns = {'Country/Region':"Country_Region",
                           'Province/State':'Province_State',
                           'Cum_Confirmed':'acc_Confirmed',
                           'Cum_Death':'acc_Death',
                           'Cum_Recovered':'acc_Recovered',
                           'PCum_Confirmed':'pacc_confirmed',
                           'PCum_Death':'pacc_Death',
                           'PCum_Recovered':'pacc_Recovered',
                           'dPCum_Confirmed':'dpacc_Confirmed',
                           'dPCum_Death':'dpacc_Death',
                           'dPCum_Recovered':'dpacc_Recovered',

                          })




tsd[tsd['Country_Region'] == 'Vietnam'].tail(15).isnull()

tsd.to_gbq(destination_table='covid19data.covid19tsd', project_id='covid19ds', if_exists='replace')



"""## Create a new Table for the LATEST recovered & death rate

## Prepare data for the race bar chart
"""

query = '''SELECT Country_Region, SUM(Confirmed) as Total_Confirmed
FROM `covid19ds.covid19data.covid19dailydata`
GROUP BY Country_Region
ORDER BY Total_Confirmed DESC
LIMIT 10'''

# test another case: recovered >= 40k and <= 100000
query = '''SELECT Country_Region, SUM(Recovered) as Total_Recovered
FROM `covid19ds.covid19data.covid19dailydata`
WHERE Confirmed >= 40000 and Confirmed <=100000 and Country_Region != 'China'
GROUP BY Country_Region
ORDER BY Total_Recovered DESC
LIMIT 10'''

data_q = gbq.read_gbq(query, project_id)


# list the countries in data_q
data_q_list = list(data_q['Country_Region'])
# check
data_q_list[len(data_q_list)-1]

# get the value of the TOP 10 recovered
data_q_value = list(data_q['Total_Recovered'])
rank_10_cf = data_q_value[len(data_q_value)-1]
print('Country which is at 10th rank: {} with {} Recovered cases'.format(data_q_list[len(data_q_list)-1], rank_10_cf))
# change bar_chart_race_data above
bar_chart_race_data = data_reco
rank_1_10_cf = data_q_value[0]


# get the value of the TOP 10 confirmed
#data_q_value = list(data_q['Total_Confirmed'])
#rank_10_cf = data_q_value[len(data_q_value)-1]
#print('Country which is at 10th rank: {} with {} confirmed cases'.format(data_q_list[len(data_q_list)-1], rank_10_cf))

# create the right name of the final dimensions of the dataset - it's the latest updated day also!
form_d = int(date_format_in_dataset[0:2])
form_m = int(date_format_in_dataset[3:5])
condition_top10 = str(form_d) + '/' + str(form_m) + '/' + date_format_in_dataset[6:]


top_10_tsd = bar_chart_race_data[(bar_chart_race_data['Country/Region'] == data_q_list[0]) |
                                 (bar_chart_race_data['Country/Region'] == data_q_list[1]) |
                                 (bar_chart_race_data['Country/Region'] == data_q_list[2]) |
                                 (bar_chart_race_data['Country/Region'] == data_q_list[3]) |
                                 (bar_chart_race_data['Country/Region'] == data_q_list[4]) |
                                 (bar_chart_race_data['Country/Region'] == data_q_list[5]) |
                                 (bar_chart_race_data['Country/Region'] == data_q_list[6]) |
                                 (bar_chart_race_data['Country/Region'] == data_q_list[7]) |
                                 (bar_chart_race_data['Country/Region'] == data_q_list[8]) |
                                 (bar_chart_race_data['Country/Region'] == data_q_list[9])]

top_10_tsd.to_csv('test.csv')

# use the tsd dataframe

tsd[tsd['Country_Region'] == 'Vietnam']

"""## New features - [ad hoc analysis] Predict future with any metrics"""

# create model and make prediction:
def predict_viz(range_day):
    # interval 0.63 for Vietnam, another: 0.91
    m = Prophet(interval_width=0.63,daily_seasonality=True)
    m.fit(df_fbprophet)
    future = m.make_future_dataframe(periods = range_day)
    forecast = m.predict(future)

    fig, ax = plt.subplots(facecolor='#F3F3F3')
    #fig = plt.figure()
    #fig.patch.set_facecolor('#F3F3F3')

    fig_predict_1 = m.plot(forecast, xlabel = 'Date - predict the next {} days'.format(range_day), ylabel = chosen_metrics)
    fig_predict_2 = m.plot_components(forecast)

    fig_predict_1.savefig('result1.jpg', facecolor=fig.get_facecolor(), transparent=True)
    fig_predict_2.savefig('result2.jpg', facecolor=fig.get_facecolor(), transparent=True)
    return forecast

# function to create a dataset with countries and metrics you want to predicts!
# And transform to the right form for using fbProphet
def create_df_fbprophet(ct, metrics):
    df_fbprophet = tsd[tsd['Country_Region'] == ct]
    df_fbprophet = df_fbprophet[['Time', metrics]].rename(columns = {'Time':'ds', metrics:'y'})
    return df_fbprophet

# CHOOSE CT      0           1    2
list_ct = ['Vietnam', 'Finland', 'US']
# CHOOSE METRICS         0                1               2                 3
list_metrics = ['acc_Confirmed', 'Daily_Confirmed', 'Daily_Recovered', 'acc_Recovered']
# choose fix val - normaly VN 0 2, US 2 1
chosen_ct = list_ct[0]
chosen_metrics = list_metrics[2]

# use func
df_fbprophet = create_df_fbprophet(chosen_ct, chosen_metrics)

# df_fbprophet = df_fbprophet[int(len(df_fbprophet)/3):]


import numpy as np
df_fbprophet.isnull()

# show upper and lower limit of y value, choose the range of day wants to predict
# vietnam 14, US 45
range_day = 45
forecast = predict_viz(range_day)
# take the previous day
previous_day = 13
total_day = range_day + previous_day
forecast_df_tobq = forecast.tail(total_day)
forecast_df_tobq.to_gbq(destination_table='covid19data.testPredict', project_id='covid19ds', if_exists='replace')

time_elapsed = datetime.datetime.now() - start_time
print('Time eslapsed (hh:mm:ss.ms) {}'.format(time_elapsed))