import scipy as sp 
import numpy as np 
import scipy.stats as stats 

data = sp.genfromtxt("recent100.txt", delimiter="\t")

ball1 = data[:,0]

ball_mass = [0]
# get first ball mass 
ball_freq = stats.itemfreq(ball1)
ball_freq /= len(ball1)
for each in ball_freq:
    ball_mass.append(each[1])

ball_mass = np.array(ball_mass)
ball_mean = 1 / 33.0
ball_mass -= ball_mean 

# second Ball
def round_balls(round, lacking):
    balls = data[:,round]
    conditions = data[:,0] != lacking
    i = 1
    while i < round:
        conditions *= (data[:,i] != lacking)
        i += 1
    return data[conditions]

numbers = np.arange(1, 34)
for each in numbers:
    i = 1
    while i < 6:
        middle_data = round_balls(i, each)
        middle_balls = middle_data[:,i]
        middle_freq = stats.itemfreq(middle_balls)
        this_mass = 0.0
        for unit_freq in middle_freq:
            if each == unit_freq[0]:
                unit_freq = unit_freq[1] / len(middle_balls)
                this_mass = unit_freq 
        middle_mean = 1.0 / (33-i)
        this_mass -= middle_mean
        ball_mass[each] += this_mass
        i += 1

# final round
# print 'final round'
# print ball_mass

picks = []
polls = list(ball_mass + 6.0/33)[1:]
pools = range(1,34)
print polls
polls = np.array(polls)
polls /= sum(polls)
i = 0
while i < 6:
    this_ball = np.random.choice(pools, 1, p=polls)
    print this_ball
    picks += this_ball
    polls = np.delete(polls, polls.index(this_ball))
    pools = np.delete(pools, pools.index(this_ball))
    print pools
    polls /= sum(polls)
    i+=1

print picks