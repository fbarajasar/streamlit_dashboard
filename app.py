import streamlit as st
import pandas as pd
import numpy as np
from olympics import *
import matplotlib.pyplot as plt
import warnings
warnings.simplefilter("ignore")

plt.style.use('fivethirtyeight')
st.sidebar.title('Olympics Data')
app_mode = st.sidebar.checkbox(label="Switch Between Blog/App",value=True)

if app_mode==True:

	selected_year = st.sidebar.number_input('Select Competition Year',1896,2016,2016,step=4)
	selected_country = st.sidebar.selectbox('Select Country',regions_list,index=193)


	country = Country(selected_country)
	df = country.last_olympics_data(selected_year)

	country.historical_olympics_data()
	SPORTS = country.historical_sports_list


	st.title(df.City.unique()[0]+" "+str(selected_year))
	st.title("Team: "+selected_country)


	df = country.last_olympics_medals_by_sport().astype(int)
	if len(df)<1:
		st.title("No Data for"+selected_country)

	else:
		st.subheader('Medals Won by Sport')

		df.plot(kind='barh',stacked=True,figsize=(8,5))
		plt.tight_layout()
		st.pyplot()


	st.subheader('Medals Won by Athlete')
	medals_by_athlete = country.last_olympics_medals_by_athlete()

	selected_sport_in_athletes_table = st.selectbox(label="Filter Sport", options=SPORTS,index=3)
	if st.checkbox('Show Whole Dataset'):
		st.table(medals_by_athlete[medals_by_athlete.Sport==selected_sport_in_athletes_table].set_index("Name"))
	else:
		st.table(medals_by_athlete[medals_by_athlete.Sport==selected_sport_in_athletes_table].set_index("Name").head(5))
	#
	historical_metrics = st.sidebar.checkbox(label="Show Historical Metrics",value=True)
	if historical_metrics==True:
		st.header("Historical Stats")
		st.subheader('Medals Won Over Time by '+selected_country)

		plt.figure()
		country.historical_olympics_data_medals_per_year().plot(kind='bar', stacked=True)
		plt.tight_layout()
		st.pyplot()

		st.subheader('Medals By Sport Over Time by '+selected_country)
		selected_sport = st.selectbox(label="Select Sport", options=SPORTS,index=2)
		plt.figure()
		country.historical_olympics_data_medals_per_year_by_sport(selected_sport).plot(kind='bar', stacked=True)
		plt.tight_layout()
		st.pyplot()


		st.subheader('Top 20 Sports Historically by '+selected_country+' by number of Medals')
		plt.figure()
		country.top_sports_historically().plot(kind='barh', stacked=True)
		plt.tight_layout()
		st.pyplot()

		st.subheader('Top Countries by Sport Historically')
		plt.figure()
		selected_sport_2 = st.selectbox(label="Select a Sport", options=SPORTS,index=3)
		st.subheader(selected_sport_2+" Gold Medals won by Country since 1896")
		country.get_country_medals_by_sport_historically(selected_sport_2).sort_values(ascending=True).tail(20).plot(kind='barh',color='orange')
		plt.tight_layout()
		st.pyplot()
		#scatter plot height weight comparing years in different colors

		#ranking by discipline to which country is the first in each discipline
		st.header("Athlete Stats")
		st.subheader('Compare Distribution of Athlete Metrics')

		year_a = st.number_input('First Year',1896,2016,1992,step=4)
		year_b = st.number_input('Second Year',1896,2016,2016,step=4)
		metric_val = st.selectbox(label="Select Metric", options=["Age","Height","Weight"],index=0)
		selected_sex = st.selectbox(label="Select Gender", options=["M","F","Both"],index=0)
		metric_ranges = {"Age":range(15,65,5),'Height':range(140,225,5),'Weight':range(40,125,5)}

		plt.figure()
		histogram_charts = country.get_histogram(metric_val=metric_val,_range=metric_ranges[metric_val],year_a=year_a,year_b=year_b,sex=selected_sex)
		st.subheader(metric_val+" Distribution "+str(year_a)+" vs "+str(year_b)+"&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp&nbsp"+"Country:"+selected_country)
		histogram_charts[0].plot(kind='bar',width=0.5,color='grey',legend=True)
		histogram_charts[1].plot(kind='bar',width=0.20,color='red',legend=True)
		plt.tight_layout()
		st.pyplot()

global_metrics = st.sidebar.checkbox(label="Show Global Metrics",value=True)
if global_metrics==True:
	st.header("Global Stats")
	st.subheader("Women in the Olympics")
	year_from = st.slider(label="compare Years", min_value=1896, max_value=2016, value=1960, step=4)
	st.subheader("Number of Countries by % of Female Athletes")
	country.get_pct_women_athletes_globally(str(year_from),str(selected_year)).plot(kind='bar')
	plt.tight_layout()
	st.pyplot()

	st.subheader("Percentage of Female Athletes by Sport")
	list_of_sports = st.multiselect(label="Select Sports to Compare", options=SPORTS,default=["All","Cycling","Gymnastics"])
	country.get_pct_women_athletes_by_sport(list_of_sports).plot(kind='line')
	plt.tight_layout()
	st.pyplot()


elif app_mode==False:
	st.title("120 years of Olympic history: Athletes and Results")
	st.header("The Dataset")
	st.write("This is a historical dataset on the modern Olympic Games,\
	 including all the Games from Athens 1896 to Rio 2016.\
	 The data contains 271116 rows and 15 columns.\
	 Each row corresponds to an individual athlete competing in an individual Olympic event (athlete-events). ")
	#st.write("https://medium.com/@fbarajasar/visualizing-the-olympic-games-history-using-streamlit-fc1dbb6f480e")