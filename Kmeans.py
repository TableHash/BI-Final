import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from sklearn.cluster import KMeans

sc = MinMaxScaler(feature_range = (0,1))

epl_data = pd.read_csv('input/EPL_Set.csv')


conditions=[epl_data['FTR']=='A',epl_data['FTR']=='H',epl_data['FTR']=='D']
choices = [epl_data['AwayTeam'],epl_data['HomeTeam'],'Draw']
home_scores=[0,3,1]
epl_data['Winner']=np.select(conditions,choices)
epl_data['HomeScore']=np.select(conditions,home_scores)
away_scores=[3,0,1]
epl_data['AwayScore']=np.select(conditions,away_scores)

half_conditions=[epl_data['HTR']=='A',epl_data['HTR']=='H',epl_data['HTR']=='D']
epl_data['Half_Winner']=np.select(half_conditions,choices)


#How does Man United score each game each season as the hometeam?
utd = epl_data.groupby(['Season','HomeTeam']).FTHG.sum().reset_index()
utd = utd.loc[utd['HomeTeam'] == 'Man United']
FTHG=np.array(utd['FTHG'])[2:]
print(FTHG)

half_utd=epl_data.groupby(['Season','HomeTeam']).HTHG.sum().reset_index()
half_utd=half_utd.loc[half_utd['HomeTeam']=='Man United']
HTHG=np.array(half_utd['HTHG'])[2:]
print(HTHG)

#How does Man United score each game each season as the awayteam?
utd = epl_data.groupby(['Season','AwayTeam']).FTAG.sum().reset_index()
utd = utd.loc[utd['AwayTeam'] == 'Man United']
FTAG=np.array(utd['FTAG'])[2:]
print(FTAG)

half_utd=epl_data.groupby(['Season','AwayTeam']).HTAG.sum().reset_index()
half_utd=half_utd.loc[half_utd['AwayTeam']=='Man United']
HTAG=np.array(half_utd['HTAG'])[2:]
print(HTAG.size)

#How many times does Man United win each season?
man = epl_data.loc[epl_data['Winner'] == 'Man United']
count_series = man.groupby(['Season']).size()
count=np.array(count_series)[2:]
print(count.size)

man_half = epl_data.loc[epl_data['Half_Winner'] == 'Man United']
count_series_half = man_half.groupby(['Season']).size()
half_count=np.array(count_series_half)
print(half_count)


x=np.array(list(zip(HTAG,count))).reshape(len(HTAG),2)
print(x)


S1=pd.Series(count)
S2=pd.Series(half_count)
S3=pd.Series(HTHG)
S4=pd.Series(FTHG)
S5=pd.Series(FTAG)
S6=pd.Series(HTAG)
print(S1.corr(S2))
print(S1.corr(S3))
print(S1.corr(S4))
print(S1.corr(S5))
print(S1.corr(S6))



#x = sc.fit_transform(x)

print(x)


kmeans=KMeans(n_clusters=3)
kmeans.fit(x)
print(kmeans.labels_)

plt.figure(figsize=(5,5))
colors=['r','g','b']
markers=['o','s','d']
plt.title("HTAG(x) VS COUNT(y)")
for i,j in enumerate(kmeans.labels_):
    plt.plot(x[i][0],x[i][1],color=colors[j],marker=markers[j],ls='None')
plt.show()

plt.figure(figsize=(5,5))
num_list=[S1.corr(S2),S1.corr(S3),S1.corr(S4),S1.corr(S5),S1.corr(S6)]
plt.bar(range(len(num_list)),num_list,color='lightskyblue',edgecolor='white',
        tick_label=['half_count','HTHG','FTHG','FTAG','HTAG'])
plt.title('The Correlation Coefficient with winning ratio')
plt.show()
