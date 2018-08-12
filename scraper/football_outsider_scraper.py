"""
Football Ousider Webscraper
 * Team Efficiency
 * Team Offense
"""

import requests
import pandas as pd
import numpy as np
import re
from bs4 import BeautifulSoup
import urllib3

def set_url(yr_range, stat_type):
    urls = ["http://www.footballoutsiders.com/stats/"+stat_type+str(x) for x in yr_range]
    return urls

def grab_data(url):
    """
    function to get soup
    """
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    return soup

def soup_table(url, season):
    """
    function to get tables from advances stats
    """
    # find all relevent tables with stats
    
    new_table = []
    tb = url.find("table", class_ = "stats")
    #stats_table = soup.find_all("table", {"class": "stats"})
    for tb in url.find_all('tr'):
        tds = tb.find_all('td')
        if tds == []:
            continue
        
        row = []
        for i in tds:
            try:
                #row.append(float(i.text.replace('%','')))
                row.append(float(i.text.strip("%")) / 100)
            except:
                row.append(i.text.replace('%',''))
        row.append(season)
        if row[0] != '':
            new_table.append(row)
            
    return new_table

def define_col_name(stat_type):
    if stat_type == 'teamoff':
        col = ['off_eff_ov_rank', 'Team', 'Off_DVOA', 'last_yr_rank', 'weighted_off', 'wei_off_rank',
              'pass_off', 'pass_rank', 'rush_off', 'rush_rank', 'non_adj_total',
              'non_adj_pass', 'non_adj_rush', 'variance', 'var_rank', 'sched', 'sched_rank','season']
    elif stat_type == 'teameff':
        # https://www.footballoutsiders.com/stats/teameff
        col = [
            'eff_rank','team', 'tot_dvoa', 'last_yr_dvoa_rank', 'non_adj_tot_voa', 'win_los', 'off_dvoa', 'off_rank',
            'def_dvoa', 'def_rank', 'st_dvoa', 'st_rank',
            'est_wins', 'est_win_rank', 'wei_dvoa', 'wei_dvoa_rank', 'sched', 'sched_rank', 'proj_wins', 'proj_win_rank',
            'variance', 'var_rank','season'
        ]
    return col

def soup_table_eff(url, season):
    row_counter = 0
    new_table_1 = []
    new_table_2 = []
    tb = url.find("table", class_ = "stats")
    for tb in url.find_all('tr'):
        tds = tb.find_all('td')
        if tds == []:
            continue
        row = []
        for i in tds:
            if "%" in i.text:
                # convert percentage strings to floats
                try:
                    row.append(float(i.text.strip("%")) / 100)
                except:
                    row.append("")
            else:
                try:
                    row.append(float(i.text))
                except:
                    row.append(i.text)
        row.append(season)



        if (row[0] != '') & (row_counter >= 34):
            new_table_2.append(row)
        elif (row[0] != '') & (row_counter < 34):
            new_table_1.append(row)
        row_counter += 1
    
    # run script to modify table since we techically scrapped 2 tables
    soup_df = strip_stats_eff(new_table_1, new_table_2)
    
    return soup_df

    
def strip_stats_eff(table_1, table_2):
    df1 = pd.DataFrame(table_1)
    df2 = pd.DataFrame(table_2)
    
    # remove seasons from df1
    df1 = df1[df1.columns[:-1]]
    
    # fields to keep for table 2 (df2)
    df2 = df2[[4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14]]
    
    
    df = pd.concat([df1,df2],axis=1)
    
    # new headers
    header = define_col_name('teameff')
    
    df.columns = header
    
    return df

def make_table(yr_range, stat_type):   
    urls = set_url(yr_range, stat_type)
    print(urls)
    
    if stat_type == 'teameff':
        df = {}
        for url in urls:
            season = url[-4:]
            print(season)
            soup = grab_data(url)
            table = soup_table_eff(soup, season)
            df[season] = pd.DataFrame(table)
        new_df = pd.concat(df.values())
    
    elif stat_type == 'teamoff':
        df = {}
        for url in urls:
            season = url[-4:]
            print(season)
            soup = grab_data(url)
            table = soup_table(soup, season)
            df[season] = pd.DataFrame(table, columns=define_col_name(stat_type))
        new_df = pd.concat(df.values())
        
        
    return new_df
