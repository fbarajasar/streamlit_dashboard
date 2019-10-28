import pandas as pd
import sqlite3

def open_csvs_and_merge():
    data = pd.read_csv(r"athlete_events.csv")
    regions = pd.read_csv(r"noc_regions.csv")
    data =  data.merge(regions,how='left',on='NOC')
    return data

def filter_by_season(data):
    return data[data.Season=='Summer']

def save_to_sql(data, conn):
    data.sort_values("NOC",ascending=True).to_sql(name = "data", con = conn,
     if_exists = "replace")
    

def clean_data_and_add_columns(data):
    medal_map = {'Gold':3,'Silver':2,'Bronze':1}
    data["medals_numeric"] = data["Medal"].map(medal_map)
    data["olympics"] = data["City"]+" "+data["Year"].astype(str)
    data.loc[data['olympics'] == "Stockholm 1956"] = "Melbourne 1956" 
    return data   


def create_sql_indices(conn):
    cursor = conn.cursor()
    sql = ("CREATE INDEX country ON data (NOC);")
    cursor.execute(sql)

    sql = ("CREATE INDEX year_index ON data (Year);")
    cursor.execute(sql)    
    



def get_female_athletes_pct_global_histogram(year):
    data = pd.read_sql("SELECT Year,Sex,region,ID FROM data WHERE Year={}".format(year),conn)
    male_vs_female_athletes = data.groupby(["region","Sex"]).count()["ID"].reset_index().pivot(index="region",columns="Sex",values="ID").fillna(0)#
    male_vs_female_athletes["total"] = male_vs_female_athletes.sum(1)
    for i in male_vs_female_athletes:
        male_vs_female_athletes[i] = (male_vs_female_athletes[i]/male_vs_female_athletes["total"])*100
    del male_vs_female_athletes["total"]
    male_vs_female_athletes["female_pct_bucket"] = pd.cut(male_vs_female_athletes["F"],bins=range(0,100,10))
    male_vs_female_athletes = male_vs_female_athletes.groupby("female_pct_bucket").count()["F"]
    male_vs_female_athletes.index = male_vs_female_athletes.index.astype(str).str.replace(", ","-")\
    .str.replace("]","%").str.replace("(","")
    return male_vs_female_athletes




def get_pct_of_female_athletes_by_sport():

    unique_sports = pd.read_sql("SELECT DISTINCT(Sport) FROM data",con=conn).Sport.unique()

    all_data = pd.DataFrame()
    for sport in unique_sports:    
        try:
            data = pd.read_sql("SELECT * FROM data WHERE Sport='{}'".format(sport),con=conn)
            women_men = data.groupby(["Year","Sex"]).count().reset_index().pivot(index="Year",columns="Sex",values="ID")
            women_men["total"] = women_men.sum(1)
            for i in women_men.columns:
                women_men[i] = (women_men[i]/women_men["total"])*100
            women_men = women_men[["F"]]
            women_men["Sport"] = sport
            all_data = all_data.append(women_men)        
        except:
            pass

    data = pd.read_sql("SELECT * FROM data".format(sport),con=conn)
    women_men = data.groupby(["Year","Sex"]).count().reset_index().pivot(index="Year",columns="Sex",values="ID")
    women_men["total"] = women_men.sum(1)
    for i in women_men.columns:
        women_men[i] = (women_men[i]/women_men["total"])*100
    women_men = women_men[["F"]]
    women_men["Sport"] = "All"
    all_data = all_data.append(women_men)
    all_data = all_data.pivot(columns="Sport",values="F")
    all_data.to_sql(name="pct_of_female_athletes_by_sport",con=conn,if_exists = "replace")


def get_country_medals_by_sport_historically():
    data = pd.read_sql("SELECT * FROM data",con=conn)
    data["unique_medals"] = data["Event"].astype(str)+" "+data["Medal"].astype(str)+" "+data["Year"].astype(str)
    data = data.drop_duplicates("unique_medals")
    data = data[data.Medal=="Gold"]
    country_medals_by_sport_historically = data.groupby(["Sport","region"]).count()["Medal"].reset_index()\
    .pivot(index="region",columns="Sport",values="Medal").to_sql(name="country_medals_by_sport_historically",con=conn,if_exists = "replace")



if __name__ == '__main__':
    #CREATE CONNECTION TO DB
    conn = sqlite3.connect("summer_olympics.db")
    #OPEN CSVS AND MERGE THEM
    data = open_csvs_and_merge()
    #CLEAN DATA
    data = clean_data_and_add_columns(data)
    #USE ONLY SUMMER OLYMPICS DATA
    data = filter_by_season(data)
    #SAVE DATA TO SQLITE3 DB
    save_to_sql(data, conn)
    #CREATE INDEX
    create_sql_indices(conn)
    #CREATE PCT WOMEN TABLE
    all_data = pd.DataFrame()
    for i in range(1896,2020,4):
        try:
            data = pd.DataFrame({"percentage":get_female_athletes_pct_global_histogram(i),"year":i})
            all_data = all_data.append(data)
        except:
            pass

    table_of_years_vs_perceantages_of_women = all_data.reset_index()\
    .pivot(index="female_pct_bucket",columns="year",values="percentage").to_sql(name = "pct_women_global", con = conn,
     if_exists = "replace")

    #CREATE PCT FEMALE ATHLETES BY SPORT TABLE
    get_pct_of_female_athletes_by_sport()    
    ##########################
    #CREATE medals_by_sport_historically TABLE
    get_country_medals_by_sport_historically()