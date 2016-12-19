#Import the numpy and pandas libraries
import numpy as np
import pandas as pd
import os

#Get the OS folder/directory path
data_path = os.path.join(os.path.dirname(__file__),os.pardir,'rawdata')

#Load the state abbreviations csv, which relates state names to their abbreviations
state_abbr = pd.read_csv(data_path+'/stateAbbr.csv')

#Load csv containing data from 300,000+ vehicles recorded by 2009 NHTS
veh = pd.read_csv(data_path+'/VEHV2PUB.CSV')

#Load csv containing population data from the 2010 Census
pop = pd.read_csv(data_path+'/populations.csv',thousands=',')

#Load csv containing number of automobiles registered in each state from FHWA
auto = pd.read_csv(data_path+'/StateMotorVehicleRegistration.csv',thousands=',')

#Create a subset dataframe with the fields of interest from the vehicle data
veh_sub = veh[['HOUSEID','HHSTATE','ANNMILES','BESTMILE','GSYRGAL']]

#Create a subset dataframe of the 2010 populations
pop_sub = pop[['STATE','Census']]
pop_sub = pop_sub[pop_sub['STATE'].str.startswith('.')]
pop_sub['STATE']=pop_sub['STATE'].str[1:]

#Create a subset dataframe of number of automobiles per state
#We are only interested in automobiles registered for private use
auto_sub = auto[['STATE','PRIVATEAUTO']]
auto_sub['STATE'] = auto_sub['STATE'].str.strip()

#Create the default dataframe for the gas consumption analysis by state
dat = np.array([state_abbr['STATEABBR'],np.zeros(51),np.zeros(51),np.zeros(51), \
        np.zeros(51),np.zeros(51),np.zeros(51),np.zeros(51),np.zeros(51),np.zeros(51)])
dat = np.transpose(dat)
state_df = pd.DataFrame(data=dat,columns=['STATEABBR','NUMCARS', \
                                'SUMMILE','AVGMILE','TOTALMILE','MILECAPITA',
                                'SUMGAS','AVGGAS','TOTALGAS','GASCAPITA'])

#Go through each row of cars and accrue the mileage and gas by state
for car in veh_sub.itertuples():
	state_df.loc[state_df['STATEABBR'] == car.HHSTATE,'SUMMILE'] += car.BESTMILE;
	state_df.loc[state_df['STATEABBR'] == car.HHSTATE,'NUMCARS'] += 1;
	state_df.loc[state_df['STATEABBR'] == car.HHSTATE,'SUMGAS'] += car.GSYRGAL;

#Merge the automobile, vehichle registration, and censue population data
merged = auto_sub.merge(state_abbr,left_on='STATE',right_on='STATE',how='inner')
merged = merged.merge(pop_sub,left_on='STATE',right_on='STATE',how='inner')
merged = merged.merge(state_df,left_on='STATEABBR',right_on='STATEABBR',how='inner')

#Calculate the average number of miles traveled and gas consumed in each state
merged['AVGMILE'] = merged['SUMMILE']/merged['NUMCARS']
merged['AVGGAS'] = merged['SUMGAS']/merged['NUMCARS']

#Calculate the total miles traveled and gas consumed in each state
merged['TOTALMILE'] = merged['SUMMILE']*(merged['PRIVATEAUTO']/merged['NUMCARS'])
merged['TOTALGAS'] = merged['SUMGAS']*(merged['PRIVATEAUTO']/merged['NUMCARS'])

#Calculate the number of miles traveled and gas consumed per capita in each state
merged['MILECAPITA'] = merged['TOTALMILE']/merged['Census']
merged['GASCAPITA'] = merged['TOTALGAS']/merged['Census']

#Save the results to a CSV
merged.to_csv(data_path+'/STATE_SUMMARY.CSV');
