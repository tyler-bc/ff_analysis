
import re
import pandas as pd
import numpy as np

time_1 = r"(?:\(([0-9]{,2}:[0-9][0-9])\))"
team_0 = r"(?:[A-Z]{2,3})"
number_0 = r"(?:[0-9][0-9]?)"
number_1 = rf"({number_0})"
lastname_0 = r"(?:[A-Z]+)"
name_0 = r"(?:[A-Z]+\.[A-Z]+)"
name_1 = rf"({name_0})"
number_name_0 = rf"{number_0}-{name_0}"
number_name_2 = rf"{number_1}-{name_1}"
new_qb_0 = fr"(?: NEW QB. NO #{number_0} {name_0}\.)"
alt_qb_0 = fr"(?: #{number_0} {name_0} AT QUARTERBACK\.)"
alt_qb2_0 = fr"(?: {team_0} {number_0} -- {lastname_0} IN AT QB\.)"
direct_snap_0 = fr"(?: DIRECT SNAP TO {number_name_0}.)"
qb_comment_0 = fr"(?:{new_qb_0}|{alt_qb_0}|{alt_qb2_0})"
formation_comment_type_0 = rf"(?:NO HUDDLE|SHOTGUN|PUNT FORMATION)"
formation_comment_0 = rf"(?: \({formation_comment_type_0}(?:, {formation_comment_type_0})*\))"
incomplete_0 = "(?:INCOMPLETE)"
completion_0 = "(?:(?:(?:SHORT|DEEP) )?(?:RIGHT|LEFT|MIDDLE))"
pass_1 = rf"((?:{incomplete_0} )?{completion_0})"
eligible_0 = rf"(?: {number_name_0} REPORTED IN AS ELIGIBLE\.)"

r_pass = re.compile(rf"{time_1}{formation_comment_0}?{eligible_0}?.*{number_name_2} PASS {pass_1}(?: TO {number_name_2})?")
#%% 
def parse_pass(description):
    if description[:8] == "END GAME":
        return None,None
    else:
        m = r_pass.match(description)
        time = m.group(1)
        passer_number = m.group(2)
        passer_name = m.group(3)
        pass_state = m.group(4)
        receiver_number = m.group(5)
        receiver_name = m.group(6)
        return passer_name, receiver_name

r_rush = re.compile(rf"{time_1}{qb_comment_0}?{formation_comment_0}?{direct_snap_0}? *{number_name_2}")
def parse_rush(description):
    m = r_rush.match(description)
    time = m.group(1)
    number = m.group(2)
    name = m.group(3)
    return name

def fetch_data(filename):
    df=pd.read_csv(filename)
    df['Passer'] = ''
    df['Receiver'] = ''
    df['Runner'] = ''
    m_pass = df.IsPass == 1
    m_rush = df.IsRush == 1
    if np.any(m_rush & m_pass):
        raise Exception()
    temp = df[m_pass].Description.apply(parse_pass)
    df.loc[m_pass,['Passer','Receiver']] = pd.DataFrame(temp.values.tolist(),index=temp.index).values
    df.loc[m_rush,'Rusher'] = df[m_rush].Description.apply(parse_rush)
    return df