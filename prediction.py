import pandas as pd
import numpy as np
from matplotlib import pyplot as plt

def exponential_smoothing(alpha, data):
    data2 = np.zeros(data.shape)
    data2[0] = data[0]
    for i in range(1, len(data2)):
        data2[i] = alpha*data[i]+(1-alpha)*data2[i-1]
    return data2

def show_data(new_year, pre_year, data, s_pre_double, s_pre_triple, alpha):
    season=np.array(data['Season'])
    wins=np.array(data['Wins'])

    plt.figure(figsize=(18, 6), dpi=80)
    plt.plot(season, wins, color='blue', label="Actual Value")
    plt.plot(new_year[:], s_pre_double[2:],color='red', label="Double Predicted Value")
    plt.plot(new_year[:], s_pre_triple[2:],color='green', label="Triple Predicted Value")
    plt.legend(loc='lower right')
    plt.title('Alpha = '+str(alpha))
    plt.xlabel('Season')
    plt.ylabel('Number of Winning')
    plt.xticks(new_year)
    plt.show()


def main(alpha):
    alpha = alpha
    pre_year = np.array(['2018-19'])
    epl_data = pd.read_csv('input/EPL_Set.csv')
    conditions = [epl_data['FTR'] == 'A', epl_data['FTR'] == 'H', epl_data['FTR'] == 'D']
    choices = [epl_data['AwayTeam'], epl_data['HomeTeam'], 'Draw']
    home_scores = [0, 3, 1]
    epl_data['Winner'] = np.select(conditions, choices)
    epl_data['HomeScore'] = np.select(conditions, home_scores)
    away_scores = [3, 0, 1]
    epl_data['AwayScore'] = np.select(conditions, away_scores)
    man = epl_data.loc[epl_data['Winner'] == 'Man United']
    count_series = man.groupby(['Season']).size()
    mancount = pd.DataFrame(data=count_series, columns=['Wins']).reset_index()
    data = mancount
    season=np.array(data['Season'])
    wins=np.array(data['Wins'])
    wins=np.insert(wins,0,values=wins[0],axis=0)
    #print(wins) #26
    s_single=exponential_smoothing(alpha,wins)
    s_double=exponential_smoothing(alpha,s_single)
    #print(s_single) #26 首位27 27
    a_double=2*s_single-s_double
    b_double = (alpha / (1 - alpha)) * (s_single - s_double)
    #print(b_double) #26 首位0 0
    s_pre_double = np.zeros(s_double.shape)
    for i in range(1,len(wins)):
        s_pre_double[i]=a_double[i-1]+b_double[i-1]
    pre_next_year=a_double[-1]+b_double[-1]*1
    pre_next_two_year=a_double[-1]+b_double[-1]*2
    #print(s_pre_double) #26 首位0 27 27
    s_pre_double=np.insert(s_pre_double,len(s_pre_double),values=np.array([pre_next_year,pre_next_two_year]),axis=0)

    s_triple = exponential_smoothing(alpha, s_double)
    a_triple = 3*s_single-3*s_double+s_triple
    b_triple = (alpha/(2*((1-alpha)**2)))*((6-5*alpha)*s_single -2*((5-4*alpha)*s_double)+(4-3*alpha)*s_triple)
    c_triple = ((alpha**2)/(2*((1-alpha)**2)))*(s_single-2*s_double+s_triple)

    s_pre_triple = np.zeros(s_triple.shape)

    for i in range(1, len(wins)):
        s_pre_triple[i] = a_triple[i-1]+b_triple[i-1]*1 + c_triple[i-1]*(1**2)

    pre_next_year = a_triple[-1]+b_triple[-1]*1 + c_triple[-1]*(1**2)
    pre_next_two_year = a_triple[-1]+b_triple[-1]*2 + c_triple[-1]*(2**2)
    s_pre_triple = np.insert(s_pre_triple, len(s_pre_triple), values=np.array([pre_next_year, pre_next_two_year]), axis=0)
    new_season = np.insert(season, len(season), values=pre_year, axis=0)
    output = np.array([new_season, s_pre_double, s_pre_triple])
    print(output)
    show_data(new_season, pre_year, data, s_pre_double, s_pre_triple,alpha)

if __name__=='__main__':
    main(0.3)
    main(0.35)
    main(0.4)
    main(0.45)
    main(0.5)