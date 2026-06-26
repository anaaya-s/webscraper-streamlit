import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import streamlit as st

web_url = "https://pokemondb.net/pokedex/all"
raw_content = requests.get(web_url)

parsed_content = bs(raw_content.text, "html.parser")

table = parsed_content.find("table", id="pokedex")

table_body = table.tbody

list_of_rows = table_body.find_all("tr")

pokedex = list()
for row in list_of_rows:
    stats = dict()
    name_row = row.find("td", class_="cell-name")
    stats['Name'] = name_row.a.text
    num_rows = row.find_all("td", class_="cell-num")
    stats['Total'] = num_rows[1].text
    stats['HP'] = num_rows[2].text
    stats['Attack'] = num_rows[3].text
    stats['Defense'] = num_rows[4].text
    stats['Sp.Atk'] = num_rows[5].text
    stats['Sp.Def'] = num_rows[6].text
    stats['Speed'] = num_rows[7].text
    pokedex.append(stats)

pokedex_df= pd.DataFrame(pokedex)

st.sidebar.title("Search")
filter = st.sidebar.selectbox("Pokemon", ["All"] + list(pokedex_df["Name"].unique()) )

st.title("PokedexApp")
if(filter == "All"):
    filtered_df = pokedex_df
else:
    filtered_df = pokedex_df[pokedex_df["Name"] == filter]   
st.write(filtered_df) 
