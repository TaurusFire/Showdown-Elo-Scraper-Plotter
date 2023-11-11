from bs4 import BeautifulSoup
from datetime import datetime
import requests 
import pandas as pd
import os
import sys

def retreive_stats_page_text():
    stats_page = requests.get("https://pokemonshowdown.com/users/chillidawg")
    stats_page_soup = BeautifulSoup(stats_page.content, "html.parser")
    stats_page_text = stats_page_soup.text
    return stats_page_text

def obtain_randbats_elo(page_text):
    ladder_index = page_text.find("gen9randombattle")
    start_number_index = ladder_index + len("gen9randombattle")
    end_number_index = start_number_index + 4
    return page_text[start_number_index: end_number_index]


def obtain_formatted_date():
    now = datetime.now()
    return now.strftime("%d/%m/%Y %H:%M:%S")

def find(name, path):
    """finds the csv file"""
    for root, dirs, files in os.walk(path):
        if name in files:
            return os.path.join(root,name) 
        else:
            return None

def is_new_elo_different(randbats_elos_df, new_elo):
    last_elo = randbats_elos_df.iloc[len(randbats_elos_df)-1,1]
    if int(new_elo) == int(last_elo):
        return False
    else:
        return True


def update_csv():
    """check if elo score has changed. then, if csv file present, 
    change into pandas dataframe before updating. if no csv file present, make one"""

    new_row = {'datetime': obtain_formatted_date(), 'Elo': obtain_randbats_elo(retreive_stats_page_text())}
    randbats_elos_csv = find('randbats_elo.csv', '.')

    if randbats_elos_csv == None:
        randbats_elos = pd.DataFrame(new_row, index=False)
    else:
        randbats_elos = pd.read_csv(randbats_elos_csv)

        if is_new_elo_different(randbats_elos, new_row['Elo']):
            randbats_elos = randbats_elos.append(new_row, ignore_index = True)
            
    randbats_elos.to_csv('randbats_elo.csv', index=False)
