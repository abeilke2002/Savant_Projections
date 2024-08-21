# Player Projections

## Process

Some of the most important MLB front office decisions are made during the offseason when executives need to decide whether or not to sign or trade for a player. Future projections of said player could help add context to this decision making. These projections can be some of the most dense and hardest modeling practices because you are attempting to predict human performance across a full season. There are so many bumps in the road over the course of a season that a player has to deal with that makes it hard to understand how they are going to perform. Although the task isn't easy, I decided to attempt to project player performance using a deep neural network.

## Modeling

The model for this code was to predict the delta run expectancy of a given pitch. There were a lot of different variables that were tallied with the potential to be a good predictor to predict the change in run expectancy. This was also not an easy task to predict the run expectancy when you are not feeding the model the outcome of the pitch. Given only pitch characteristics, it can be tough for a model to understand the result of the pitch. 

In order to make the model a litte more forgiving, I decided to create two different models trained on pitches were the pitch was swung at, and a model trained on pitches that were not swung at.

### Swing Model

In the swing model, it was tested that there were 11 variables that we could conclude significant in the prediction of delta run expectancy. The model used in the swing model was a Gradient Boosting Model. The RMSE of this model was around a 0.341. The variables were, ranked by significance:

- Vertical Location of Pitch
- The Statcast Attack Zone
- Balls in the count
- Horizontal Location of Pitch
- Strikes in the count
- Velocity of Pitch
- Vertical movement of Pitch
- Spin Rate of Pitch
- Horizontal movement of Pitch
- Pitch Type
- Handedness of Pitcher

### Take Model

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
