#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Friday Aug 17 2018
"""

import pandas as pd  # data manipultion librabry
import datetime

def game_weeks(df):
    """
    Create dataset indicate the game week. 
    """
    
    week_dict = {}
    first_game_date = df.min().date()
    game_date = first_game_date
    last_game_date = df.max().date()
    week_num = 1 # start week 1 and increment from there
    
    for i in range((last_game_date - first_game_date).days+1):
        if game_date.weekday() == 1: # check if weekday is Tuesday.. if so reset week_number
            week_num += 1
        week_dict[game_date] = week_num
        game_date += datetime.timedelta(days=1)
    
    week_list = pd.Series(week_dict).to_frame()[0]
    
    return week_list

def make_week(df):
    """
    Create function to make week number for each seasonal game. 
    """
    week_df = []
    for season in df.Season.unique():
        print(season)
        week_list = game_weeks(df[df.Season == season]['Date'])
        #week_df[season] = pd.DataFrame(week_list)
        week_df.append(week_list)
    new_df = pd.concat(week_df)
    
    return new_df
