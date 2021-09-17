import pytz
import datetime
import pandas as pd
from time import time
from math import floor,log
from numpy import hstack,mean
from sklearn.cluster import KMeans
from database.raw_wifi import SessionsTable
from database.system import VenuesTable, NodesTable
from database import get_venue_timezone, get_local_venue_datetime

class RSSIException(Exception):
    def __init__(self, message, status='error', info=None):
        Exception.__init__(self)
        self.message = message
        self.status = status
        self.info = info if info else ''
    def __str__(self):
        return self.message

def get_threshold(closed_value):

    k = int(floor(2*log(len(closed_value),5)))
    
    if(k<=3):
        k = k+1
    elif(k>=4 and k<=10):
        k = k-1
    elif(k>10):
        k = k+1
    
    lines = map(int,closed_value)
    try:
        lines_df = pd.DataFrame(lines)
        ones_df = pd.DataFrame([1]*len(lines))
        comb_df = hstack((ones_df,lines_df))   
        km = KMeans(k,random_state=0)
        km.fit(comb_df)
        k_centers = pd.DataFrame(km.cluster_centers_)
        k_centers_list = k_centers[1].tolist()
        k_centers_list.sort()
        threshold = mean(k_centers_list[-3:])

    except:    
        raise RSSIException('Error occured while searching for clusters')
    
    return ("%.1f" % threshold)

def amac_to_tz(amac):
    node = NodesTable().get(amac)
    venue = VenuesTable().get(node.venue)
    tz = get_venue_timezone(venue)
    return tz
    
def validate_time(human_time, opened_wd_dt, closed_wd_dt, opened_we_dt, closed_we_dt):
    flag = 0
    
    start_of_weekends = 4
    end_of_weekends = 5
    start_of_weekdays = 6
    end_of_weekdays = 3
    
    try:
        if((human_time.weekday()>=0) and (human_time.weekday()<=end_of_weekdays or human_time.weekday()==start_of_weekdays)): #Weekdays            
            try:
                if(human_time.time()>opened_wd_dt and human_time.time()<closed_wd_dt):
                    flag = 1
                elif(human_time.time()<opened_wd_dt or human_time.time()>closed_wd_dt):
                    flag = 2
            except:
                raise RSSIException('Timing is out of range')
        elif(human_time.weekday()==start_of_weekends or human_time.weekday()==end_of_weekends): #Weekends
            try:
                if(human_time.time()>opened_we_dt and human_time.time()<closed_we_dt):
                    flag = 1
                elif(human_time.time()<opened_we_dt or human_time.time()>closed_we_dt):
                    flag = 2
            except:
                raise RSSIException('Timing is out of range')
    except:
        raise RSSIException('Day-of-week is out of range')
    return flag
        
def calc_shop_opening_hours(opened_wd, closed_wd, opened_we, closed_we):
    if opened_wd is None:
        opened_wd = "10:00"
    if closed_wd is None:
        closed_wd = "22:00"
    if opened_we is None:
        opened_we = "10:00"
    if closed_we is None:
        closed_we = "22:00"
    
    try:
        opened_wd_hr = int(opened_wd.split(':')[0])
        opened_wd_min = int(opened_wd.split(':')[1])    
        closed_wd_hr = int(closed_wd.split(':')[0])
        closed_wd_min = int(closed_wd.split(':')[1])    
        opened_we_hr = int(opened_we.split(':')[0])
        opened_we_min = int(opened_we.split(':')[1])    
        closed_we_hr = int(closed_we.split(':')[0])
        closed_we_min = int(closed_we.split(':')[1])
    except:       
        raise RSSIException('The input format is incorrect')
    
    opened_wd = datetime.time(opened_wd_hr,opened_wd_min,0)
    closed_wd = datetime.time(closed_wd_hr,closed_wd_min,0)
    opened_we = datetime.time(opened_we_hr,opened_we_min,0)
    closed_we = datetime.time(closed_we_hr,closed_we_min,0)
    
    return opened_wd,closed_wd,opened_we,closed_we

def log_processor(lines, tz, opened_wd, closed_wd, opened_we, closed_we):
    
    #print 'Calculating RSSI threshold is in progress...'
    cut_line = []
    opened_value = []
    closed_value = []
    time_list = []
    cmac_list = []
    rssi_list = []
    
    line_cnt = 0
    
    opened_wd_dt,closed_wd_dt,opened_we_dt,closed_we_dt = calc_shop_opening_hours(opened_wd,closed_wd,opened_we,closed_we)
    
    for item in lines:  
        line_cnt = line_cnt + 1
        human_time = datetime.datetime.fromtimestamp(item['fseen'],pytz.timezone(tz))
        is_open_hours = validate_time(human_time,opened_wd_dt,closed_wd_dt,opened_we_dt,closed_we_dt)
        
        if(item['fseen'] and item['cmac'] and item['max_rssi']): #Ensure consistent records in the lists
            time_list.append(human_time)
            cmac_list.append(item['cmac'])
            rssi_list.append(item['max_rssi'])
        
        if(is_open_hours==1):
            opened_value.append(item['max_rssi'])
        elif(is_open_hours==2):
            closed_value.append(item['max_rssi'])
    
    if(len(closed_value)==0 or len(opened_value)==0):
        raise RSSIException('Insufficient data for RSSI threshold calculation. Try changing your search time interval by adjusting start and end.')
   
    time_df = pd.DataFrame(time_list)
    cmac_df = pd.DataFrame(cmac_list)
    rssi_df = pd.DataFrame(rssi_list)
    tcr_df = pd.concat([time_df,cmac_df,rssi_df],axis=1)
    tcr_df.columns = ['time','cmac','rssi']
    
    return opened_value,closed_value,tcr_df

def log_get(amac, start, end):
    records = []
    sess = SessionsTable()
    #print 'Gathering logs for RSSI threshold calculation is in progress...'
    records = sess.query_by_amac(amac, start, end)
    #print 'Gathering logs completed.'
    return records

def time_range_rules(start, end):
    now = int(time())
    
    if end is None:
        end = now
    if start is None:
        start = end - 604800
    
    if(len(str(start))!=10 or len(str(end))!=10):
        raise RSSIException('Time must be specified in unix timestamp format')
    if(end>now or start>now):
        raise RSSIException('Future time selected')
    if(start>end):
        raise RSSIException('Start time is greater than end')
    if(end-start<86400):
        raise RSSIException('Start and end must be at least 24 hours apart. It is recommended that you set the time interval to be 7 days.')
    if(end-start>2678400): #One month difference between start and end is set as the maximum to reduce computational strain and DynamoDB throughput
        start = end - 2678400
    
    return start,end
    
def main(amac, start, end, ot_list_delim):
    start,end = time_range_rules(start,end)
    log = log_get(amac,start,end)
    opened_wd=ot_list_delim[0]
    closed_wd=ot_list_delim[1]
    opened_we=ot_list_delim[2]
    closed_we=ot_list_delim[3]
    tz = amac_to_tz(amac)
    opened_value,closed_value,tcr_df = log_processor(log,tz,opened_wd,closed_wd,opened_we,closed_we)
    threshold = int(float(get_threshold(closed_value)))
    
    return threshold