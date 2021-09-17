from database.raw_wifi import SummariesTable
from lib import dateutil
from datetime import datetime, timedelta
import pandas as pd
from numpy import diff
from dynamo_objects import database

class CustSegException(Exception):
    def __init__(self, message, status='error', info=None):
        Exception.__init__(self)
        self.message = message
        self.status = status
        self.info = info if info else ''
    def __str__(self):
        return repr(self.value)

def grouper(df):
    lower_limits = []
    upper_limits = []
    limits_categories = []
    diff = []
    
    group_sum = df.groupby('category').shoppers.sum().values
    lower_limits = df.groupby('category').days.min().values
    upper_limits = df.groupby('category').days.max().values
    
    try:
        cnt = 0
        for _ in range(len(lower_limits)):
            limits_categories.append("%d-%d" %(lower_limits[cnt],upper_limits[cnt]))
            diff.append(upper_limits[cnt]-lower_limits[cnt]+1)
            cnt += 1
    except:
        raise CustSegException("Category ")
    
    limits_categories_df = pd.DataFrame(limits_categories)
    diff_df = pd.DataFrame(diff)
    group_sum_df = pd.DataFrame(group_sum)
    
    sum_by_category_df = pd.concat([limits_categories_df,diff_df,group_sum_df],axis=1)
    sum_by_category_df.columns = ['category','span','shopper']
    
    sum_by_category_new_df = sum_by_category_df[sum_by_category_df['span']>1]
    return sum_by_category_new_df
    
def dbv_count(df):
    days = []
    shoppers = []
    day_category = []
    group_size = 5
    
    days = df.groupby('time').cmac.count().keys()
    days_int = [int(float(x/timedelta(1))) for x in days]
    shoppers = df.groupby('time').cmac.count().values
    
    for day in days_int:
        day_category.append(int(float((day-1)/group_size))+1)
        
    
    days_df = pd.DataFrame(days_int)
    shoppers_df = pd.DataFrame(shoppers)
    category_df = pd.DataFrame(day_category)
    
    days_shoppers_df = pd.concat([days_df,category_df,shoppers_df],axis=1)
    days_shoppers_df.columns = ['days','category','shoppers']
    
    return days_shoppers_df
    
def duration_between_visits(comb_df, lvpc_no_employee_df):
    lvpc_no_employee_sorted_df = lvpc_no_employee_df.sort('cmac', ascending=True)
    comb_sorted_df = comb_df.sort('cmac', ascending=True)
        
    cmac_list = lvpc_no_employee_df[lvpc_no_employee_df['visits']>1]['cmac'].value_counts().index
    comb_gb = comb_df.groupby(['cmac'])
    duration_between_visits_list = []
    
    for item in cmac_list:
        date_list = []
        timedelta_list = []
        date_list = comb_gb.get_group(item).date.values
        date_list = list(set(date_list))
        date_list.sort()
        
        timedelta_list = diff(date_list).tolist()
        timedelta_len = len(timedelta_list)
        if timedelta_len==0:
            timedelta_len=1
        avg_timedelta = sum(timedelta_list, timedelta(0)) / timedelta_len
        
        if avg_timedelta.seconds >= 43200:
            avg_timedelta = avg_timedelta - timedelta(seconds=avg_timedelta.seconds) + timedelta(1)
        else:
            avg_timedelta = avg_timedelta - timedelta(seconds=avg_timedelta.seconds)
            
        duration_between_visits_list.append(avg_timedelta)
    
    cmac_df = pd.DataFrame(cmac_list)
    dbv_df = pd.DataFrame(duration_between_visits_list)
    cdbv_df = pd.concat([cmac_df, dbv_df],axis=1)
    cdbv_df.columns = ['cmac','time']
    
    dbv_sorted_df = cdbv_df.sort('time',ascending=False)
    
    return dbv_sorted_df
    
def cmac_count(df):
    cmac_count_df = df.groupby('cmac')['visits'].sum()
    cmac_lastvisit_df = df.groupby('cmac')['date'].max()
    
    cmac_count_list = cmac_count_df.index
    visit_count_list = cmac_count_df.values
    cmac_count_df = pd.DataFrame(cmac_count_list)
    visit_count_df = pd.DataFrame(visit_count_list)
    cmac_visit_count_df = pd.concat([cmac_count_df,visit_count_df],axis=1)
    cmac_visit_count_df.columns = ['cmac','visits']
    
    cmac_lastvisit_list = cmac_lastvisit_df.index
    lastvisit_list = cmac_lastvisit_df.values
    cmac_lastvisit_df = pd.DataFrame(cmac_lastvisit_list)
    lastvisit_df = pd.DataFrame(lastvisit_list)
    cmac_lastvisit_new_df = pd.concat([cmac_lastvisit_df, lastvisit_df],axis=1)
    cmac_lastvisit_new_df.columns = ['cmac','last_visit']
    
    last_visit_plus_count_df = pd.merge(cmac_visit_count_df,cmac_lastvisit_new_df, on='cmac')
    return last_visit_plus_count_df
    
def summary_to_dataframe(summaries):
    temp_new_list = []
    temp_repeat_list = []
    temp_repeat_freq_list = []
    
    cmac_new_list = []
    cmac_repeat_list = []
    cmac_repeat_freq_list = []
    
    date_new_list = []
    date_repeat_list = []
    
    for summary in summaries:
        temp_new_list = list(summary.cmac_new)
        temp_repeat_list = list(summary.cmac_repeat.keys())
        temp_repeat_freq_list = list(summary.cmac_repeat.values())
        
        dt = datetime.strptime(summary.date, "%Y-%m-%d").date()
        
        cnt = 0
        for _ in range(len(temp_new_list)):
            cmac_new_list.append(temp_new_list[cnt])
            date_new_list.append(dt)
            cnt += 1
            
        cnt = 0
        for _ in range(len(temp_repeat_list)):
            cmac_repeat_list.append(temp_repeat_list[cnt])
            cmac_repeat_freq_list.append(temp_repeat_freq_list[cnt])
            date_repeat_list.append(dt)
            cnt += 1
    
    date_new_df = pd.DataFrame(date_new_list)
    cmac_new_df = pd.DataFrame(cmac_new_list)
    ones_df = pd.DataFrame([1]*len(cmac_new_list))
    new_df = pd.concat([cmac_new_df,ones_df,date_new_df],axis=1)
    try:
        new_df.columns = ['cmac','visits','date']
    except:
        raise CustSegException('Insufficient data. Try adjusting the start and end parameters.')
    
    date_repeat_df = pd.DataFrame(date_repeat_list)
    cmac_repeat_df = pd.DataFrame(cmac_repeat_list)
    cmac_freq_repeat_df = pd.DataFrame(cmac_repeat_freq_list)
    repeat_df = pd.concat([cmac_repeat_df,cmac_freq_repeat_df,date_repeat_df],axis=1)
    try:
        repeat_df.columns = ['cmac','visits','date']
    except:
        raise CustSegException('Insufficient data. Try adjusting the start and end parameters.')
    
    new_repeat_df = pd.concat([new_df,repeat_df],axis=0)
    return new_repeat_df
    
def get_summary(amac, start, end):
    summ_tab = SummariesTable()
    summaries = summ_tab.query_summaries(amac, start, end)
    return summaries

def time_range_rules(start, end):
    now = datetime.now().date()
    diff = end - start
    
    if(start>now or end>now):
        raise CustSegException("Future time selected.")
    if(diff<timedelta(0)):
        raise CustSegException("Start is greater than end.")
    elif(diff<timedelta(1)):
        raise CustSegException("Start and end must be at least 1 day apart.")
    
def main(amac_list, start, end):
    
    time_range_rules(start, end)
    summaries = []
    new_repeat_df_list = []
    
    for amac in amac_list:
        summaries.append(get_summary(amac,start,end))
    
    for summary in summaries:
        new_repeat_df_list.append(summary_to_dataframe(summary))
    
    comb_df = pd.concat(new_repeat_df_list, axis=0)
    comb_nodup_df = comb_df.drop_duplicates()
    last_visit_plus_count_df = cmac_count(comb_nodup_df)
    
    dbv_sorted_df = duration_between_visits(comb_df, last_visit_plus_count_df)
    days_shoppers_df = dbv_count(dbv_sorted_df)
    sum_by_category_new_df = grouper(days_shoppers_df)
    
    category = []
    shopper = []
    data = {}
    category = list(sum_by_category_new_df["category"])
    shopper = list(sum_by_category_new_df["shopper"])
    shopper = map(str,shopper)
    
    data = {'category':category, 'shopper':shopper}
    return data
