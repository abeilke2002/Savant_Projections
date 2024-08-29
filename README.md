# Player Projections
Streamlit link: https://aidanbeilke-savant-predictions.streamlit.app/

## Process

Some of the most important decisions made by MLB front offices occur during the offseason when executives must decide whether to sign or trade for players. Future projections of a player's performance can help add context to these decisions. However, these projections are some of the densest and most challenging modeling practices because predicting human performance over a full season is difficult. Players face numerous challenges throughout a season, making it hard to forecast how they will perform. Despite the difficulty, I decided to attempt to project player performance using a deep neural network.

## Modeling

I constructed a deep neural network utilizing Keras in Python. I imported the Sequential model from Keras because the data spanned from 2015-2024, and it was essential to recognize that this is time-series data. Seasons from 2023 should not be used to predict 2021 data. The network is composed of six hidden layers to allow the model to learn the non-linear relationships involved in predicting future player performance. I also included batch normalization and dropout layers to improve generalization. In earlier iterations, I added more layers and regularization techniques, but I found that the model began overfitting the training data, so I opted for a simpler design.

### Response Variables

I chose my response variables to replicate what [Baseball Savant](https://baseballsavant.mlb.com/) does with their bubbles and percentiles. Not everyone may understand how good a .380 xwOBA is, but the colors and numbers in their visualizations make it more user-friendly, especially for people who may not have a strong grasp on sabermetrics. Here is a list of the variables I predicted:

- xwOBA
- xBA
- xSLG
- EV
- Barrel%
- Hard Hit%
- Chase%
- Whiff%
- K%
- BB%



### Features

The feature set consisted of over 200 unique statistics that can be collected for a player over the course of a season. These features ranged from basic counting stats like singles, doubles, and home runs to advanced metrics like O-Swing% and Z-Swing%. To reduce overfitting, I created a function that selected the top 20 features for each individual statistic. Since it would be lengthy to list all 20 features for each of the 10 response variables, here are the 20 most important features for predicting xSLG in 2023:

- Soft%
- Hard%
- Previous xSLG
- WAR
- xwOBA
- Barrels
- IBB
- Oppo%
- Swing%
- Z-Swing%
- O-Swing%
- OBP
- Med%
- Pull%
- EV
- Chase%
- LD%
- 3B
- SwStr%
- HR

## Results

I used Mean Absolute Error (MAE) as the evaluation metric. MAE represents the average absolute difference between the actual and predicted values. Below is the MAE for each of the response variables:

- Next_BB%         0.017909
- Next_Barrel%     0.075940
- Next_Chase%      0.030418
- Next_EV          1.516423
- Next_HardHit%    0.204434
- Next_K%          0.059124
- Next_Whiff%      0.030549
- Next_xBA         0.021822
- Next_xSLG        0.162571
- Next_xwOBA       0.051578

## Conclusions

This project was a lot of fun and allowed me to replicate what MLB front offices might do every offseason. Although I used a deep learning neural network, there are certainly areas where this process could be improved.

#### Potential Improvements

- A.) More Data
  
For an already complex model, the lack of data doesn't help. When training for the 2021 season, the dataset had only about 1,800 rows, despite limiting the player seasons to those with a minimum of 100 at-bats. While setting a minimum threshold of 100 at-bats helped gather more training data, it introduced a risk of randomness.

- B.) Pitch Level Data

The statistics used in this model were full-season aggregates. This approach may allow for luck or randomness to influence a player's season statistics. Other projection models use pitch-level data to get a deeper understanding of how players accumulate their season totals. In contrast, this model took surface-level statistics with little regard for how they were achieved.

- C.) Simple Deep Learning Model

Another limitation might be the simplicity of the model. While I included a few hidden layers with batch normalization and dropout, there is room for more complexity. Other baseball projection models utilize convolutional neural networks (CNNs) with convolutional layers, max-pooling layers, and dense layers to capture the complex, non-linear relationships present in year-to-year player performance.
