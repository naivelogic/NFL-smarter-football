"""
# NFL Passer Rating Formula
The NFL passer rating formula includes four variables:
    - completions percentages
    - yards per attempt
    - touchdowns per attempt
    - interception per attempt

Each of these variables is scaled to a value between 0 and 2.375, with 
1.0 being statistically average (based on league data between 1960-1970).

Note: passing performance in 2017 as the league average rating was 88.6

Source: https://en.wikipedia.org/wiki/Passer_rating 

"""

import pandas as pd

pass_ = pd.read_csv('pass_.csv')

qb_rating = pass_.groupby(['passer']).aggregate({
    'passing_cmp':sum,
    'passing_att':sum,
    'passing_yds':sum,
    'passing_tds':sum,
    'passing_int':sum
}).reset_index()

qb_rating['cmp'] = ((qb_rating.passing_cmp / qb_rating.passing_att) - .3) * 5           # completion percentage
qb_rating['ypa'] = ((qb_rating.passing_yds / qb_rating.passing_att) - 3) * .25          # yards per attempt
qb_rating['tdpa'] = (qb_rating.passing_tds / qb_rating.passing_att) * 20                # touchdowns per attempt 
qb_rating['intpa'] = 2.375 - ((qb_rating.passing_int / qb_rating.passing_att) * 25)     # interceptions per attempt 

rating_col = ['cmp', 'ypa', 'tdpa', 'intpa']

def pass_rate_quality_check(rating):
    """
    If the result of any calculation is greater than 2.375, it is set to 2.375. 
    If the result is a negative number, it is set to zero.
    """
    if rating > 2.375:
        rating = 2.375

    elif rating < 0:
        rating = 0
    
    return rating

qb_rating['cmp'] = qb_rating.cmp.apply(lambda x: pass_rate_quality_check(x))
qb_rating['ypa'] = qb_rating.ypa.apply(lambda x: pass_rate_quality_check(x))
qb_rating['tdpa'] = qb_rating.tdpa.apply(lambda x: pass_rate_quality_check(x))
qb_rating['intpa'] = qb_rating.intpa.apply(lambda x: pass_rate_quality_check(x))


# Passer Rating
qb_rating['pass_rate'] = ((qb_rating['cmp'] + qb_rating['ypa'] + qb_rating['tdpa'] + qb_rating['intpa']) / 6) * 100

print(qb_rating)
