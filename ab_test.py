import pandas as pd
from pandas.io.json import json_normalize
import random
import math
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import datetime
import json
import os
#import bigquery as bq
import time
from datetime import datetime, timedelta


file_dir = os.path.dirname(os.path.abspath(__file__))
project_id = 'crafty-campaign-106420'
#crafty_key = json.load(open(str(file_dir) + '/crafty_key.json'))
#client = bq.get_client(project_id,json_key=crafty_key,readonly=False)


#job_id, _results = client.query('select * from tqin.v_ABRetention')


#complete = False

#while True:
#    if complete == False:
#        complete, row_count = client.check_job(job_id)
#    else:
#        break

#results = client.get_query_rows(job_id)

#retention_data = json_normalize(results)

retention_data = pd.read_gbq('select * from tqin.v_ABRetention', project_id)

#retention_data = pd.read_csv('/Users/thomasqin/Documents/python/abretention.csv')
test_groups = ['control','v1','v2','v3']
#now = datetime.now()
#current_date = now.strftime("%m-%d-%y")


#date_converter = lambda x: datetime.fromtimestamp(x)

#retention_data['install_date'] = retention_data['install_date'].apply(date_converter)

#player_id_control = retention_data_control['player_id']
#player_id_test = retention_data_test['player_id']



d1_retention_test = []
d1_retention_control = []
d3_retention = []
d7_retention = []
d14_retention = []
      

def reject_rate(p_values):
    reject =len([p for p in p_values if p <= 0.05])    
    rejected = (reject/float(len(p_values))) * 100
    return rejected

def retention_simulation1(group1, group2, n, sample_size, d):

    p_values = []
    
    retention_data1 = retention_data[(retention_data['experiment_group'] == group1) & (retention_data['install_date'] <= (datetime.now() - timedelta(days = -d)))]
    retention_data2 = retention_data[(retention_data['experiment_group'] == group2) & (retention_data['install_date'] <= (datetime.now() - timedelta(days = -d)))]
    
    day = 'd'+str(d)
    retention_data1 = retention_data1[day].values #extract the Numpy array to speed up the calculation
    retention_data2 = retention_data2[day].values
    d1_retention_test = []
    d1_retention_control = []

    for i in range(n):
        if i % 100 == 0:        
            print 'Running test simulation %s...' % i

        samp1 = random.sample(retention_data1,sample_size) #need install and app_family
        samp2 = random.sample(retention_data2,sample_size) #need install and app_family

        p1 = sum(samp1)/float(sample_size)
        p2 = sum(samp2)/float(sample_size)
        #p1 = len(samp1[samp1['d1'] == 1])/float(len(samp1))
        #p2 = len(samp2[samp2['d1'] == 1])/float(len(samp2))
        #time2 = (time.time() - startTime) + time2
        #startTime = time.time()
        p_values.append(stats.binom_test(sum(samp2), sample_size, p1))
        #startTime = time.time()
        #time3 = (time.time() - startTime) + time3
        #startTime = time.time()
        d1_retention_control.append(p1)        
        d1_retention_test.append(p2)
        #time4 = (time.time() - startTime) + time3
        
    return p_values, d1_retention_control, d1_retention_test       
       

    #t,p = stats.ttest_ind(samp1['d1'],samp2['d1'],equal_var=False)
 

def retention_simulation(retention_data1, retention_data2, n, sample_size, d):

    p_values = []

    #install_dates = retention_data['install_date']

    retention_data1 = retention_data1[d].values #extract the Numpy array to speed up the calculation
    retention_data2 = retention_data2[d].values
    d1_retention_test = []
    d1_retention_control = []

    for i in range(n):
        if i % 100 == 0:        
            print 'Running test simulation %s...' % i

        samp1 = random.sample(retention_data1,sample_size) #need install and app_family
        samp2 = random.sample(retention_data2,sample_size) #need install and app_family

        p1 = sum(samp1)/float(sample_size)
        p2 = sum(samp2)/float(sample_size)
        #p1 = len(samp1[samp1['d1'] == 1])/float(len(samp1))
        #p2 = len(samp2[samp2['d1'] == 1])/float(len(samp2))
        #time2 = (time.time() - startTime) + time2
        #startTime = time.time()
        p_values.append(stats.binom_test(sum(samp2), sample_size, p1))
        #startTime = time.time()
        #time3 = (time.time() - startTime) + time3
        #startTime = time.time()
        d1_retention_control.append(p1)        
        d1_retention_test.append(p2)
        #time4 = (time.time() - startTime) + time3
        
    return p_values, d1_retention_control, d1_retention_test   




#retention_data_control = retention_data[(retention_data['experiment_group'] == 'control') & (retention_data['install_date'] <= (datetime.now() - timedelta(days = -7)))]
#retention_data_test = retention_data[(retention_data['experiment_group'] == 'v2') & (retention_data['install_date'] <= (datetime.now() - timedelta(days = -7)))]
startTime = time.time()
d1_retention_p, dX_retention, dX_retention2 = retention_simulation1('control', 'v2',20000,3000, 7) #75.2 #161.396529913 #321.671721935
print time.time() - startTime

#startTime = time.time()
#d1_retention_p, dX_retention, dX_retention2 = retention_simulation(retention_data_control, retention_data_test,20000,3000, 'd7') #75.2 #143.341856003 #312.343669891
#print time.time() - startTime

rejected_perc = reject_rate(d1_retention_p)


print '--------------------------------------------------------------' 
print 'Summary' 
print 'Out of 1000 simulated tests, reject null hypothesis of equal means %d%% of the time' %rejected_perc  
    
    
#d1_retention = sorted(d1_retention)
#d3_retention = sorted(d3_retention)
#d7_retention = sorted(d7_retention)
#d14_retention = sorted(d14_retention)
plt.clf()
fit = stats.norm.pdf(dX_retention, np.mean(dX_retention), np.std(dX_retention))
fit2 = stats.norm.pdf(dX_retention2, np.mean(dX_retention2), np.std(dX_retention2))

common_params = dict(bins=20,range=[0.07,0.15],normed=True)

plt.subplot(211)
plt.plot(dX_retention,fit,'o')
plt.hist(dX_retention,**common_params)

plt.subplot(212)
plt.plot(dX_retention2,fit2,'o')
plt.hist(dX_retention2,**common_params)

plt.savefig(str(file_dir) + '/try.png')
