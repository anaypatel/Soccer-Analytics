import pandas as pd
import networkx as nx
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.patches import Arc
import tweepy
import numpy as np

def xg_plot(gameid, xgshots, rawshots, teams, gameinfo):
    xgshots = xgshots[xgshots['gameID'] == gameid]
    rawshots = rawshots[rawshots['gameID'] == gameid]

    curr_game = gameinfo.loc[gameinfo['gameID'] == gameid]
    curr_game.reset_index(inplace=True)

    date = str(curr_game.iloc[0, 2])

    hteam = str(curr_game.iloc[0, 8])
    ateam = str(curr_game.iloc[0, 10])

    fname = 'xGPlots/' + hteam + ' vs. ' + ateam + ' xG Plot ' + date.replace('/', '-') + '.png'

    ref = curr_game.iloc[0, 6]
    attendance = int(curr_game.iloc[0, 7])
    hfinal = int(curr_game.iloc[0, 12])
    afinal = int(curr_game.iloc[0, 13])

    # Create figure
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    # Pitch Outline & Centre Line
    plt.plot([0, 0], [0, 90], color="black", alpha=0.3)
    plt.plot([0, 130], [90, 90], color="black", alpha=0.3)
    plt.plot([130, 130], [90, 0], color="black", alpha=0.3)
    plt.plot([130, 0], [0, 0], color="black", alpha=0.3)
    plt.plot([65, 65], [0, 90], color="black", alpha=0.3)

    # Left Penalty Area
    plt.plot([16.5, 16.5], [65, 25], color="black", alpha=0.3)
    plt.plot([0, 16.5], [65, 65], color="black", alpha=0.3)
    plt.plot([16.5, 0], [25, 25], color="black", alpha=0.3)

    # Right Penalty Area
    plt.plot([130, 113.5], [65, 65], color="black", alpha=0.3)
    plt.plot([113.5, 113.5], [65, 25], color="black", alpha=0.3)
    plt.plot([113.5, 130], [25, 25], color="black", alpha=0.3)

    # Left 6-yard Box
    plt.plot([0, 5.5], [54, 54], color="black", alpha=0.3)
    plt.plot([5.5, 5.5], [54, 36], color="black", alpha=0.3)
    plt.plot([5.5, 0.5], [36, 36], color="black", alpha=0.3)

    # Right 6-yard Box
    plt.plot([130, 124.5], [54, 54], color="black", alpha=0.3)
    plt.plot([124.5, 124.5], [54, 36], color="black", alpha=0.3)
    plt.plot([124.5, 130], [36, 36], color="black", alpha=0.3)

    # Prepare Circles
    centreCircle = plt.Circle((65, 45), 9.15, color="black", alpha=0.3, fill=False)
    centreSpot = plt.Circle((65, 45), 0.8, color="black", alpha=0.3)
    leftPenSpot = plt.Circle((11, 45), 0.8, color="black", alpha=0.3)
    rightPenSpot = plt.Circle((119, 45), 0.8, color="black", alpha=0.3)

    # Draw Circles
    ax.add_patch(centreCircle)
    ax.add_patch(centreSpot)
    ax.add_patch(leftPenSpot)
    ax.add_patch(rightPenSpot)

    # Prepare Arcs
    leftArc = Arc((11, 45), height=18.3, width=18.3, angle=0, theta1=310, theta2=50, color="black", alpha=0.3)
    rightArc = Arc((119, 45), height=18.3, width=18.3, angle=0, theta1=130, theta2=230, color="black", alpha=0.3)

    # Draw Arcs
    ax.add_patch(leftArc)
    ax.add_patch(rightArc)

    # Tidy Axes
    plt.axis('off')

    # Add xG Plot
    hteamxg = 0
    ateamxg = 0
    for index, row in rawshots.iterrows():
        if row['team'] == ateam:
            x = 1.3*row['x']
            y = 80 - 0.8*row['y']
            s = 150 * xgshots.loc[[row['eventID']], ['xGShooter']]['xGShooter']
            ateamxg = float(xgshots.loc[[row['eventID']], ['xGShooter']]['xGShooter']) + ateamxg
            plt.scatter(x, y, s=s, c=teams.loc[teams['team'] == ateam, 'color'])
        else:
            x = 130 - (1.3 * row['x'])
            y = 80 - 0.8 * row['y']
            s = 150 * xgshots.loc[[row['eventID']], ['xGShooter']]['xGShooter']
            hteamxg = float(xgshots.loc[[row['eventID']], ['xGShooter']]['xGShooter']) + hteamxg
            plt.scatter(x, y, s=s, c=teams.loc[teams['team'] == hteam, 'color'])

    ateamxg = round(ateamxg, 2)
    hteamxg = round(hteamxg, 2)

    score = 'Final Score: ' + hteam + ' ' + str(hfinal) + '-' + str(afinal) + ' ' + ateam
    moreinfo = 'Referee: ' + ref + ', Attendance: ' + str(attendance)
    xgscore = 'Final xG: ' + hteam + ' ' + str(hteamxg) + '-' + str(ateamxg) + ' ' + ateam
    title = 'xGPlot ' + date + ' ' + hteam + ' vs. ' + ateam + '\nData via @AnalysisEvolved\n' + xgscore

    personalinfo = 'Twitter: @anayfutbol Website: www.anaypatel.net'

    plt.title(title, size=10)
    plt.text(65, -10, score + '\n' + moreinfo + '\n' + personalinfo, ha="center", size=8)

    # Display Pitch
    #plt.show()
    fig.savefig(fname)
