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
  