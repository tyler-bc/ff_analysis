# To add a new cell, type '#%%'
# To add a new markdown cell, type '#%% [markdown]'

#%%
import re
import pandas as pd


#%%
df=pd.read_csv('pbp-2019.csv')
#%% 
r_pass = re.compile(r"\((?:[0-9]*:[0-9][0-9])\)(?: \(.*\)| NEW QB.*)? ([0-9]+-[A-Z\.]+) (?:(PASS INCOMPLETE)|.*([0-9]+-[A-Z\.]*)).*")

def parse_pass(description):
    if description[:8] == "END GAME":
        return None,None
    else:
        m = r_pass.match(description)
        if m:
            return m.group(1),m.group(2) or m.group(3)
        else:
            raise Exception("Couldn't parse \n" + description)
df[df.IsPass == 1].Description.apply(parse_pass)

#%%
df=df[df['IsNoPlay']==0]
#%%
def extract_passer(x):
    return x.split('-')[1].split(' ')[0]

def extract_receiver(x):
    if len(x.split('-'))>2:
        return x.split('-')[2].split(' ')[0]
    else:
        'None'

def extract_running_back(x):
    if len(x.split('-'))>2:
        return x.split('-')[1].split(' ')[0]
    else:
        'None'


#%%
df['Target']=df[df['IsPass']==1]['Description'].apply(lambda x:extract_receiver(x))
df['QB']=df[df['IsPass']==1]['Description'].apply(lambda x:extract_passer(x))
df['RB']=df[df['IsRush']==1]['Description'].apply(lambda x:extract_running_back(x))


#%%
df[df['Target']=='G.BERNARD.']['Description']


#%%
df.head()


#%%
df.to_csv('2019_clean_data.csv')

#%% [markdown]
# ## Example Use Case: See % of all Targets by WR

#%%
df[df['IsNoPlay']==0].groupby(['Target','OffenseTeam']).sum()[['IsPass','Yards']].div(df[df['IsNoPlay']==0].groupby(['OffenseTeam']).sum()[['IsPass','Yards']]).sort_values(by='IsPass',ascending=False)


#%%
targets=df[df['IsNoPlay']==0].groupby(['Target','OffenseTeam']).sum()[['IsPass','Yards']].div(df[df['IsNoPlay']==0].groupby(['OffenseTeam']).sum()[['IsPass','Yards']]).sort_values(by='IsPass',ascending=False).reset_index()


#%%
targets[targets['OffenseTeam']=='KC']


#%%



