import json
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#load Json
records = [json.loads(line) for line in open('usagov.txt')]
#build a counter
counter = {}
for x in records :
    if 'tz' in x :
        if x['tz'] in counter:
            counter[x['tz']] += 1
        else:
            counter[x['tz']] = 1

#put counter into a pandas data frame
df = pd.DataFrame(counter.items(),columns=['Country','Visits'])

#Diagnose your data
print(df.info())
print(df.shape)
print(df.describe())
print(df.columns)

# Drop na , duplicate and missing values
df1 = df.drop_duplicates()
df1 = df.dropna()
df1 = df[df['Country'] != ""]

#Seperate The city Column into Contient/city Columns

df1['Col_sep']= df1.Country.str.split('/')
df1['Contient']= df1.Col_sep.str.get(0)
df1['City']=df1.Col_sep.str.get(1)
df1['City'] = df1['City'].str.replace("_"," ")



#drop the col_sep column
del df1['Col_sep']


#plot some statistics to test our dataframe
sns.barplot(x=df1['City'],y=df1['Visits'],hue=df1['Contient'],data=df1)
plt.show()

#some data seems to be wrong as the plot show a contient with the name of Chile and another with the name of pacfic

print(df1.loc[df1.Contient == 'Pacific'] )
print(df1.loc[df1.Contient == 'Chile'] )

#the first record seems to be right , the second we must change

df2=df1
df2.set_value(43,'Contient','America')
df2.set_value(43,'Country','Chile/America')

print(df2.loc[43])

#change type of continent column to Categorial

df2['Contient'] = df2['Contient'].astype('category')

#now let's plot the Contient data after cleaning
sns.barplot(x=df2['Contient'],y=df2['Visits'],data=df2,palette='bright')
plt.show()

