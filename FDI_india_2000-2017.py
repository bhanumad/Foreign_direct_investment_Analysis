#!/usr/bin/env python
# coding: utf-8

# ### Foreign Direct Investment Analysis

# #### Importing require libraries

# In[1]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# In[3]:


# extract csv file from inner system 

FDI = pd.read_csv('FDI_data.csv')
FDI.style.set_caption('FDI (amount in USD million)').format(precision=2)


# In[4]:


FDI.info()


# In[5]:


FDI.columns


# In[6]:


for i in FDI['Sector']:
    print(i)


# ##### Observation - There are two type of column,
# 1) Sector column contains 63 different sectors has received FDI from 2000-01 to 2016-17.
# 
# 2) Year column shows amount recieved to particular sector from foreign from 2000-01 to 2016-17.

# In[7]:


Year = ['2000-01', '2001-02', '2002-03', '2003-04', '2004-05',
       '2005-06', '2006-07', '2007-08', '2008-09', '2009-10', '2010-11',
       '2011-12', '2012-13', '2013-14', '2014-15', '2015-16', '2016-17']
Sectors = ['Sector']


# In[8]:


# Check for any null values present in dataset or not

FDI.isnull().sum()


# #### No null value present 

# #### Now we convert USD to INR which gives us better understanding of recieved amount and visualization of data.

# In[9]:


# Exchange rate. reference = https://en.wikipedia.org/wiki/Exchange_rate_history_of_the_Indian_rupee

rate = [45.68,47.69,48.39,45.95,44.93,44.27,45.24,40.26,45.99,47.44,45.56,47.92,54.40,60.50,61.14,65.46,67.07]


# In[10]:


# Create a function which is convert FDIs value from USD to INR  


def multiply_columns(df, col_list, num):
    for col in col_list:
        df[col] = df[col] * rate[col_list.index(col)]
    return df


# In[11]:


FDI_USD = FDI.copy() 
FDI_INR = multiply_columns(FDI, Year, rate)


# In[12]:


FDI_INR.style.set_caption('FDI (amount in crore INR)').format(precision=2)


# #### Unpivote DataFrame from wide to long 

# In[13]:


melt = pd.melt(FDI_USD, id_vars= Sectors, value_vars= Year, var_name= 'Year', value_name= 'FDI_amount in USD (million)',
              ignore_index=True)

melt


# In[14]:


melt1 = pd.melt(FDI_INR, id_vars= Sectors, value_vars= Year, var_name= 'Year', value_name= 'FDI_amount in INR (crore)',
              ignore_index=True)
melt1 = round(melt1,2)
melt1


# #### Merge FDI_amount in USD (million) column in melt1 DataFrame

# In[15]:


Merged = melt1.merge(melt, how='left')
Merged


# In[16]:


# Sorting the Sector and Year column

Sorted = Merged.sort_values(['Sector','Year'], ignore_index=True)
Sorted


# ### Statistics for each sector

# In[17]:


print('\n Statistics for each sector as follows \n','-'*60, sep=' ')
print(pd.DataFrame(Sorted.groupby('Sector').describe().loc[ : , : ]).transpose())


# In[18]:


Sorted = Sorted[['Sector','FDI_amount in INR (crore)', 'FDI_amount in USD (million)'
                 ,]].replace(["CONSTRUCTION DEVELOPMENT: Townships, housing, built-up infrastructure and construction-development projects"
                              ,"SERVICES SECTOR (Fin.,Banking,Insurance,Non Fin/Business,Outsourcing,R&D,Courier,Tech. Testing and Analysis, Other)"
                              ,'TEA AND COFFEE (PROCESSING & WAREHOUSING COFFEE & RUBBER)']
                             ,["CONSTRUCTION DEVELOPMENT","SERVICES SECTOR",'TEA AND COFFEE'])


# ### Sector by sector total FDI from 2000-01 to 2016-17

# In[19]:


Sectorwise_FDI = Sorted.groupby('Sector').sum()
Sectorwise_FDI.sort_values(by='FDI_amount in USD (million)',ascending=False)


# ##### From above, 
# Highest FDI comes in service sector and lowest in coir. Also computer, construction, telecommunications and automoblie sector 
# are in top 5.

# ### Data analysis by visuals

# In[20]:


Sectorwise_FDI.plot(kind='bar',y='FDI_amount in INR (crore)',figsize = (25,8), legend= True, title='Sector by Sector FDI',
                    ylabel='FDI_amount in INR (crore)')


# ### Top 15 sectors that got foreign direct investment (FDI)

# In[21]:


top15 = Sectorwise_FDI.nlargest(15,['FDI_amount in INR (crore)'])
top15


# In[22]:


# The total percentage of stakehold by sector

total_FDI = round(melt1['FDI_amount in INR (crore)'].sum(),2)
Sum = top15['FDI_amount in INR (crore)'].sum()
top15['% of total'] = round(top15['FDI_amount in INR (crore)']/Sum*100,2) 
top15['% to amount'] = round((top15['FDI_amount in INR (crore)']/total_FDI)*100,2)
top15


# ##### FDI in top 15 sector from 2000-01 to 2016-17

# In[23]:


# Represented with piechart

plt.figure(figsize=(20,8))
plt.pie(top15['FDI_amount in INR (crore)'], labels=top15.index, autopct='%1.1f%%', startangle=90)
plt.axis('equal')
plt.title('FDI in top 15 sectors', fontdict={ 'horizontalalignment': 'right'})
plt.show()


# ##### from the above, we have seen that the service sector has the highest FDI. followed by computers, telecommunication, construction, etc.

# ### Bottom 15 sectors that got foreign direct investment (FDI)

# In[24]:


bottom15 = Sectorwise_FDI.nsmallest(15,['FDI_amount in INR (crore)'])
Sum = bottom15['FDI_amount in INR (crore)'].sum()
bottom15['% of total'] = round(bottom15['FDI_amount in INR (crore)']/Sum*100,2) 
bottom15['% to amount'] = round((bottom15['FDI_amount in INR (crore)']/total_FDI)*100,2)
bottom15


# In[25]:


plt.figure(figsize=(15,7))
plt.barh(bottom15.index,bottom15['FDI_amount in INR (crore)'])
plt.title('FDI in bottom 15 sectors')
plt.xlabel('FDI_amount in INR (crore)')
plt.ylabel('Bottom 15 Sectors')
plt.show()


# #### Here COIR has the lowest FDI of 216.21 crore. followed by defence of 260.99 Cr, mathematical 416.15 Cr and coal production 1221.34 Cr etc.

# ### Year to Year FDI analysis

# #### We create new DataFrame based on previous and add new column of ' % of growth '

# In[26]:


DF2 = melt1[['Year','FDI_amount in INR (crore)']]
DF2 = round(DF2.groupby('Year').sum(),2)

DF2['% of growth in FDI'] = round(DF2.pct_change()*100,2)
DF2

DF2.fillna('-')


# ### Plotting visual for year to year growth

# In[27]:


DF2.plot.line(y='FDI_amount in INR (crore)',figsize=(10,10))
plt.ylabel('FDI_amount in INR (crore)')
plt.title('Year to Year Growth in FDI')
plt.show()


# ### Conclusion
# 
# The above graph shows the total amount of FDI in India during the period 2000 to 2017.
# 
# from period 2000-01 to 2001-2002, it shows good result in FDI. a little bit down and up between 2002-03 and 2004-05. from 2004-05 to 2008-09 bulls hold the ground. again ups and down between 2008-09 and 2012-2013, and after 2012-13 till 2017 FDI boom again.

# In[28]:


# save file 

Merged.to_csv('FDI_2000-2017.csv')


# In[ ]:




