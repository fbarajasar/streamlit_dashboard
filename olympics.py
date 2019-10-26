import pandas as pd
import sqlite3
import numpy as np
#CONNECT TO DB
conn = sqlite3.connect("summer_olympics.db", check_same_thread=False)
regions = pd.read_csv("noc_regions.csv").set_index("region")["NOC"].to_dict()
regions_list = np.array(list(regions.keys()))
regions_list.sort()

class Country():
    
    def __init__(self,country):
        self.country = country
        self.noc = regions[country]        

        self.__db_conn = conn    

    

    def last_olympics_data(self,year):

        self.__sql_last_date_query = "SELECT * FROM data WHERE NOC='{}' AND Year = {}".format(self.noc,year)
        self.last_olympics_data =  pd.read_sql(self.__sql_last_date_query,self.__db_conn)
        return self.last_olympics_data
    
    def last_olympics_info(self):
        last_olympics_data_medals_won_count = self.last_olympics_data.Medal.count()
        last_olympics_data_gold_medals_won_count = self.last_olympics_data[self.last_olympics_data.Medal=='Gold'].count()[0]
        last_olympics_data_silver_medals_won_count = self.last_olympics_data[self.last_olympics_data.Medal=='Silver'].count()[0]
        last_olympics_data_bronze_medals_won_count = self.last_olympics_data[self.last_olympics_data.Medal=='Bronze'].count()[0]
        
        return {'medals_total':last_olympics_data_medals_won_count,
                'medals_gold':last_olympics_data_gold_medals_won_count,
                'medals_silver':last_olympics_data_silver_medals_won_count,
                'medals_bronze':last_olympics_data_bronze_medals_won_count}
    
    def last_olympics_medals_by_sport(self):
        medals_by_sport = self.last_olympics_data.groupby(["Sport","Medal"]).count().reset_index().pivot("Sport","Medal","index").fillna(0)
        medals_by_sport["total"] = medals_by_sport.sum(1)
        medals_by_sport = medals_by_sport.sort_values("total",ascending=True)
        del medals_by_sport["total"]
        return medals_by_sport

    def last_olympics_medals_by_athlete(self):
        medal_map = {'Gold':1,'Silver':2,'Bronze':3}
        medals_by_athlete = self.last_olympics_data[["Name","Sex","Height","Weight","Sport","Medal"]]
        medals_by_athlete["key"] = medals_by_athlete["Name"].astype(str)+medals_by_athlete["Sport"].astype(str)+medals_by_athlete["Medal"].astype(str)
        medals_by_athlete = medals_by_athlete.drop_duplicates("key")
        medals_by_athlete = medals_by_athlete[~medals_by_athlete.Medal.isnull()]
        medals_by_athlete["numeric_score"] = medals_by_athlete.Medal.map(medal_map)
        medals_by_athlete.sort_values("numeric_score",ascending=True,inplace=True)
        medals_by_athlete["new_index"] = range(len(medals_by_athlete))

        del medals_by_athlete["numeric_score"]
        del medals_by_athlete["key"]

        return medals_by_athlete.set_index("new_index")

    def historical_olympics_data(self):
        sql_historical_date_query = "SELECT * FROM data WHERE NOC='{}'".format(self.noc)
        self.historical_olympics_data =  pd.read_sql(sql_historical_date_query,self.__db_conn)
        self.historical_sports_list = self.historical_olympics_data.Sport.unique()
        self.historical_sports_list.sort()
        return self.historical_olympics_data

    def historical_olympics_data_medals_per_year(self):
        hist_data = self.historical_olympics_data.groupby(["Year","olympics"]).count()["Medal"].reset_index()
        olympics_years = pd.DataFrame({'Year':range(1896,2020,4)})
        hist_data = olympics_years.merge(hist_data,on="Year",how="left").set_index("Year")["Medal"]
        return hist_data

    def historical_olympics_data_medals_per_year_by_sport(self,sport):
        hist_data = self.historical_olympics_data[self.historical_olympics_data.Sport==sport].groupby(["Year","olympics"]).count()["Medal"].reset_index()
        olympics_years = pd.DataFrame({'Year':range(1896,2020,4)})
        hist_data = olympics_years.merge(hist_data,on="Year",how="left").set_index("Year")["Medal"]
        return hist_data