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

############################################################
"""
Here is the new function for qb_rating
"""
def qb_rating(cmp = 0, att = 0, yds = 0, tds = 0, intpa = 0):
    cmp_ = ((cmp / att) - .3) * 5
    ypa_ = ((yds / att) - 3) * .25
    tdpa_ = ((tds / att) *20)
    intpa_ = 2.375 - ((intpa / att) * 25)
    
    cmp_ = pass_rate_quality_check(cmp_)
    ypa_ = pass_rate_quality_check(ypa_)
    tdpa_ = pass_rate_quality_check(tdpa_)
    intpa_ = pass_rate_quality_check(intpa_)
    
    rating = ((cmp_ + ypa_ + tdpa_ + intpa_) / 6 )* 100
    
    return rating 

# qb_rating(cmp = 19, att = 34, yds = 251, tds=0, intpa = 1)

#####
"""
Cumlative Passing Features

May need to consider the implications of doing a cummsum metrics on the current play, as it would 
indicate the result of the play not the prior. May need to consider shifting down stats afterwards.
"""

pass_['passing_att_cum'] = (pass_.groupby(['passer'])['passing_att'].cumsum())
pass_['passing_cmp_cum'] = (pass_.groupby(['passer'])['passing_cmp'].cumsum())
pass_['passing_int_cum'] = (pass_.groupby(['passer'])['passing_int'].cumsum())
pass_['passing_tds_cum'] = (pass_.groupby(['passer'])['passing_tds'].cumsum())
pass_['passing_yds_cum'] = (pass_.groupby(['passer'])['passing_yds'].cumsum())

pass_['cmp_cum'] = ((pass_.passing_cmp_cum / pass_.passing_att_cum) - .3) * 5           # completion percentage
pass_['ypa_cum'] = ((pass_.passing_yds_cum / pass_.passing_att_cum) - 3) * .25          # yards per attempt
pass_['tdpa_cum'] = (pass_.passing_tds_cum / pass_.passing_att_cum) * 20                # touchdowns per attempt 
pass_['intpa_cum'] = 2.375 - ((pass_.passing_int_cum / pass_.passing_att_cum) * 25)     # interceptions per attempt 

pass_['cmp_q'] = pass_.cmp_cum.apply(lambda x: pass_rate_quality_check(x))
pass_['ypa_q'] = pass_.ypa_cum.apply(lambda x: pass_rate_quality_check(x))
pass_['tdpa_q'] = pass_.tdpa_cum.apply(lambda x: pass_rate_quality_check(x))
pass_['intpa_q'] = pass_.intpa_cum.apply(lambda x: pass_rate_quality_check(x))

# Passer Rating

pass_['pass_rate_cum'] = ((pass_['cmp_q'] + pass_['ypa_q'] + pass_['tdpa_q'] + pass_['intpa_q']) / 6) * 100

pass_.drop(['cmp_cum', 'ypa_cum', 'tdpa_cum', 'intpa_cum','cmp_q','ypa_q','tdpa_q','intpa_q'], axis=1, inplace=True)
