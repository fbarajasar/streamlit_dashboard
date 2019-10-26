import streamlit as st
import pandas as pd
import numpy as np
from olympics import *
import seaborn
import matplotlib.pyplot as plt


plt.style.use('fivethirtyeight')
st.sidebar.title('Olympics Data')



selected_country = st.sidebar.selectbox('Select Country',regions_list,index=193)

selected_year = st.sidebar.number_input('Select Competition Year',1896,2016,2016,step=4)


country = Country(selected_country)
df = country.last_olympics_data(selected_year)


st.title(df.City.unique()[0]+" "+str(selected_year)+": "+selected_country)


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


if st.checkbox('Show Whole Dataset'):
	st.table(medals_by_athlete)
else:
	st.table(medals_by_athlete.head(5))
#
st.header("Historical Stats")
st.subheader('Medals Won Over Time by '+selected_country)
country.historical_olympics_data()
SPORTS = country.historical_sports_list
plt.figure()
country.historical_olympics_data_medals_per_year().plot(kind='area')
plt.tight_layout()
st.pyplot()

st.subheader('Medals By Sport Over Time by '+selected_country)
selected_sport = st.selectbox(label="Select Sport", options=SPORTS,index=2)
plt.figure()
country.historical_olympics_data_medals_per_year_by_sport(selected_sport).plot(kind='bar')
plt.tight_layout()
st.pyplot()
