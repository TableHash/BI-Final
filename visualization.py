import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

epl_data = pd.read_csv('input/EPL_Set.csv')

conditions=[epl_data['FTR']=='A',epl_data['FTR']=='H',epl_data['FTR']=='D']
choices = [epl_data['AwayTeam'],epl_data['HomeTeam'],'Draw']
home_scores=[0,3,1]
epl_data['Winner']=np.select(conditions,choices)
epl_data['HomeScore']=np.select(conditions,home_scores)
away_scores=[3,0,1]
epl_data['AwayScore']=np.select(conditions,away_scores)

print(epl_data.tail())

#Who are the teams that win most?
tmp=epl_data.loc[:,['Season','Winner']]
win = tmp.groupby(['Season', 'Winner']).size().reset_index(name='counts')
sort = win.sort_values(['Season', 'counts'], ascending=[True, False])
no_draws = sort[sort.Winner.str.contains('Draw')==False].reset_index()
most_wins= no_draws.groupby('Season').head(1)
print(most_wins)
titles= most_wins['Winner'].value_counts().reset_index()
print(titles)
plt.figure(figsize=(15, 10))
sns.barplot(x='index', y='Winner', data=titles)
plt.show()


#How many times do teams win each season?
a=epl_data.loc[:,['Season','Winner']]
b=a.groupby(['Season', 'Winner']).size().reset_index(name='Times')
c=b.sort_values(['Season', 'Times'], ascending=[True, False])
d=c[c.Winner.str.contains('Draw')==False].reset_index()
print(d)
plt.figure(figsize=(17, 6))
sns.countplot(x='Times' ,data=d)
plt.xticks(rotation='vertical')
plt.show()


#How do teams perform as hometeams?
print(epl_data["HomeTeam"].value_counts(dropna=False))
plt.figure(figsize=(51, 18))
sns.countplot(x='HomeTeam',hue='HomeScore', data=epl_data)
plt.xticks(rotation='vertical')
plt.show()

#How do teams perform as awayteams?
plt.figure(figsize=(102, 36))
sns.countplot(x='AwayTeam',hue='AwayScore',palette="Set2", data=epl_data)
plt.xticks(rotation='vertical')
plt.show()

#How many do all the teams have their home goals?
plt.rcParams['figure.figsize'] = [18, 15]
temp=epl_data[['HomeTeam','FTHG']].groupby('HomeTeam').sum().sort_values(by='FTHG',ascending= True)
temp.plot.barh(color='purple')
plt.title('')
plt.show()

#How many do all the teams have their away goals?
plt.rcParams['figure.figsize'] = [18, 15]
temp=epl_data[['AwayTeam','FTAG']].groupby('AwayTeam').sum().sort_values(by='FTAG',ascending= True)
temp.plot.barh(color='blue')
plt.title('')
plt.show()

#How does Man United score each game each season as the hometeam?
utd = epl_data.groupby(['Season','HomeTeam']).FTHG.sum().reset_index()
utd = utd.loc[utd['HomeTeam'] == 'Man United']
plt.rcParams['figure.figsize'] = [20, 18]
sns.barplot(x='Season', y='FTHG', data=utd)
plt.show()

#How does Man United score each game each season as the awayteam?
utd = epl_data.groupby(['Season','AwayTeam']).FTAG.sum().reset_index()
utd = utd.loc[utd['AwayTeam'] == 'Man United']
plt.rcParams['figure.figsize'] = [20, 18]
sns.barplot(x='Season', y='FTAG', data=utd)
plt.show()

#What about Arsenal as the hometeam?
ars = epl_data.groupby(['Season','HomeTeam']).FTHG.sum().reset_index()
ars = ars.loc[ars['HomeTeam'] == 'Arsenal']
plt.rcParams['figure.figsize'] = [20, 20]
sns.barplot(x='Season', y='FTHG', data=ars)
plt.show()

#What about Arsenal as the awayteam?
ars = epl_data.groupby(['Season','AwayTeam']).FTAG.sum().reset_index()
ars = ars.loc[ars['AwayTeam'] == 'Arsenal']
plt.rcParams['figure.figsize'] = [20, 20]
sns.barplot(x='Season', y='FTAG', data=ars)
plt.show()

#How many times does Chelsea win each season?
chelsea = epl_data.loc[epl_data['Winner'] == 'Chelsea']
count_series = chelsea.groupby(['Season']).size()
mancount = pd.DataFrame(data=count_series, columns=['Wins']).reset_index()
plt.figure(figsize=(20, 20))
plt.plot('Season', 'Wins', data=mancount, marker='o',linewidth=3, color='skyblue')
plt.show()

#How many times does Man United win each season?
man = epl_data.loc[epl_data['Winner'] == 'Man United']
count_series = man.groupby(['Season']).size()
mancount = pd.DataFrame(data=count_series, columns=['Wins']).reset_index()
print(mancount)
plt.figure(figsize=(20, 20))
plt.plot('Season', 'Wins', data=mancount, marker='o',linewidth=3, color='red')
plt.show()

#How does Man United perform when he faces Arsenal?
man_ars = epl_data[((epl_data['HomeTeam']=='Man United' )& (epl_data['AwayTeam']=='Arsenal'))|((epl_data['HomeTeam']=='Arsenal') & (epl_data['AwayTeam']=='Man United'))].groupby(['Winner'])['Winner'].count()
labels = (np.array(man_ars.index))
sizes = (np.array((man_ars / man_ars.sum())*100))
colors = ['gold', 'lightskyblue','lightgreen']
plt.subplots(figsize=(10, 8))
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
plt.title("Win Ratio Between Man United and Arsenal")
plt.show()

#How does Man United perform when he faces Man City?
man_derby = epl_data[((epl_data['HomeTeam']=='Man United' )& (epl_data['AwayTeam']=='Man City'))|((epl_data['HomeTeam']=='Man City') & (epl_data['AwayTeam']=='Man United'))].groupby(['Winner'])['Winner'].count()
labels = (np.array(man_derby.index))
sizes = (np.array((man_derby / man_derby.sum())*100))
colors = ['skyblue', 'lightgreen', 'gold']
plt.subplots(figsize=(10, 8))
plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True, startangle=90)
plt.title("Win Ratio Between Man United and Man City")
plt.show()