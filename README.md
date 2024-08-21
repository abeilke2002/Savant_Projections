# Player Projections

## Process

Some of the most important MLB front office decisions are made during the offseason when executives need to decide whether or not to sign or trade for a player. Future projections of said player could help add context to this decision making. These projections can be some of the most dense and hardest modeling practices because you are attempting to predict human performance across a full season. There are so many bumps in the road over the course of a season that a player has to deal with that makes it hard to understand how they are going to perform. Although the task isn't easy, I decided to attempt to project player performance using a deep neural network.

## Modeling

As mentioned previously I constructed a deep neural network utilizing the Kera's packages in Python. From Keras I imported Sequential because the data was from 2015-2024 and it was important to note that this is time series data and seasons from 2023 shouldn't be used to predict 2021 data. The network is compiled of 6 hidden layers to give the model an opportunity to understand the non-linear relationships that come with predicting future player performance. In the end I also added some batch normalization and a dropout as well. In previous iterations I added more layers and more normalizations and dropouts, but found that the model was learning the training data too specifically, so I opted to keep the model more simplistic.

### Response Variables

My responses were choosen soley because I wanted to replicate what [Baseball Savant](https://baseballsavant.mlb.com/) does with their bubbles and percentiles. Not everybody may understand how good a .380 xwOBA is, but what is important is the colors and numbers. This was a really creative idea on behalf of the developers of Baseball Savant as it is more user friendly for people who perhaps don't have a firm grasp on sabermetrics. Here is a list of all of the variables I predicted:

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

The length of features spanned to be over 200 unique different variables of statistics that you could have for a player over the course of a season. Some examples of these statistics ran from 1B's, 2B's, 3B's, HR's, all the way to O-Swing% and Z-Swing%. In another effort to reduce overfitting, I created a function to select the top 20 features for each individual statistic. Because 20 features times 10 response variables would be a lot of writing, here were the 20 most important features for 2023 xSLG:

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

The metric I decided to go with was Mean Absolute Error. Essentially what MAE is is the absolute difference actual and predicted. Here is a list of the MAE for each of the response variables built in the model:

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

This project was a lot of fun and allowed me to be able to replicate what potentially MLB front office's do every offseason. Although I used a deep learning neural network, there are certainly areas to improve this model process.

#### Potential Improvements

- A.) More Data
For a model complex in itself already, the lack of data doesn't do the model any favors. When training for predictions for the 2021 season, the training data shape was only around 1800 rows. This is in addition to getting player seasons with a minimum at bats of 100. There is opportunity for randomness when a set the minimum threshold 100, but a risk I took to be able to get more training data.

- B.) Pitch Level Data
The statistics that were used to predict were strictly full season data. There is chance for luck to overtake a players stats. I've seen other player projection models use each batted ball from a hitter's season to get a deeper understanding of how they are coming to their season statistics. In this model, I took their statistics at surface level with little regard for how they got there.





