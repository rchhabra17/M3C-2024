import pandas as pd
import numpy as np
import math
import matplotlib.pyplot as plt

pricing_increase = [0.05,0.1,0.15,0.2,0.25,0.26,0.27,0.28,0.29,0.3]
carrying_capacity = 535249

def one_year(affordable_housing,current_homeless,built_houses,vacant_units, # MODEL INPUT VALUES
             ND_loss,ER_loss,new_immigrants, # STRENGTH TESTING
             const_price=373285,given_budget=339000000,income=42635): # DEFAULT VALUES
    budget = (given_budget + sum(affordable_housing[i]*pricing_increase[min(i,len(pricing_increase)-1)]*income 
                                 for i in range(len(affordable_housing)))) * (1-ER_loss)

    temp_housing = [round(i * (1-ND_loss)) for i in affordable_housing]
    affordable_housing = temp_housing
    built_houses *= (1-ND_loss)
    homeless_immigrants = (new_immigrants-vacant_units) * (vacant_units < new_immigrants)
    new_housing = budget//const_price
    if(new_housing > carrying_capacity - built_houses):
        return [],0,False
    affordable_housing.insert(0,new_housing)
    return affordable_housing,homeless_immigrants,True


def simulate_housing(ideal_homeless,ideal_time, # TOOL SPECIFIC ANALYSIS
                     homeless_data,built_houses_data,vacant_units_data, # MODEL INPUT VALUES
                     ND_loss_data,ER_loss_data,new_immigrants_data, # STRENGTH TESTING
                     const_price=373285,given_budget=339000000,income=42635): # DEFAULT VALUES
    all_housing = []
    homeless_immigrants = 0
    for i in range(0,ideal_time):
        all_housing,new_homeless_immigrants,success = one_year(all_housing,homeless_data[i]-sum(all_housing)+homeless_immigrants,built_houses_data[i],
                                                               vacant_units_data[i],ND_loss_data[i],ER_loss_data[i],new_immigrants_data[i],
                                                               const_price,given_budget,income)
        homeless_immigrants += new_homeless_immigrants
        if(not success):
            return [],0,False
        if(sum(all_housing) + ideal_homeless > homeless_data[i]+homeless_immigrants):
            return all_housing,homeless_data[i]+homeless_immigrants-sum(all_housing),True
    return [],0,False


def optimal_housing(ideal_homeless,ideal_time,homeless_data,built_houses_data,vacant_units_data, ND_loss_data,ER_loss_data,new_immigrants_data):
    print()
    print("Admissible # of Homeless People:",ideal_homeless)
    print("Ideal Time:",ideal_time)
    print()
    print("Calculating...")
    print()
    optimal_plan = []
    curr_homeless = 0
    budget_percent = 1.05
    success = True
    while(success):
        budget_percent -= 0.05
        previous_plan = optimal_plan
        prev_homeless = curr_homeless
        optimal_plan,curr_homeless,success = simulate_housing(ideal_homeless,ideal_time,
                     homeless_data,built_houses_data,vacant_units_data,
                     ND_loss_data,ER_loss_data,new_immigrants_data,given_budget=339000000*budget_percent)
    if(not previous_plan):
        print("Not possible in the given amount of time!")
        print("To Fix: Increase Homeless Threshold OR Increase Time")
        return 0
    print("Success!")
    print("You can spend",str(math.ceil((budget_percent+0.05)*100))+"% of your urban development budget on affordable housing")
    print()
    for i in range(1,len(previous_plan)+1):
        print(str(2022+i)+":",int(previous_plan[-i])," new affordable housing units")
    print()
    print("People in Affordable Housing:",int(sum(previous_plan)))
    print("Homeless after",ideal_time,"years:",int(prev_homeless),"people")
    print()
    return budget_percent+0.05


homeless_data = [13731, 13656, 13778, 14149, 14505, 14741, 14938, 15172, 15427, 15668, 15889, 16105, 16323, 16538, 16747, 16949, 17148, 17343, 17535, 17722, 17905, 18084, 18259, 18431, 18599, 18763, 18924, 19082, 19236, 19388, 19535, 19680, 19822, 19961, 20097, 20229, 20360, 20487, 20612, 20734, 20853, 20970, 21085, 21197, 21307, 21414, 21519, 21622, 21723, 21822]
built_houses_data = [381633, 389184, 396499, 403572, 410397, 416973, 423297, 429368, 435188, 440759, 446083, 451164, 456007, 460617, 465001, 469163, 473113, 476855, 480398, 483750, 486917, 489908, 492730, 495390, 497897, 500257, 502478, 504566, 506529, 508373, 510105, 511730, 513255, 514685, 516025, 517281, 518458, 519560, 520591, 521557, 522460, 523306, 524096, 524836, 525527, 526173, 526777, 527341, 527868, 528361, 528821, 529251, 529652, 530027, 530377, 530703, 531008, 531293, 531558, 531806]
vacant_units_data = [23414, 23761, 24108, 24455, 24802, 25149, 25496, 25843, 26190, 26537, 26884, 27231, 27578, 27925, 28272, 28619, 28966, 29313, 29660, 30007, 30354, 30701, 31048, 31395, 31742, 32089, 32436, 32783, 33130, 33477, 33824, 34171, 34518, 34865, 35212, 35559, 35906, 36253, 36600, 36947, 37294, 37641, 37988, 38335, 38682, 39029, 39376, 39723, 40070, 40417, 40764, 41111, 41458, 41805, 42152, 42499, 42846, 43193, 43540, 43887]



x1 = []
y1 = []
c1 = []
x2 = []
y2 = []
c2 = []
for i in range(500,5250,250):
    x1.append(i)
    y1.append(optimal_housing(i,15,homeless_data,built_houses_data,vacant_units_data,[0]*60,[0]*60,[0]*60))
    if(y1[-1]): 
        c1.append('g')
    else:
        c1.append('r')

for i in range(10,45,5):
    x2.append(i)
    y2.append(optimal_housing(2000,i,homeless_data,built_houses_data,vacant_units_data,[0]*60,[0]*60,[0]*60))
    if(y2[-1]): 
        c2.append('g')
    else:
        c2.append('r')

figure, axis = plt.subplots(1, 2)
axis[0].scatter(x1,y1,c=c1)
axis[0].set_title("Budget Percentage At 15 Year Time")
axis[0].set_ylabel("% of Budget Used on Housing / Year")
axis[0].set_xlabel("# of Admissibile Homeless People")
axis[1].scatter(x2,y2,c=c2)
axis[1].set_title("Budget Percentage At 2000 Admissible Homeless")
axis[1].set_xlabel("Time Given")
plt.show()








