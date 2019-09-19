
# coding: utf-8

# In[25]:


import re
import pandas as pd


# In[26]:


df=pd.read_csv('data/pbp-2019.csv')


# In[27]:


df=df[df['IsNoPlay']==0]


# In[28]:


def extract_passer(x):
    return x.split('-')[1].split(' ')[0]


# In[29]:


def extract_receiver(x):
    if len(x.split('-'))>2:
        return x.split('-')[2].split(' ')[0]
    else:
        'None'


# In[30]:


def extract_running_back(x):
    if len(x.split('-'))>2:
        return x.split('-')[1].split(' ')[0]
    else:
        'None'


# In[31]:


df['Target']=df[df['IsPass']==1]['Description'].apply(lambda x:extract_receiver(x))
df['QB']=df[df['IsPass']==1]['Description'].apply(lambda x:extract_passer(x))
df['RB']=df[df['IsRush']==1]['Description'].apply(lambda x:extract_running_back(x))


# In[32]:


df.head()


# In[33]:


df.to_csv('data/2019_clean_data.csv')


# ## Example Use Case: See % of all Targets by WR

# In[44]:


df[df['IsNoPlay']==0].groupby(['Target','OffenseTeam']).sum()[['IsPass','Yards']].div(df[df['IsNoPlay']==0].groupby(['OffenseTeam']).sum()[['IsPass','Yards']]).sort_values(by='IsPass',ascending=False)

