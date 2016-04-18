import csv


def load_file(filename):
    with open(filename) as csvfile:
        spamreader = csv.DictReader(csvfile)
        my_list = []
        for row in spamreader:
            print(row)
            my_list.append(row)
        return my_list


l = load_file('soccer_players.csv')
print(len(l))
