import streamlit as st
import pandas as pd
import numpy as np
from olympics import *
import matplotlib.pyplot as plt
import warnings
import math


warnings.simplefilter("ignore")
plt.style.use('fivethirtyeight')


MEDALS_COLOR_MAP = {'Gold':'#d4af37','Silver':'#aaa9ad','Bronze':'#cd7f32'}
MEDALS_COLUMN_MAP = {'Gold':1,'Silver':2,'Bronze':3}
NUMBER_TO_MEDALS_MAP = {1:'Gold',2:'Silver',3:'Bronze'}


#APP STARTS HERE

#CONTENT ON THE SIDE BAR
st.sidebar.title('Olympics Data')


#CONTENT ON THE CENTRAL PART OF THE PAGE
selected_year = st.sidebar.number_input('Select Competition Year',1896,2016,2016,step=4)
selected_country = st.sidebar.selectbox('Select Country',regions_list,index=197)

country = Country(selected_country)
df = country.last_olympics_data(selected_year)
country.historical_olympics_data()
SPORTS = country.historical_sports_list
st.title(df.City.unique()[0]+" "+str(selected_year))
st.title("Team: "+selected_country)

#FIRST PLOT
df = country.last_olympics_medals_by_sport().fillna(0).astype(int)
if len(df)<1:
	st.title("No Data for"+selected_country)

else:
	st.subheader('Medals Won by Sport')
	dct = country.last_olympics_info()
	if df.sum().sum()<10:
		for x in dct.keys():
			st.write(x,":",dct[x])
	else:

		df.columns = df.columns.map(MEDALS_COLUMN_MAP).sort_values()
		df.columns = df.columns.map(NUMBER_TO_MEDALS_MAP)

		df.plot(kind='barh',stacked=True,figsize=(8,5),color=[MEDALS_COLOR_MAP.get(x, '#333333') for x in df.columns])
		plt.tight_layout()
		st.pyplot()

#FIRST TABLE
st.subheader('Medals Won by Athlete')
medals_by_athlete = country.last_olympics_medals_by_athlete()

selected_sport_in_athletes_table = st.selectbox(label="Filter Sport", options=SPORTS,index=3)
if st.checkbox('Show Whole Dataset'):
	st.table(medals_by_athlete[medals_by_athlete.Sport==selected_sport_in_athletes_table].set_index("Name"))
else:
	st.table(medals_by_athlete[medals_by_athlete.Sport==selected_sport_in_athletes_table].set_index("Name").head(5))

#CHECKBOX: WHEN CHECKED SHOWS HISTORICAL INFORMATION FOR THE SELECTED COUNTRY AND THE OLYMPICS IN GENERAL
historical_metrics = st.sidebar.checkbox(label="Show Historical Metrics",value=False)
if historical_metrics==True:
	
	#HISTORICAL STATISTICS SECTION

	st.header("Historical Stats")
	st.subheader('Medals Won Over Time by '+selected_country)
	
	#SECOND PLOT
	plt.figure()
	df = country.historical_olympics_data_medals_per_year()
	df.columns = df.columns.map(MEDALS_COLUMN_MAP).sort_values()
	df.columns = df.columns.map(NUMBER_TO_MEDALS_MAP)
	df.plot(kind='bar', stacked=True,color =[MEDALS_COLOR_MAP.get(x, '#333333') for x in df.columns])
	plt.tight_layout()
	st.pyplot()
	
	#THIRD PLOT
	st.subheader('Medals By Sport Over Time by '+selected_country)
	selected_sport = st.selectbox(label="Select Sport", options=SPORTS,index=3)
	plt.figure()
	df = country.historical_olympics_data_medals_per_year_by_sport(selected_sport)
	df.columns = df.columns.map(MEDALS_COLUMN_MAP).sort_values()
	df.columns = df.columns.map(NUMBER_TO_MEDALS_MAP)

	df.plot(kind='bar', stacked=True,color = [MEDALS_COLOR_MAP.get(x, '#333333') for x in df.columns])
	plt.tight_layout()
	st.pyplot()
	
	#FOURTH PLOT
	st.subheader('Top 20 Sports Historically by '+selected_country+' by number of Medals')
	plt.figure()
	df = country.top_sports_historically()
	df.columns = df.columns.map(MEDALS_COLUMN_MAP).sort_values()
	df.columns = df.columns.map(NUMBER_TO_MEDALS_MAP)

	df.plot(kind='barh', stacked=True,color = [MEDALS_COLOR_MAP.get(x, '#333333') for x in df.columns])
	plt.tight_layout()
	st.pyplot()
	#FIFTH PLOT
	st.subheader('Top Countries by Sport Historically')
	plt.figure()
	selected_sport_2 = st.selectbox(label="Select a Sport", options=SPORTS,index=3)
	st.subheader(selected_sport_2+" Gold Medals won by Country since 1896")
	country.get_country_medals_by_sport_historically(selected_sport_2).sort_values(ascending=True).tail(20).plot(kind='barh',color='#d4af37')
	plt.tight_layout()
	st.pyplot()
	
	#SIXTH PLOT
	st.header("Athlete Stats")
	st.subheader('Compare Distribution of Athlete Metrics')

	year_a = st.number_input('First Year',1896,2016,1992,step=4)
	year_b = st.number_input('Second Year',1896,2016,2016,step=4)
	metric_val = st.selectbox(label="Select Metric", options=["Age","Height","Weight"],index=0)
	selected_sex = st.selectbox(label="Select Gender", options=["M","F","Both"],index=0)
	metric_ranges = {"Age":range(15,65,5),'Height':range(140,225,5),'Weight':range(40,125,5)}
	
	#SEVENTH PLOT
	plt.figure()
	histogram_charts = country.get_histogram(metric_val=metric_val,_range=metric_ranges[metric_val],year_a=year_a,year_b=year_b,sex=selected_sex)
	st.subheader(metric_val+" Distribution "+str(year_a)+" vs "+str(year_b)+"&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp"+"Country:"+selected_country)
	histogram_charts[0].plot(kind='bar',width=0.5,color='grey',legend=True)
	histogram_charts[1].plot(kind='bar',width=0.20,color='red',legend=True)
	plt.tight_layout()
	st.pyplot()

	
	#GLOBAL STATISTICS SECTION

	st.header("Global Stats")
	st.subheader("Women in the Olympics")
	year_from = st.slider(label="compare Years", min_value=1896, max_value=2016, value=1960, step=4)
	st.subheader("Number of Countries by % of Female Athletes")

	#EIGHTH PLOT
	plt.figure()
	country.get_pct_women_athletes_globally(str(year_from),str(selected_year)).plot(kind='bar')
	plt.tight_layout()
	st.pyplot()

	#NINETH PLOT
	st.subheader("Percentage of Female Athletes by Sport")
	list_of_sports = st.multiselect(label="Select Sports to Compare", options=SPORTS,default=["All","Cycling","Gymnastics"])
	country.get_pct_women_athletes_by_sport(list_of_sports).plot(kind='line')
	plt.tight_layout()
	st.pyplot()

	#TENTH PLOT
	SPORTS = country.historical_sports_list
	st.subheader("Compare Countries by Medals Won")
	selected_sport_in_comp_table = st.selectbox(label="Filter Sport", options=SPORTS,index=3,key='22')
	region_selection_list_in_comp_table = st.multiselect(label="Select Countries to Compare", options=regions_list.tolist(),default=["UK","United States"])
	country.country_medals(selected_sport_in_comp_table, region_selection_list_in_comp_table).plot(kind='bar')
	plt.tight_layout()
	st.pyplot()    