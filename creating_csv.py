def create_csv(features_name, features_values):
    file = open("players_stats.csv", "w", newline='')
    writer = csv.writer(file)
    data=[]
    data.append(features_name)
    player1_team1=features_values[0:14]
    data.append(player1_team1)
    player2_team1 = features_values[14:28]
    data.append(player2_team1)
    player3_team1 = features_values[28:42]
    data.append(player3_team1)
    player4_team1 = features_values[42:56]
    data.append(player4_team1)
    player5_team1 = features_values[56:70]
    data.append(player5_team1)
    player1_team2 = features_values[70:84]
    data.append(player1_team2)
    player2_team2 = features_values[84:98]
    data.append(player2_team2)
    player3_team2 = features_values[98:112]
    data.append(player3_team2)
    player4_team2 = features_values[112:126]
    data.append(player4_team2)
    player5_team2 = features_values[126:140]
    data.append(player5_team2)
    for string in data:
        del string[0:3]
    for string in data:
        del string[2:5]
    for string in data:
        del string[-3:-1]
    for row in data:
        writer.writerow(row)