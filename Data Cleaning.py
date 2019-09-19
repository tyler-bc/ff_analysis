
# coding: utf-8

# In[1]:


import re
import pandas as pd


# In[3]:


df=pd.read_csv('pbp-2019.csv')


# In[4]:


df=df[df['IsNoPlay']==0]


# In[5]:


def extract_passer(x):
    return x.split('-')[1].split(' ')[0]


# In[6]:


def extract_receiver(x):
    if len(x.split('-'))>2:
        return x.split('-')[2].split(' ')[0]
    else:
        'None'


# In[7]:


def extract_running_back(x):
    if len(x.split('-'))>2:
        return x.split('-')[1].split(' ')[0]
    else:
        'None'


# In[8]:


df['Target']=df[df['IsPass']==1]['Description'].apply(lambda x:extract_receiver(x))
df['QB']=df[df['IsPass']==1]['Description'].apply(lambda x:extract_passer(x))
df['RB']=df[df['IsRush']==1]['Description'].apply(lambda x:extract_running_back(x))


# In[29]:


df[df['Target']=='G.BERNARD.']['Description']


# In[9]:


df.head()


# In[10]:


df.to_csv('2019_clean_data.csv')


# ## Example Use Case: See % of all Targets by WR

# In[11]:


df[df['IsNoPlay']==0].groupby(['Target','OffenseTeam']).sum()[['IsPass','Yards']].div(df[df['IsNoPlay']==0].groupby(['OffenseTeam']).sum()[['IsPass','Yards']]).sort_values(by='IsPass',ascending=False)


# In[22]:


targets=df[df['IsNoPlay']==0].groupby(['Target','OffenseTeam']).sum()[['IsPass','Yards']].div(df[df['IsNoPlay']==0].groupby(['OffenseTeam']).sum()[['IsPass','Yards']]).sort_values(by='IsPass',ascending=False).reset_index()


# In[27]:


targets[targets['OffenseTeam']=='KC']

