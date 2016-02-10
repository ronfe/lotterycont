import string, pprint
import operator
import numpy as np

def get_first(balls):
    # reform data
    balls_num = []
    balls_dist = []
    for each in balls:
        balls_num.append(each[0])
        balls_dist.append(each[1])

    # get probability distribution
    balls_dist = np.array(balls_dist)
    balls_dist = balls_dist / float(np.sum(balls_dist))

    # choose one ball
    first_ball = np.random.choice(balls_num, 1, p=balls_dist)
    return first_ball[0]

def get_rest(params, showed_balls):
    # initialize customed prob
    custom_prob = np.array([0] * 34)

    # fill up the prob
    for each in showed_balls:
        this_ball = int(each)
        this_ori_prob = np.array(params[this_ball])
        custom_prob = custom_prob + this_ori_prob

    for each in showed_balls:
        custom_prob[each] = 0

    balls_dist = np.array(custom_prob)
    balls_dist = balls_dist / float(np.sum(balls_dist))

    this_rest = np.random.choice(range(34), 1, p=balls_dist)

    return this_rest[0]

# rand_index receives an int, 0 for randomize, >0 for fixed index
# if repeat_option, randomization will choose first repeated number
def get_lottery(calc_result, blue_result, rand_index, repeat_option):
    result = []
    blue = 0

    # get blues
    blue_dist = np.array(blue_result)
    blue_dist = blue_dist / float(np.sum(blue_dist))
    blue = np.random.choice(range(17), 1, p=blue_dist)
    blue = blue[0]

    if rand_index != 0:
        first = int(calc_result['scores'][-rand_index][0])
        result.append(first)

        params = calc_result['params']
        last_ball = first
        i = 1
        while i < 6:
            this_dist = np.array(params[last_ball])
            next_ball = this_dist.argsort()[-rand_index:][::-1][-1]
            result.append(next_ball)
            last_ball = next_ball
            i += 1
    else:
        if repeat_option:
            temp_pool = []
            first = get_first(calc_result['scores'])
            while not first in temp_pool:
                temp_pool.append(first)
                first = get_first(calc_result['scores'])
            result.append(int(first))

            i = 1
            params = calc_result['params']
            while i < 6:
                temp_pool = []
                this_temp = get_rest(params, result)
                while not this_temp in temp_pool:
                    temp_pool.append(this_temp)
                    this_temp = get_rest(params, result)
                result.append(this_temp)
                i += 1
        else:
            result.append(int(get_first(calc_result['scores'])))

            i = 1
            params = calc_result['params']
            while i < 6:
                result.append(get_rest(params, result))
                i += 1
    return (sorted(result), blue)



# outer layer
def outer(calc_result):
    pool = set([])
    result = set([])
    while len(result) <= 6:
        this_way = set(get_lottery(calc_result, 0, True))
        result = result.union(this_way.intersection(pool))
        pool = pool.union(this_way)

    return sorted(list(result))

def calc_blue():
    scores = [0]*17

    f = open('recent100blue.txt').readlines()

    for each in f:
        b = int(each.strip())
        scores[b] += 1

    return scores

def calc_blue_list(blue_list):
    scores = [0]*17

    for each in blue_list:
        scores[each] += 1

    return scores

def calc_red_list(red_list):
    scores = {}
    params = [[]]

    i = 1
    while i <= 33:
        if i < 10:
            temp_txt = '0' + str(i)
        else:
            temp_txt = str(i)

        scores[temp_txt] = 0
        params.append([0]*34)
        i+= 1

    for each in red_list:
        a1,a2,a3,a4,a5,a6 = each
        scores[a1] += 42
        scores[a2] += 30
        scores[a3] += 20
        scores[a4] += 12
        scores[a5] += 6
        scores[a6] += 2

        a1 = string.atoi(a1)
        a2 = string.atoi(a2)
        a3 = string.atoi(a3)
        a4 = string.atoi(a4)
        a5 = string.atoi(a5)
        a6 = string.atoi(a6)

        params[a1][a2] += 30
        params[a1][a3] += 24
        params[a1][a4] += 18
        params[a1][a5] += 12
        params[a1][a6] += 6

        params[a2][a3] += 20
        params[a2][a4] += 15
        params[a2][a5] += 10
        params[a2][a6] += 5

        params[a3][a4] += 12
        params[a3][a5] += 8
        params[a3][a6] += 4

        params[a4][a5] += 6
        params[a4][a6] += 3

        params[a5][a6] += 2

    sorted_scores = sorted(scores.items(), key=operator.itemgetter(1))
    return {'scores': sorted_scores, 'params': params}

def calc_red():
    scores = {}
    params = [[]]

    i = 1
    while i <= 33:
        if i < 10:
            temp_txt = '0' + str(i)
        else:
            temp_txt = str(i)

        scores[temp_txt] = 0
        params.append([0]*34)
        i+= 1

    f = open('recent100.txt').readlines()

    for each in f:
        a1,a2,a3,a4,a5,a6 = each.strip().split('\t')
        scores[a1] += 42
        scores[a2] += 30
        scores[a3] += 20
        scores[a4] += 12
        scores[a5] += 6
        scores[a6] += 2

        a1 = string.atoi(a1)
        a2 = string.atoi(a2)
        a3 = string.atoi(a3)
        a4 = string.atoi(a4)
        a5 = string.atoi(a5)
        a6 = string.atoi(a6)

        params[a1][a2] += 30
        params[a1][a3] += 24
        params[a1][a4] += 18
        params[a1][a5] += 12
        params[a1][a6] += 6

        params[a2][a3] += 20
        params[a2][a4] += 15
        params[a2][a5] += 10
        params[a2][a6] += 5

        params[a3][a4] += 12
        params[a3][a5] += 8
        params[a3][a6] += 4

        params[a4][a5] += 6
        params[a4][a6] += 3

        params[a5][a6] += 2
    
    sorted_scores = sorted(scores.items(), key=operator.itemgetter(1))
    return {'scores': sorted_scores, 'params': params}