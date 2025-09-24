import pandas as pd
import requests
from bs4 import BeautifulSoup
import time

seasons = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024,2025]
for year in seasons:
    url = f"https://www.basketball-reference.com/leagues/NBA_{year}_totals.html"
    print(f"scraping {url}")

    response = requests.get(url)
    soup = BeautifulSoup(response.text,"lxml")
    tables = pd.read_html(url)
    df = tables[0]
    df = df[:-1]
    df = df.reset_index(drop=True)

    players = soup.select("table#totals_stats tbody tr td[data-stat='name_display'] a")
    player_ids_list = []
    for player_link in players:
        url = player_link.get("href", "")
        player_id = url.split("/")[-1].replace(".html", "")
        player_ids_list.append(player_id)
    df.insert(1, "player_id", player_ids_list)

    filename = f"nba_totals_{year-1}-{str(year)[-2:]}.csv"
    df.to_csv(filename,index=False)
    print(f"Saved {filename}")
    time.sleep(3)