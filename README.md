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

The take model followed a nearly identical process as the swing model, but with a few important changes to note. First, we of course were looking only at pitches not swung at. Secondly, we used a different model that required a lot less features. We used an XGBoost model that had an RMSE of 0.070. An RMSE much better than our swing model likely because the results for a take are less variable than a result for a swing. Here are the variables, ranked by significance:

- Attack Zone
- Balls in the count
- Strikes in the count
- Vertical Location of Pitch
- Horizontal Location of Pitch


## Results

After training the model on 2023 data, I decided to use these two separate models and test on the 2024 season so far. After finding the leaders in both the swing decision and take decisions, I would then find the average of the two and create a wholistic statistic that could find overall who makes the most impactful decisions.


### Take Leaders
Here are the batters with the best take decisions:

- Kyle tucker
- Brandon Nimmo
- Lamonte Wade
- Bryce Harper

What separates these guys is that they are not swinging at pitches generally that are predicted to have a negative run expectancy. Simply put, they are not chasing pitches that are hard to do damage against.

### Swing Leaders
Here are the batters with the best swing decisions:

- Brandon Marsh
- Brenton Doyle
- Steven Kwan
- Gleyber Torres

Similiar to the take leaders, what these batters excel at is swinging at pitches that have a positive run expectancy predicted value. Something of note for this leaderboard is the lineup around them. If a player has a superstar lineup around them filled with all stars, and this player in question is not an all star, they are likely to see more pitches to hit, forcing them to swing more. Same could be said for a leadoff batter as well.

## Conclusions

Baseball is a challenging game, and therein lies the importance of process metrics. Having a robust process can reassure players or front offices that a small sample of a player's struggles is just that—a small sample—and not necessarily indicative of future performance. Instead, a sound process might suggest that a breakout could be imminent.

The dilemma with these process-oriented models is determining where to draw the line. Ultimately, baseball is a results-oriented game for many. Each team has a different tolerance for how long they can wait for a player to start showing positive results. No baseball statistic is perfect, and other factors likely contribute to a player's struggles as well.

In our model, we only looked at pitch characteristics and count to determine the run expectancy of a pitch, intentionally omitting the outcome of the pitch. This could be a shortcoming of the model and may lead to some inaccuracies. There is also potential bias in the swing model. Batters who tend to get more pitches to hit, swing more, or are the weak points in their lineup will have more opportunities to swing. While this model is not perfect, it could help identify potential areas of strength or weakness in a batter."

This version refines some phrases and maintains the critical perspective on the limitations of process metrics while acknowledging their potential benefits.
