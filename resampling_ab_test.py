

import pandas as pd
import random
import numpy as np
import scipy.stats as stats
import matplotlib.pyplot as plt
import datetime
import os
import argparse
import time
import string
from datetime import timedelta,datetime


file_dir = os.path.dirname(os.path.abspath(__file__)) #path in which the jpeg is saved


def reject_rate(p_values):
    reject =len([p for p in p_values if p <= 0.20])    
    rejected = (reject/float(len(p_values))) * 100
    return rejected

def resampling(test_data, group1, group2, n, sample_size, d, test_type):

    p_values = []
    
    test_data1 = test_data[(test_data['experiment_group'] == group1) & (test_data['install_date'] <= (datetime.now() - timedelta(days = -d)))]
    test_data2 = test_data[(test_data['experiment_group'] == group2) & (test_data['install_date'] <= (datetime.now() - timedelta(days = -d)))]
    
    day = 'd'+str(d)
    test_data1 = test_data1[day].values #extract the Numpy array to speed up the calculation
    test_data2 = test_data2[day].values
    day_d_test = []
    day_d_control = []


    for i in range(n):
        if i % 100 == 0:        
            print 'Running test simulation %s...' % i
    
        samp1 = random.sample(test_data1,sample_size) #need install and app_family
        samp2 = random.sample(test_data2,sample_size) #need install and app_family
    
        p1 = sum(samp1)/float(sample_size)
        p2 = sum(samp2)/float(sample_size)
    
        if test_type == 'retention' or test_type == 'conversion':        
            p_values.append(stats.binom_test(sum(samp2), sample_size, p1))
        else:
            t,p = stats.ttest_ind(samp1,samp2)
            p_values.append(p)
    
        day_d_control.append(p1)        
        day_d_test.append(p2)

        #time4 = (time.time() - startTime) + time3
        
    return p_values, day_d_control, day_d_test       
 
       
#test_data_control = test_data[(test_data['experiment_group'] == 'control') & (test_data['install_date'] <= (datetime.now() - timedelta(days = -7)))]
#test_data_test = test_data[(test_data['experiment_group'] == 'v2') & (test_data['install_date'] <= (datetime.now() - timedelta(days = -7)))]

    
def plot_dist(dX, dX2, group1, group2, bin_size, test_type):
    
    a_mean = np.mean(dX)
    a_std = np.std(dX)

    b_mean = np.mean(dX2)
    b_std = np.std(dX2)    
    
    plt.clf()
    fit = stats.norm.pdf(dX, a_mean, a_std)
    fit2 = stats.norm.pdf(dX2, b_mean, b_std)
    
    min_range = min(min(dX),min(dX2))
    max_range = max(max(dX),max(dX2))    
    common_params = dict(bins=bin_size,range=[min_range,max_range],normed=False)
    
    a=plt.subplot(211)
    #a.plot(dX,fit,'o')
    a.hist(dX,**common_params)
    a.set_title('%s distribution for group: %s'%(test_type,group1))
    #a.text(a_mean,-.2,'Mean: %f' %a_mean)
    a.text(0.95,0.95,'Mean: %f\nStandard Dev: %f' %(a_mean,a_std),horizontalalignment='right',verticalalignment='top',transform=a.transAxes)
    a.axvline(a_mean,color='r',linestyle='dashed',linewidth=2)

    b=plt.subplot(212)
    #b.plot(dX2,fit2,'o')
    b.hist(dX2,**common_params)
    b.set_title('%s distribution for group: %s'%(test_type,group2))
    #b.text(b_mean,-.2,'Mean: %f' %b_mean)
    b.text(0.95,0.95,'Mean: %f\nStandard Dev: %f' %(b_mean,b_std),horizontalalignment='right',verticalalignment='top',transform=b.transAxes)
    b.axvline(b_mean,color='r',linestyle='dashed',linewidth=2)

    plt.savefig(str(file_dir) + '/%sScreen%f.png' %(test_type,time.time()))



def main(group1, group2, d, sample_size, iterations, bin_size, test_type, experiment_id):
    project_id='crafty-campaign-106420'
    
    test_data = pd.read_gbq('select * from AvengersCrossEvent.v_ABTest_%s where experiment_id = %s' %(string.upper(test_type),experiment_id), project_id)
   
    p_values, day_d, day_d2 = resampling(test_data,group1,group2,iterations,sample_size, d, test_type) #75.2 #161.396529913 #321.671721935
    rejected_perc = reject_rate(p_values)
    print '--------------------------------------------------------------' 
    print 'Summary' 
    print 'Out of %i simulated tests, reject null hypothesis of equal means %d%% of the time' %(iterations,rejected_perc  )
    
    plot_dist(day_d,day_d2,group1,group2, bin_size,test_type)
    print np.mean(day_d), np.mean(day_d2)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    #parser.add_argument('project_id', default='crafty-campaign-106420')
    parser.add_argument(
        'group1', 
        help='test group ID',
        type=str,
        default='control')
    parser.add_argument(
        'group2', 
        help='test group ID',
        type=str)
    parser.add_argument(
        'd', 
        help='nDay',
        type=int)
    parser.add_argument(
        'sample_size', 
        help='Resampling size',
        type=int)
    parser.add_argument(
        'iterations', 
        help='Number of iterations',
        type=int)
    parser.add_argument(
        'bin_size', 
        help='Number of bins',
        type=int)
    parser.add_argument(
        'test_type', 
        help='Type of test: retention, arpu, arppu, conversion',
        type=str)
    parser.add_argument(
        'experiment_id', 
        help='experiment ID',
        type=str,
        default='115')
    args = parser.parse_args()

    main(
        args.group1,
        args.group2,
        args.d,
        args.sample_size,
        args.iterations,
        args.bin_size,
        args.test_type,
        args.experiment_id)
    

#plt.clf()
#fit = stats.norm.pdf(d_retention, np.mean(d_retention), np.std(d_retention))
#fit2 = stats.norm.pdf(d_retention2, np.mean(d_retention2), np.std(d_retention2))
#a=plt.subplot(211)
#a.plot(d_retention,fit,'o')
#a.hist(d_retention,**common_params)
#a.set_title('Retention Distributionfor Control')

#b=plt.subplot(212)
#b.plot(d_retention2,fit2,'o')
#b.hist(d_retention2,**common_params)
