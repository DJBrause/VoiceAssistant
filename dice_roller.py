import random


def roll_dice(x):
    results_dict = {'ones': 0, 'twos': 0, 'threes': 0, 'fours': 0, 'fives': 0, 'sixes': 0}

    for r in range(x):
        roll = random.randint(1, 6)
        if roll == 1:
            x = results_dict['ones']
            x += 1
            results_dict['ones'] = x
        elif roll == 2:
            x = results_dict['twos']
            x += 1
            results_dict['twos'] = x
        elif roll == 3:
            x = results_dict['threes']
            x += 1
            results_dict['threes'] = x
        elif roll == 4:
            x = results_dict['fours']
            x += 1
            results_dict['fours'] = x
        elif roll == 5:
            x = results_dict['fives']
            x += 1
            results_dict['fives'] = x
        elif roll == 6:
            x = results_dict['sixes']
            x += 1
            results_dict['sixes'] = x

    return results_dict
