import pybaseball as py
from pybaseball import statcast, playerid_reverse_lookup
import numpy as np
import pandas as pd

def next_season(player, cols):
    player = player.sort_values("Season")
    for col in cols:
        player[f"Next_{col}"] = player[col].shift(-1)
    return player

def get_batting_stats_with_year(start_year, end_year, min_abs):
    all_data = pd.DataFrame()
    
    for year in range(start_year, end_year + 1):
        print(f"Getting data for the year {year}")
        yearly_data = py.batting_stats(year, qual=min_abs)
        
        yearly_data['Whiff%'] = 1 - yearly_data['Contact%']
        yearly_data['Chase%'] = yearly_data['O-Swing%']
        all_data = pd.concat([all_data, yearly_data], ignore_index=True)

    all_data = all_data.groupby("IDfg", group_keys=False).filter(lambda x: x.shape[0] > 1)

    pred_cols = ['xwOBA', 'xBA', 'xSLG', 'EV', 'HardHit%', 'Barrel%', 'Chase%', 'Whiff%', 'K%', 'BB%']

    all_data = all_data.groupby("IDfg", group_keys=False).apply(next_season, cols=pred_cols)
    all_data = all_data.sort_values(by="Season", ascending=True)

    # Extract player names for lookup
    player_ids = all_data['IDfg'].unique()
    player_map = pd.DataFrame()

    for player_id in player_ids:
        player_info = py.playerid_reverse_lookup([player_id], key_type='fangraphs')
        if not player_info.empty:
            player_map = pd.concat([player_map, player_info[['key_fangraphs', 'key_mlbam']]], ignore_index=True)

    all_data = all_data.merge(player_map, left_on='IDfg', right_on='key_fangraphs', how='left')

    return all_data
