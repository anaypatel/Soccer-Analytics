import pandas as pd
import networkx as nx
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt
from matplotlib.patches import Arc
import tweepy
import numpy as np

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
