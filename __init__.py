import sys
import csv
# properties initialization
dates = {"Dragons": "March 17, 1pm", "Sharks": "March 17, 3pm", "Raptors": "March 18, 1pm"}
teams = [("Dragons", []), ("Sharks", []), ("Raptors", [])]


# load csv file from filename and return the list of dictionary
def load_file(filename):
    with open(filename) as csvfile:
        csvreader = csv.DictReader(csvfile)
        my_list = []
        for row in csvreader:
            my_list.append(row)
        return my_list


# form the team by their experience and return a list of formed team
def form_team(player_list, teams):
    exp_index = 0
    no_exp_index = 0
    number_of_teams = len(teams)
    for player in player_list:
        if player['Soccer Experience'] == 'YES':
            (team_name, team_list) = teams[exp_index]
            team_list += [player]
            exp_index += 1
        else:
            (team_name, team_list) = teams[no_exp_index]
            team_list += [player]
            no_exp_index += 1
        if exp_index >= number_of_teams:
            exp_index = 0
        if no_exp_index >= number_of_teams:
            no_exp_index = 0
    return player_list


# generate letters to the guardians
def generate_personalized_letters(teams, dates):
    letter_template = """
Team practice of {team}

{time}, {name} is going to attend the team practice,
I believe your kids gain confidence and a love for the game through positive feedback from coaches, and other players.
Skill level develops at different rates for kids, but effort and having fun can always be achieved.
I try to always provide positive feedback for effort.

Sincerely,

Vincent de Soshified
    """
    for (team_name, members) in teams:
        for member in members:
            with open('{}.txt'.format(member['Guardian Name(s)']), 'w') as file:
                file.write(letter_template.format(team=team_name, name=member['Name'], time=dates[team_name]))


# swap player's to limit each team’s average height is within 1 inch of the others
def averaging_height(teams):
    def max_member(team, is_exp):
        max_height = 0
        for member in team:
            if is_exp ^ (member['Soccer Experience'] == 'NO') and float(member['Height (inches)']) > max_height:
                max_height = float(member['Height (inches)'])
                max_member = member
        return max_member

    def min_member(team, is_exp):
        min_height = sys.float_info.max
        for member in team:
            if is_exp ^ (member['Soccer Experience'] == 'NO') and float(member['Height (inches)']) < min_height:
                min_height = float(member['Height (inches)'])
                min_member = member
        return min_member

    def swap(high_team, low_team):
        is_exp = False
        if float(max_member(high_team, True)['Height (inches)']) - float(min_member(low_team, True)['Height (inches)']) > float(max_member(high_team, False)['Height (inches)']) - float(min_member(low_team, False)['Height (inches)']):
            is_exp = True
        high_member = max_member(high_team, is_exp)
        low_member = min_member(low_team, is_exp)
        (high_team[high_team.index(high_member)], low_team[low_team.index(low_member)]) = (low_member, high_member)

    avg_heights = []
    avg_height = 0
    for (team_name, members) in teams:
        for member in members:
            avg_height += float(member['Height (inches)'])
        avg_height /= len(members)
        avg_heights += [avg_height]
        print("{} avg_height = {}".format(team_name, avg_height))
    while max(avg_heights) - min(avg_heights) > 1:
        print('CK1')
        (team_name, high_members) = teams[avg_heights.index(max(avg_heights))]
        (team_name, low_members) = teams[avg_heights.index(min(avg_heights))]
        swap(high_members, low_members)


def print_teams():
    avg_height = 0
    for (team_name, members) in teams:
        for member in members:
            avg_height += float(member['Height (inches)'])
            print("{name} \t{exp} {height}".format(name=member['Name'], exp=member['Soccer Experience'], height=member['Height (inches)']))
        avg_height /= len(members)
        print("{} avg_height = {}".format(team_name, avg_height))

if __name__ == '__main__':
    player_list = load_file('soccer_players.csv')
    player_list = form_team(player_list, teams)
    #generate_personalized_letters(teams, dates)
    averaging_height(teams)
    #print_teams()
