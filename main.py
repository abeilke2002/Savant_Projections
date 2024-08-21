import pandas as pd
from data_gather import get_batting_stats_with_year, get_launch_angle_swsp, join_all_df
import numpy as np

def main():
    start_year = 2015
    end_year = 2023
    min_abs = 200

    start_date = '2015-01-01'
    end_date = '2023-09-30'
    min_bbe = 100

    season_stats = get_batting_stats_with_year(start_year, end_year, min_abs)
    la_swsp = get_launch_angle_swsp(start_date, end_date, min_bbe)

    data = join_all_df(season_stats, la_swsp)
    la_swsp.to_csv("la_swsp.csv")
    data.to_csv("all_players.csv")


if __name__ == "__main__":
    main()



# Save the accumulated predictions to a CSV file after the loop
test_2023.to_csv("2023_preds.csv", index=False)
print("2023 predictions saved to preds.csv")

average_diff_df = pd.DataFrame(average_diffs)
average_diff_df.to_csv("average_diffs.csv", index=False)