import numpy as np
import pandas as pd
from geopy import distance

wells  = pd.read_csv('data/InjectionWells_w_geology.csv', parse_dates = ['Approval Date'])
wells[['LAT', 'LONG']] = wells[['LAT','LONG']].replace(0, np.NaN)
wells = wells.dropna(subset=['LONG', 'LAT'])

quakes = pd.read_csv('data/okQuakes_w_geology.csv', parse_dates = ['time'])
quakes['time'] = quakes['time'].dt.tz_localize(None)

# wells_sub = wells.loc[1:200,]
# #quakes_sub = quakes.loc[1:200,]
# #quakes_sub = quakes.loc[1:200, ]
# quakes_sub = quakes.tail(200)


columns_I_want = ['WellType', 'Approval Date', 'County', 'PSI', 'BBLS', 'ZONE',
                'UNIT_NAME', 'AGE_MIN', 'AGE_MAX', 'MAJOR1', 'MAJOR2', 'MAJOR3',
                'GENERALIZE']

for i, quake in quakes.iterrows():
    if i in np.arange(0,len(quakes), 500):
        print('Itterating over the {}th row'.format(i))
    active_wells = wells.loc[wells['Approval Date'] < quake.time, ].reset_index()
    distance_vector = [distance.distance(pair, (quake.latitude, quake.longitude)).km for pair in active_wells[['LAT','LONG']].values]
    quake.at['WellType'] = active_wells.at[np.argmin(distance_vector), 'WellType']
    quake.at['Approval Date'] = active_wells.at[np.argmin(distance_vector), 'Approval Date']
    quake.at['County'] = active_wells.at[np.argmin(distance_vector), 'County']
    quake.at['PSI'] = active_wells.at[np.argmin(distance_vector), 'PSI']
    quake.at['BBLS'] = active_wells.at[np.argmin(distance_vector), 'BBLS']
    quake.at['ZONE'] = active_wells.at[np.argmin(distance_vector), 'ZONE']
    quake.at['Well_UNIT_NAME'] = active_wells.at[np.argmin(distance_vector), 'UNIT_NAME']
    quake.at['Well_AGE_MIN'] = active_wells.at[np.argmin(distance_vector), 'AGE_MIN']
    quake.at['Well_AGE_MAX'] = active_wells.at[np.argmin(distance_vector), 'AGE_MAX']
    quake.at['Well_MAJOR1'] = active_wells.at[np.argmin(distance_vector), 'MAJOR1']
    quake.at['Well_MAJOR2'] = active_wells.at[np.argmin(distance_vector), 'MAJOR2']
    quake.at['Well_MAJOR3'] = active_wells.at[np.argmin(distance_vector), 'MAJOR3']
    quake.at['Well_GENERALIZE'] = active_wells.at[np.argmin(distance_vector), 'GENERALIZE']
