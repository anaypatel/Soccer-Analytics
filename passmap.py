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


def pass_map(team, gameid, nodecolor, team_no, lineups, subs, passes, gameinfo, touches):

    # Filtering lineups data for a specific game ID and team, extracting player names

    lineups = lineups[lineups['gameID'] == gameid]

    lineups.reset_index(inplace=True)

    IC = lineups.ix[team_no, 5:23]

    startingXI = lineups.ix[team_no, 5:16]

    lineups.to_csv('lineups.csv')

    # Creating an adjacency matrix

    passNetwork = pd.DataFrame(0, index=IC, columns=IC)

    # Time of first substitution

    subs = subs[subs['gameID'] == gameid]
    subs = subs[subs['team'] == team]
    subs.reset_index(inplace=True)

    try:
        firstsub = subs.ix[0, 3]
    except:
        firstsub = '100:00'

    # Filtering passes data for a specific game ID and team

    passes = passes[passes['gameID'] == gameid]
    passes = passes[passes['team'] == team]
    passes = passes[passes['time'] <= firstsub]

    # Creating a title for the plot

    date = passes.iloc[0, 0]
    opp = passes.iloc[0, 9]
    title = date + ' ' + team + ' Passing Network vs. ' + opp + '\nMinutes 0:00-' + firstsub + '\n(Data via @AnalysisEvolved)\n\nTwitter: @anayfutbol\nwww.anaypatel.net'

    # Creating more info from the game for the plot

    gameinfo = gameinfo[gameinfo['gameID'] == gameid]

    ref = gameinfo.iloc[0, 5]
    attendance = gameinfo.iloc[0, 6]
    home = gameinfo.iloc[0, 7]
    away = gameinfo.iloc[0, 9]
    hfinal = gameinfo.iloc[0, 11]
    afinal = gameinfo.iloc[0, 12]

    score = 'Final Score: ' + home + ' ' + hfinal.astype(str) + '-' + afinal.astype(str) + ' ' + away
    moreinfo = 'Referee: ' + ref + ', Attendance: ' + attendance.astype(str)

    for index, row in passes.iterrows():
        if row["success"] == 1:
            try:
                passNetwork.loc[[row["passer"]], [row["recipient"]]] = passNetwork.loc[[row["passer"]], [row["recipient"]]] + 1
            except:
                print("an error occurred")

    # Filtering touches data for a specific game ID and team
    touches = touches[touches['gameID'] == gameid]
    touches = touches[touches['team'] == team]

    # Creating a graph
    G = nx.Graph()

    # Create nodes
    for index, row in touches.iterrows():
        if row['player'] in startingXI.values:
            if len(row['player'].split()) > 1:
                label = row['player'].split()[1]
            else:
                label = row['player']

            G.add_node(row['player'], pos=(90-0.8*row['averageY'], 1.3*row['averageX']),
                       sz=row['touches']*7, label=label)
            # G.add_node(row['player'], pos=(90-0.8*row['averageY'], 1.3*row['averageX']),
            #           sz=passNetwork[row['player']].sum()*5)

    # Create edges from adjacency matrix
    for passer in startingXI:
        for recipient in startingXI:
            if (passNetwork.loc[passer, recipient] + passNetwork.loc[recipient, passer]).astype(float) >= 4:
                        G.add_edge(passer, recipient, weight=(passNetwork.loc[passer, recipient] + passNetwork.loc[recipient, passer]).astype(float)/4)

    passNetwork.to_csv('passNetwork.csv')
    passes.to_csv('currentPasses.csv')

    # Get attributes for plotting
    pos = nx.get_node_attributes(G, 'pos')
    sz = nx.get_node_attributes(G, 'sz')
    weight = nx.get_edge_attributes(G, 'weight')
    labels = nx.get_node_attributes(G, 'label')

    # Create the figure

    fig = plt.figure(figsize=(9,13))
    ax = fig.add_subplot(1, 1, 1)

    #Pitch Outline & Centre Line
    plt.plot([0,0],[130,0], color="black",alpha=0.3)
    plt.plot([90,0],[0,0], color="black",alpha=0.3)
    plt.plot([90,90],[0,130], color="black",alpha=0.3)
    plt.plot([0,90],[65,65], color="black",alpha=0.3)
    plt.plot([0,90],[130,130], color="black",alpha=0.3)

    # Bottom Penalty Area
    plt.plot([65,25],[16.5,16.5],color="black",alpha=0.3)
    plt.plot([65,65],[0,16.5],color="black",alpha=0.3)
    plt.plot([25,25],[16.5,0],color="black",alpha=0.3)

    # Top Penalty Area
    plt.plot([65, 65],[130, 113.5],  color="black", alpha=0.3)
    plt.plot([65, 25], [113.5, 113.5], color="black", alpha=0.3)
    plt.plot([25, 25], [113.5, 130], color="black", alpha=0.3)

    # Bottom 6-yard Box
    plt.plot([54, 54], [0, 5.5], color="black", alpha=0.3)
    plt.plot([54, 36], [5.5, 5.5], color="black", alpha=0.3)
    plt.plot([36, 36], [5.5, 0.5], color="black", alpha=0.3)

    # Top 6-yard Box
    plt.plot([54, 54], [130, 124.5], color="black", alpha=0.3)
    plt.plot([54, 36], [124.5, 124.5], color="black", alpha=0.3)
    plt.plot([36, 36], [124.5, 130], color="black", alpha=0.3)

    # Prepare Circles
    centreCircle = plt.Circle((45, 65), 9.15, color="black", fill=False, alpha=0.3)
    centreSpot = plt.Circle((45, 65), 0.8, color="black", alpha=0.3)
    leftPenSpot = plt.Circle((45, 11), 0.8, color="black", alpha=0.3)
    rightPenSpot = plt.Circle((45, 119), 0.8, color="black", alpha=0.3)

    #Draw Circles
    ax.add_patch(centreCircle)
    ax.add_patch(centreSpot)
    ax.add_patch(leftPenSpot)
    ax.add_patch(rightPenSpot)

    # Prepare Arcs
    botArc = Arc((45,11),height=18.3,width=18.3,angle=90,theta1=310,theta2=50,color="black", alpha=0.3)
    topArc = Arc((45,119),height=18.3,width=18.3,angle=90,theta1=130,theta2=230,color="black", alpha=0.3)

    # Add Arcs
    ax.add_patch(botArc)
    ax.add_patch(topArc)

    # Create the plot
    nx.draw_networkx_nodes(G, pos=pos, node_size=sz.values(), node_color=nodecolor)
    nx.draw_networkx_labels(G, pos=pos, font_size=12, font_family='sans-serif', labels=labels)
    nx.draw_networkx_edges(G, pos=pos, edgelist=weight.keys(), width=weight.values(), edge_color='dimgray')

    plt.axis([0, 100, 0, 140])
    plt.tick_params(
        axis='both',
        which='both',
        bottom=False,
        top=False,
        left=False,
        right=False,
        labelbottom=True,
        labelleft=True)
    plt.title(title, size=15)
    description = '\n\n- Node size proportional to number of touches\n- Edge between nodes indicates 4+ passes\n- Edge width proportional to number of passes'
    plt.text(45, -18, score + '\n' + moreinfo + description, ha="center", size=12)

    plt.axis('off')

    plt.draw()

    filename = team + ' Passing Map (' + home + ' vs. ' + away + ') ' + date.replace('/', '-') + '.png'

    fig.savefig('Current Week/' + filename)

    return fig

    #plt.show()


gameinfo = pd.read_csv('Game Information.csv')
teams = pd.read_csv('teams.csv')
passes = pd.read_csv('raw passes.csv')
lineups = pd.read_csv('Starting Lineups.csv')
subs = pd.read_csv('playerChanges.csv')
touches = pd.read_csv('touches.csv')
xgshots = pd.read_csv('shots with xG.csv')
rawshots = pd.read_csv('raw shots.csv')

xgshots.set_index("eventID", inplace=True)

consumer_key ="cfntUtAO597m1XKmO4GTTI5NJ"
consumer_secret ="i9oz3En3MsWsvjus91Wufhvtlzi86muGPmRQgZDcAl05tRpfuc"
access_token ="1061824758734512129-HTKpKVnTgzEI6NO10Hvcp9SmFCNMfE"
access_token_secret ="uXRkxfcciLqrK6tAytHXhuIBICgvh4MJJDz9NKi6Hi7UD"

# authentication
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

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






