import pandas as pd
import networkx as nx
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.patches import Arc
import tweepy
import numpy as np

def create_viz():
  gameinfo = pd.read_csv('Game Information.csv')
  teams = pd.read_csv('teams.csv')
  passes = pd.read_csv('raw passes.csv')
  lineups = pd.read_csv('Starting Lineups.csv')
  subs = pd.read_csv('playerChanges.csv')
  touches = pd.read_csv('touches.csv')
  xgshots = pd.read_csv('shots with xG.csv')
  rawshots = pd.read_csv('raw shots.csv')

  xgshots.set_index("eventID", inplace=True

  # authentication
  # auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
  # auth.set_access_token(access_token, access_token_secret)

  # api = tweepy.API(auth)

  games = [1351761]

  for gameid in games:
      curr_game = gameinfo.loc[gameinfo['gameID'] == gameid, ['hteam', 'ateam', 'date']]
      curr_game.reset_index(inplace=True)

      date = curr_game.iloc[0, 3]

      team1 = str(curr_game.iloc[0, 1])
      team2 = str(curr_game.iloc[0, 2])

      color1 = teams.loc[teams['team'] == team1, 'color']
      color2 = teams.loc[teams['team'] == team2, 'color']

      fname1 = 'Current Week/' + team1 + ' Passing Map (' + team1 + ' vs. ' + team2 + ') ' + date.replace('/', '-') + '.png'
      fname2 = 'Current Week/' + team2 + ' Passing Map (' + team1 + ' vs. ' + team2 + ') ' + date.replace('/', '-') + '.png'
      fname3 = 'xGPlots/' + team1 + ' vs. ' + team2 + ' xG Plot ' + date.replace('/', '-') + '.png'

      pass_map(team1, gameid, color1, 0, lineups, subs, passes, gameinfo, touches)
      pass_map(team2, gameid, color2, 1, lineups, subs, passes, gameinfo, touches)
      #xg_plot(gameid, xgshots, rawshots, teams, gameinfo)

      hashtag1 = str(teams.loc[teams['team'] == team1, 'hashtag']).split()[1]
      hashtag2 = str(teams.loc[teams['team'] == team2, 'hashtag']).split()[1]

      twitter1 = str(teams.loc[teams['team'] == team1, 'twitter']).split()[1]
      twitter2 = str(teams.loc[teams['team'] == team2, 'twitter']).split()[1]

      tweet = '%s: Passing Network and xGPlot for %s vs. %s \n\n%s %s #MLS #autotweet' % (date, twitter1, twitter2, hashtag1, hashtag2)
      images = (fname1, fname2, fname3)

      #media_ids = [api.media_upload(i).media_id_string for i in images]

      #api.update_status(status=tweet, media_ids=media_ids)
