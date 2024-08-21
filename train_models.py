import tensorflow as tf
from tensorflow import keras
from data_preprocess import set_df
from keras.models import Sequential
from keras.layers import Dense, Activation, Flatten, Input, BatchNormalization, Dropout
import pandas as pd
import numpy as np

def train_target_model(input_dim):
    xwoba_model = Sequential()

    xwoba_model.add(Input(shape=(input_dim,)))

    # First block
    xwoba_model.add(Dense(128, kernel_initializer='normal', activation='relu'))

    # Second block
    xwoba_model.add(Dense(256, kernel_initializer='normal', activation='relu'))

    # Third block
    xwoba_model.add(Dense(256, kernel_initializer='normal', activation='relu'))

    # Fourth block
    xwoba_model.add(Dense(128, kernel_initializer='normal', activation='relu'))

    # Fifth block
    xwoba_model.add(Dense(64, kernel_initializer='normal', activation='relu'))

    # Sixth block
    xwoba_model.add(Dense(32, kernel_initializer='normal', activation='relu'))

    # Apply batch normalization and dropout after all dense layers
    xwoba_model.add(BatchNormalization())
    xwoba_model.add(Dropout(0.2))

    # Output layer
    xwoba_model.add(Dense(1, kernel_initializer='normal', activation='linear'))

    # Compile model
    xwoba_model.compile(loss='mean_absolute_error', optimizer='adam', metrics=['mean_absolute_error'])
    
    return xwoba_model

def get_top_predictors(train_data, predictors, target, num_features=20):
    input_dim = train_data[predictors].shape[1]
    model = train_target_model(input_dim)
    
    model.fit(train_data[predictors], train_data[target], epochs=50, batch_size=32, verbose=0)
    
    weights = model.layers[0].get_weights()[0]
    feature_weights = pd.Series(np.abs(weights).sum(axis=1), index=predictors)
    
    top_predictors = feature_weights.nlargest(num_features).index.tolist()
    
    return top_predictors

def predict_next_season_stats(data, predictors, start=5, step=1, epochs=50, batch_size=32):
    targets = ['Next_xwOBA', 'Next_xBA', 'Next_EV', 'Next_HardHit%', 'Next_Barrel%', 'Next_Chase%', 'Next_Whiff%',
               'Next_K%', 'Next_BB%','Next_xSLG']

    predictions_df = pd.DataFrame(columns=["Name", "Season", "Stat", "Actual", "Predicted"])

    final_model = None
    years = sorted(data["Season"].unique())
    
    for target in targets:
        print(f"Processing target: {target}")

        # Select top 15 predictors based on the initial training period
        initial_train = data[(data["Season"] < years[start]) & (data[target].notna())]
        top_predictors = get_top_predictors(initial_train, predictors, target)

        for i in range(start, len(years) - 1, step):
            current_year = years[i]
            train = data[(data["Season"] < current_year) & (data[target].notna())]
            test = data[(data["Season"] == current_year) & (data[target].notna())]

            # Debugging statements
            print(f"Training model for year: {current_year}")
            print(f"Selected top predictors: {top_predictors}")
            print(f"Training data shape: {train[top_predictors].shape}")
            print(f"Testing data shape: {test[top_predictors].shape}")

            input_dim = len(top_predictors)
            xwoba_model = train_target_model(input_dim)
        
            xwoba_model.fit(train[top_predictors], train[target], epochs=epochs, batch_size=batch_size, verbose=0)
        
            preds = xwoba_model.predict(test[top_predictors])
            preds = pd.Series(preds.flatten(), index=test.index)

            print(f"Predictions for {target} in year {current_year}: {preds.head()}")

            # Create a temporary DataFrame with the required information
            temp_df = pd.DataFrame({
                "Name": test["Name"],
                "Season": test["Season"],
                "Stat": target,
                "Actual": test[target],
                "Predicted": preds
            })

            # Append to the main predictions DataFrame
            predictions_df = pd.concat([predictions_df, temp_df], ignore_index=True)
        
            if current_year == 2022:
                final_model = xwoba_model
    
        # Predict for 2024 season (for 2025)
        if final_model is not None:
            test_2024 = data[(data["Season"] == 2024)]
            preds_2024 = final_model.predict(test_2024[top_predictors])
            preds_2024 = pd.Series(preds_2024.flatten(), index=test_2024.index)
        
            temp_df_2023 = pd.DataFrame({
                "Name": test_2024["Name"],
                "Season": test_2024["Season"],
                "Stat": target,
                "Actual": test_2024[target],
                "Predicted": preds_2024
            })

            predictions_df = pd.concat([predictions_df, temp_df_2023], ignore_index=True)
            predictions_df['diff'] = (predictions_df['Predicted'] - predictions_df['Actual']).abs()

            diff_table = predictions_df.groupby('Stat')['diff'].mean()
            print(diff_table.head(len(diff_table)))

        else:
            print(f"No model was trained for the 2023 season for {target}. Check your data and backtesting logic.")

    return predictions_df



def get_percentiles(data):
    flip_stats = ['Next_Chase%', 'Next_K%', 'Next_Whiff%']

    if not (data['Season'] == 2024).all():
        # Calculate actual percentiles for seasons other than 2024
        actual_percentile = data.loc[data['Season'] != 2024].groupby(['Season', 'Stat'])['Actual'].rank(pct=True) * 100
        predicted_percentile = data.groupby(['Season', 'Stat'])['Predicted'].rank(pct=True) * 100

        data.loc[data['Season'] != 2024, 'Actual_Percentile'] = actual_percentile.where(~actual_percentile.isna(), other=pd.NA).round(0)
        data['Predicted_Percentile'] = predicted_percentile.where(~predicted_percentile.isna(), other=pd.NA).round(0)

        data.loc[data['Season'] != 2024, 'Actual_Percentile'] = data.loc[data['Season'] != 2024, 'Actual_Percentile'].apply(lambda x: int(x) if pd.notna(x) else pd.NA)
        data['Predicted_Percentile'] = data['Predicted_Percentile'].apply(lambda x: int(x) if pd.notna(x) else pd.NA)

    else:
        # For the 2024 season, only calculate predicted percentiles
        predicted_percentile = data.groupby(['Season', 'Stat'])['Predicted'].rank(pct=True) * 100
        data['Predicted_Percentile'] = predicted_percentile.where(~predicted_percentile.isna(), other=pd.NA).round(0)
        data['Predicted_Percentile'] = data['Predicted_Percentile'].apply(lambda x: int(x) if pd.notna(x) else pd.NA)

    # Flip the percentiles for stats where higher is worse
    data.loc[data['Stat'].isin(flip_stats), 'Actual_Percentile'] = 100 - data['Actual_Percentile']
    data.loc[data['Stat'].isin(flip_stats), 'Predicted_Percentile'] = 100 - data['Predicted_Percentile']

    return data



data = set_df(pd.DataFrame())
predictors = ['Age', 'G', 'PA', 'H', '1B', '2B', '3B', 'HR', 'R', 'RBI', 'BB', 'IBB', 'SO', 'HBP', 'SB', 'AVG', 'BB%', 'K%', 'OBP', 'SLG', 'OPS',
              'ISO', 'BABIP', 'LD%', 'GB%', 'FB%', 'wOBA', 'wRC+', 'WAR', 'O-Swing%', 'Z-Swing%', 'Swing%', 'O-Contact%', 'Zone%', 'SwStr%', 'Pull%',
              'Cent%', 'Oppo%', 'Soft%', 'Med%', 'Hard%', 'EV', 'LA', 'Barrels', 'maxEV', 'xSLG', 'xwOBA', 'Whiff%', 'Chase%']

# Run backtest
test = predict_next_season_stats(data, predictors)
test = get_percentiles(test)
test.to_csv("preds.csv")


