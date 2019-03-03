import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

records = []
#load Json
records = [json.loads(line) for line in open('usagov.txt')]

rec = pd.DataFrame(records)
print(rec.head())
print(rec.info())
print(rec.describe())
print(rec.columns)

rec = rec[['a','tz']]
rec.columns = ['Os','Region']

# Searching for Windows / Not Windows

rec['Windows'] = rec['Os'].str.contains('Windows').astype(str)
rec['Windows'] = rec['Windows'].str.replace('True','Windows')
rec['Windows'] = rec['Windows'].str.replace('False','Not_Windows')

# drop nan and missing values
rec = rec.dropna(how='any')
rec = rec[rec['Region'] != '']
rec = rec.reset_index()
print(rec.head())
print(rec.info())
print(rec.describe())
print(rec.columns)


# Grouping By Windows/Region Columns

rec2 = pd.DataFrame(rec.groupby(['Windows','Region']).size())
rec2 = rec2.reset_index()
rec2['Count'] = rec2[0]
del rec2[0]

# Using Pivot to Tidy Data and make a column into rows and repalce nan with 0.0

rec2 = rec2.pivot(index='Region',columns='Windows',values = 'Count')

rec2 =rec2.fillna(0)

# Building Cumulative visits Column

rec2['Total_Visits'] = rec2['Not_Windows'] + rec2['Windows']

# Creating a Continent Column
rec2['split'] = rec2.index.str.split('/',1)
rec2['Continent'] = rec2.split.str.get(0)
print(rec2.Continent.value_counts())
del rec2['split']


# Fixing Continent Column as it contains Chile as a Continent

print(rec2.loc[rec2.Continent == 'Chile'].index.get_values() )
rec2.set_value(['Chile/Continental'],'Continent','America')
rec2['Continent'] = rec2['Continent'].astype('category')

# Getting Some Statistical Insights

w_p = rec2['Windows']/rec2['Total_Visits']
nw_p = rec2['Not_Windows']/rec2['Total_Visits']

g = dict(rec2.groupby('Continent').Total_Visits.sum())
g1 = dict(rec2.groupby('Continent').Windows.sum())
g2 = dict(rec2.groupby('Continent').Not_Windows.sum())

g_names = list(g.keys())
g_values = list(g.values())
g_values1 = list(g1.values())
g_values2 = list(g2.values())

c = rec2.Continent.value_counts().to_dict()
c_names =list(c.keys())
c_values = list(c.values())


# Plotting



sns.scatterplot(x=rec2['Windows'],data=rec2,y = rec2['Not_Windows'],hue=rec2['Continent'])
#plt.title("Windows to Non Windows Visits For each Continent")
plt.show()

plt.subplot(2,2,1)
plt.bar(range(len(c)),c_values,tick_label=c_names,color ='green')
plt.title('The Contribution Of Every Continent to the Dataset')

plt.subplot(2,2,2)

plt.bar(range(len(g)),g_values,tick_label =g_names)
plt.title('The Sum Of Total Visits By Continent')

plt.subplot(2,2,3)

plt.bar(range(len(g1)),g_values1,tick_label =g_names)
plt.title('The Sum Of Windows Visits By Continent')

plt.subplot(2,2,4)
plt.bar(range(len(g2)),g_values2,tick_label =g_names)
plt.title('The Sum Of Non Windows Visits By Continent')


plt.show()

