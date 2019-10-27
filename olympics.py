import pandas as pd
import sqlite3
import numpy as np

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
        medals_by_sport = self.last_olympics_data
        medals_by_sport = medals_by_sport[~medals_by_sport.Medal.isnull()]
        medals_by_sport["unique_medals"] = medals_by_sport["Event"].astype(str)+" "+medals_by_sport["Medal"].astype(str)
        medals_by_sport = medals_by_sport.drop_duplicates("unique_medals")

        medals_by_sport = medals_by_sport.groupby(["Sport","Medal"]).count().reset_index().pivot("Sport","Medal","index").fillna(0)
        medals_by_sport["total"] = medals_by_sport.sum(1)
        medals_by_sport = medals_by_sport.sort_values("total",ascending=True)
        del medals_by_sport["total"]
        return medals_by_sport[["Gold","Silver","Bronze"]]

    def last_olympics_medals_by_athlete(self):
        medal_map = {'Gold':1,'Silver':2,'Bronze':3}
        medals_by_athlete = self.last_olympics_data[["Name","Sex","Height","Weight","Sport","Event","Medal"]]
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
        hist_data = self.historical_olympics_data
        hist_data = hist_data[~hist_data.Medal.isnull()]
        hist_data["unique_medals"] = hist_data["Event"].astype(str)+" "+hist_data["Medal"].astype(str)+" "+hist_data["Year"].astype(str)
        hist_data = hist_data.drop_duplicates("unique_medals")
        hist_data = hist_data.groupby(["Year","Medal"]).count().reset_index().pivot("Year","Medal","index").fillna(0)
        olympics_years = pd.DataFrame({'Year':range(1896,2020,4)})
        hist_data = olympics_years.merge(hist_data,on="Year",how="left").set_index("Year")
        return hist_data

    def historical_olympics_data_medals_per_year_by_sport(self,sport):
        hist_data = self.historical_olympics_data
        hist_data = hist_data[~hist_data.Medal.isnull()]
        hist_data["unique_medals"] = hist_data["Event"].astype(str)+" "+hist_data["Medal"].astype(str)+" "+hist_data["Year"].astype(str)
        hist_data = hist_data.drop_duplicates("unique_medals")
        hist_data = hist_data[hist_data.Sport==sport].groupby(["Year","Medal"]).count().reset_index().pivot("Year","Medal","index").fillna(0)
        olympics_years = pd.DataFrame({'Year':range(1896,2020,4)})
        hist_data = olympics_years.merge(hist_data,on="Year",how="left").set_index("Year")#["Medal"]
        return hist_data

    def top_sports_historically(self):
        hist_data = self.historical_olympics_data
        hist_data = hist_data[~hist_data.Medal.isnull()]
        hist_data["unique_medals"] = hist_data["Event"].astype(str)+" "+hist_data["Medal"].astype(str)+" "+hist_data["Year"].astype(str)
        hist_data = hist_data.drop_duplicates("unique_medals")
        hist_data = hist_data.groupby(["Sport","Medal"]).count().reset_index()\
        .pivot("Sport","Medal","unique_medals").fillna(0)#.sort_values("Gold",ascending=True).tail(10).plot(kind='barh',stacked=True)
        hist_data["total"] = hist_data.sum(1)
        hist_data = hist_data.sort_values("total",ascending=True)[["Bronze","Silver","Gold","total"]]
        del hist_data["total"]
        return hist_data.tail(20)

    def get_histogram(self,metric_val,_range,year_a,year_b,sex):

        hist_data = self.historical_olympics_data
        if sex!="Both":
            hist_data = hist_data[hist_data.Sex==sex]


        weight_height_year_a = hist_data[hist_data.Year==year_a][["Height","Weight","Age"]].dropna()
        weight_height_year_b = hist_data[hist_data.Year==year_b][["Height","Weight","Age"]].dropna()

        a = pd.DataFrame({year_a:weight_height_year_a[metric_val]}).reset_index().astype(int)
        b = pd.DataFrame({year_b:weight_height_year_b[metric_val]}).reset_index().astype(int)

        results_a = pd.cut(a[year_a],bins=_range).value_counts().sort_index()
        results_b = pd.cut(b[year_b],bins=_range).value_counts().sort_index()
        
        return results_a,results_b

    def get_pct_women_athletes_globally(self,year_a,year_b):
        return pd.read_sql("SELECT * FROM pct_women_global",con=conn,index_col="female_pct_bucket")[[year_a,year_b]]
