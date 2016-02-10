import calc_coeff as cc 

f = open('testset.txt').readlines()

def test_proc():
    i = 0
    right_recom_1 = 0
    right_recom_2 = 0
    right_recom_3 = 0
    right_recom_t = 0
    while i < 631:
    # while i < 1:
        i += 1
        last150 = f[i:i+151]
        result = f[i-1]
        result_red = result.strip().split('  ')[8:14]
        result_blue = result.strip().split('  ')[-1]

        red = []
        blue = []

        for each in last150:
            x = each.strip().split('  ')
            this_red = x[2:8]
            this_blue = x[-1]

            red.append(this_red)
            blue.append(int(this_blue))

        blue_matrix = cc.calc_blue_list(blue)
        red_matrix = cc.calc_red_list(red)

        # test recommendation
        recommendation = [each[0] for each in red_matrix['scores'][30:33]]
        if recommendation[0] in result_red:
            right_recom_1 += 1.0
            right_recom_t += 1.0
        if recommendation[1] in result_red:
            right_recom_2 += 1.0
            right_recom_t += 1.0
        if recommendation[2] in result_red:
            right_recom_3 += 1.0
            right_recom_t += 1.0

        # test randomization
        hold1 = cc.get_lottery(red_matrix, blue_matrix, 0, True)
        hold2 = cc.get_lottery(red_matrix, blue_matrix, 0, True)
        print hold1
        print hold2
        print result_red
        print ''

    print 'first recom accu: %f' %(right_recom_1 / i)
    print 'second recom accu: %f' %(right_recom_2 / i)
    print 'third recom accu: %f' %(right_recom_3 / i)
    print 'totle recom accu: %f' %(right_recom_t / (i*3))


    # return (red, blue)

