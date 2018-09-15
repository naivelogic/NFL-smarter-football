# preprocessing.py

"""
Listing of functions to assist with formatting text including:
- Defining the words to remove from the corpus and n-grams
- Data cleaning
- data normalization (work in progress - may convert to another file)
"""


import nltk
from nltk.corpus import stopwords
from sklearn.feature_extraction.stop_words import ENGLISH_STOP_WORDS

def remove_stop_words():
    '''
    Remove any stopwards as needed
    '''
    default_stopwords = set( stopwords.words('english') ).union( set(ENGLISH_STOP_WORDS) )
    my_additional_stop_words = (nfl_news_stopwords) # Add any additional stopwords we dont want and update the list
    default_stopwords = default_stopwords.union(my_additional_stop_words)
    
    return(default_stopwords)   



import re

def preprocess_post(post):
    post = post.lower()
    post = re.sub('\n', ' ', post)
    post = re.sub(r'[^\w\s]','',post)
    
    return post

"""
listing of words that im currently considering not applicable
for purposes of n-grams, they may be incorporated when we perform 
sentiment analysis and start using LSTM
"""
nfl_news_stopwords = ['game', 'team', 'season', 'year', 'like', 'time', 'just', 'nfl', '2018', 'august', 'field', 
                        'games', 'who', 'years', 'pm', 'et', 'aug', 'say', 'lot', 'august', 'let', 'week', 'vs', 'going', 
                        'links', 'day', '2017', 'things', 'really', 'numbers', 'live', 'saw', 'does', 'fan', 'youre', '53',
                        'didnt', 'makes', '12', 'used', 'yes', 'let', 'hey', 'gets', 'cat', 'getty', 'images', 'th', 
                        'think', 'said', 'im', 'hes', 'thats', 'tag', 'need', 'went', 'dont', 'look', 'want', 'st', 'nd', 
                        'rd', 'isnt', 'play','player']



def game_weeks(df):
    """
    Create dataset indicate the game week. 
    """
    
    week_dict = {}
    first_game_date = df.min().date()
    game_date = first_game_date
    season_start_date = pd.to_datetime('2018-09-04 00:00:00').date()
    last_game_date = df.max().date()
    week_num = 1 # start week 1 and increment from there
    
    for i in range((last_game_date - first_game_date).days+1):
        if game_date <= season_start_date:
            week_dict[game_date] = 0
            game_date += datetime.timedelta(days=1)
        else:
            if game_date.weekday() == 1: # check if weekday is Tuesday.. if so reset week_number
                week_num += 1
            week_dict[game_date] = week_num
            game_date += datetime.timedelta(days=1)
    
    week_list = pd.Series(week_dict).to_frame()[0]
    
    return week_list

#d = game_weeks(nfl.date)
#for o,j in enumerate(d.index):
#    nfl.loc[nfl.date == j, 'week'] = d[o]
