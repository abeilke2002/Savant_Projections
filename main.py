import pandas as pd
from data_preprocess.py import set_df
from train_models import predict_next_season_stats, get_percentiles
import numpy as np

def main():
    data = set_df(pd.DataFrame())
    predictors = ['Age', 'G', 'PA', 'H', '1B', '2B', '3B', 'HR', 'R', 'RBI', 'BB', 'IBB', 'SO', 'HBP', 'SB', 'AVG', 'BB%', 'K%', 'OBP', 'SLG', 'OPS',
              'ISO', 'BABIP', 'LD%', 'GB%', 'FB%', 'wOBA', 'wRC+', 'WAR', 'O-Swing%', 'Z-Swing%', 'Swing%', 'O-Contact%', 'Zone%', 'SwStr%', 'Pull%',
              'Cent%', 'Oppo%', 'Soft%', 'Med%', 'Hard%', 'EV', 'LA', 'Barrels', 'maxEV', 'xSLG', 'xwOBA', 'Whiff%', 'Chase%']

    test = predict_next_season_stats(data, predictors)
    test = get_percentiles(test)
    test.to_csv("preds.csv")


if __name__ == "__main__":
    main()
