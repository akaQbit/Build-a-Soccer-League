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
# form the team by their experience and return a list of formed team
def form_team_with_height_match(player_list, teams):
    def error_value(current_total, next, avg, num):
        return abs((current_total + next) / num - avg)

    def fill_team(team, team_fragment, fragment_size, height_average):
        current_value = 0
        while len(team_fragment) < fragment_size:
            min_error = sys.float_info.max
            for member in team:
                current_error = error_value(current_value, float(member["Height (inches)"]), height_average, len(team_fragment) + 1)
                if current_error < min_error:
                    min_error_member = member
                    min_error = current_error
                    current_value += float(member["Height (inches)"])
            team_fragment += [min_error_member]
            team.remove(min_error_member)
        return team

    def print_team_avg(team_fragment):
        for fm in team_fragment:
            print()
            avg = 0
            for m in fm:
                avg += float(m['Height (inches)'])
                print('{} : {}'.format(m['Name'], m['Height (inches)']))
            avg /= len(fm)
            print('average = {}'.format(avg))

    def join_fragments(no_exp_frags, exp_frags, expected_average):
        output_list = []

        def get_frag_avg(frag):
            avg = 0
            for f in frag:
                avg += f['Height (inches)']
            return avg / len(frag)

        def frag_merge_error(frag1, frag2, e_avg):
            avg = 0
            for f in frag1:
                avg += float(f['Height (inches)'])
            for f in frag2:
                avg += float(f['Height (inches)'])
            avg /= (len(frag1) + len(frag2))
            return abs(avg - e_avg)

        def frag_merge(frag1, frag2):
            temp_list = []
            for f in frag1:
                temp_list.append(f)
            for f in frag2:
                temp_list.append(f)
            return temp_list

        for no_exp_frag in no_exp_frags:
            min_error = sys.float_info.max
            for exp_frag in exp_frags:
                error = frag_merge_error(no_exp_frag, exp_frag, expected_average)
                if error < min_error:
                    min_error = error
                    merge_target = exp_frag
            output_list.append(frag_merge(no_exp_frag, merge_target))
            exp_frags.remove(merge_target)
        return output_list

    exp_team = []
    exp_team_fragments = []
    no_exp_team = []
    no_exp_team_fragments = []
    players_average_height = 0
    number_of_teams = len(teams)

    for player in player_list:
        players_average_height += float(player["Height (inches)"])
        if player['Soccer Experience'] == 'YES':
            exp_team.append(player)
        else:
            no_exp_team.append(player)
    players_average_height /= len(player_list)

    number_of_exp_member_per_fragment = len(exp_team) / number_of_teams
    number_of_no_exp_member_per_fragment = len(no_exp_team) / number_of_teams

    while len(exp_team) > 0:
        exp_team_fragment = []
        fill_team(exp_team, exp_team_fragment, number_of_exp_member_per_fragment, players_average_height)
        exp_team_fragments += [exp_team_fragment]
    while len(no_exp_team) > 0:
        no_exp_team_fragment = []
        fill_team(no_exp_team, no_exp_team_fragment, number_of_no_exp_member_per_fragment, players_average_height)
        no_exp_team_fragments += [no_exp_team_fragment]

    team_list = join_fragments(exp_team_fragments, no_exp_team_fragments, players_average_height)
    for index in range(len(teams)):
        (output_team_name, output_team_list) = teams[index]
        teams[index] = (output_team_name, team_list[index])


# for visualization of data/ debugging
def print_teams():
    total_avg = 0
    total_count = 0
    for (team_name, members) in teams:
        avg_height = 0
        print('----- {} -----'.format(team_name))
        for member in members:
            total_avg += float(member['Height (inches)'])
            total_count += 1
            avg_height += float(member['Height (inches)'])
            print("{name} \t{exp} {height}".format(name=member['Name'], exp=member['Soccer Experience'], height=member['Height (inches)']))
        avg_height /= len(members)
        print("{} avg_height = {}".format(team_name, avg_height))
        print()
    print('Entire team avg_height = {}'.format(total_avg / total_count))


# main function entry point
if __name__ == '__main__':
    player_list = load_file('soccer_players.csv')
    form_team_with_height_match(player_list, teams)
    generate_personalized_letters(teams, dates)
    print_teams()
