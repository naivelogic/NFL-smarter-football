# Smarter Football
A set of analtyics and machine learning models with the goal of bring intelligence to the NFL. 

![Smarter Football](https://imagesvc.timeincapp.com/v3/mm/image?url=https%3A%2F%2Fcdn-s3.si.com%2Fs3fs-public%2F2017%2F06%2F27%2Fsmarterfootballlogo.jpg "smarterfootballlogo")

## Topics Coverage
In this repository, there is an accumulation of different projects and notebooks all task with bring machine learning to the NFL. Some are applied data analytics answering questions such do teams perform better over time with a star runningback (stealers) or should teams adopt a duo time-sharing methdology (falcons)? We consider analysis if teams winning the first quarter more likely to win the game and perform better throughout the season. 
* Running Back Analytics
* NFL Playoff Prediction
* NFL Play-by-Play Run/Pass Prediction 
* Walkthroughs of applied machine learning pipelines 
* NFL News Analysis _(Work In Progress)_ [repo](https://github.com/naivelogic/NFL-smarter-football/tree/master/NFL%20News%20Analysis)
* NFL Twitter Analysis [Nike - Kaepernick](https://github.com/naivelogic/NFL-smarter-football/blob/master/Twitter%20Analysis%20on%20Nike's%20Kaepernick%20Endorsement.ipynb)

## Introduction
Months away from the 2019 NFL season, we take a look back on past NFL team season statistics to build a model to predict if a team is playoff bound or not. 

Machine learning models require much more than individual player and team statistics to determine the outcome of a game, let alone the course of a teams season that is filled with uncertainty to the untrained fan. Nevertheless, as a naive logician, we can attempt to use the odds in our favor and build a machine learner that can provide us an edge and advance the NFL competitiveness.


## Data Source
Most related to NFL Play-by-Play (pbp) 2012 - 2017 season is from [nflscraoR-data](https://github.com/ryurko/nflscrapR-data). 

For all the articles for the NFL News Analysis, I started scrapping various NFL teams the summer of 2018. Link to the [newspaper documentation](https://github.com/codelucas/newspaper) that I used for article scaping and curation.


__Point to remember about causality:__ One law of data science to keep top of mind: correlation does not imply causation. This is a common statistical phases used to emphasize that a correlation between two variables does not imply that one causes the other.

## Core Features
* Team
* Opponent
* Quarter
* Time
* Field position
* Down
* Yards to go
* Shotgun formation (0/1)
* PlayType: pass / run / kickoff/ penalty / punt/ fumble / int / timeout / extra point / field goal
* PlayDirection
  -> Pass: left / middle / right
  -> Run: left end / left tackle / left guard / middle / right guard / right tackle / right end
* PassDistance (short / deep)
* Success Measures _(Work In Progress)_
