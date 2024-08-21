from data_gather import get_batting_stats_with_year
import pandas as pd


def set_df(df):
    df = get_batting_stats_with_year(2015, 2024, 100)

    feats = ['Age', 'G', 'PA', 'H', '1B', '2B', '3B', 'HR', 'R', 'RBI', 'BB', 'IBB', 'SO', 'HBP', 'SB', 'AVG', 'BB%', 'K%', 'OBP', 'SLG', 'OPS',
             'ISO', 'BABIP', 'LD%', 'GB%', 'FB%', 'wOBA', 'wRC+', 'WAR', 'O-Swing%', 'Z-Swing%', 'Swing%', 'O-Contact%', 'Zone%', 'SwStr%', 'Pull%',
             'Cent%', 'Oppo%', 'Soft%', 'Med%', 'Hard%', 'EV', 'LA', 'Barrels', 'maxEV', 'xSLG', 'xwOBA', 'Whiff%', 'Chase%']
    
    targets = ['Next_xwOBA', 'Next_xBA', 'Next_EV', 'Next_HardHit%', 'Next_Barrel%', 'Next_Chase%', 'Next_Whiff%',
               'Next_K%', 'Next_BB%','Next_xSLG']
    
    all = feats + targets
    df = df.dropna(subset=feats)  

    return df