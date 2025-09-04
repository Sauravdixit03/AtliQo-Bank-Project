
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import statsmodels.stats.api as sms
import statsmodels.api as sm

# Loading campaign result data
df=pd.read_excel(r"C:\Users\skd53\OneDrive\Documents\avg_transactions_after_campaign.xlsx")
print(df.head())
print(df.shape)
# lets see how many times the average control transcation is greater than average test transaction
# out of 62 the 18 people has more transacction in control group
# we can say that test group average transaction is more than control group
print(df[df["control_group_avg_tran"]>df["test_group_avg_tran"]].shape)
# we need to do hypothesis testing , we are going to perform two sample z test
mean_control=df.control_group_avg_tran.mean()
std_control=df.control_group_avg_tran.std()
print(mean_control,std_control)
mean_test=df.test_group_avg_tran.mean()
std_test=df.test_group_avg_tran.std()
print(mean_test,std_test)

sample_size=62
# lets calculate z score of  two sample
a=std_test**2/sample_size
b=std_control**2/sample_size
z_score=(mean_test-mean_control)/np.sqrt(a+b)
print(z_score)

null_hypo="test group avg transaction is lower or equal to the control group"
alternate_hypo="test group avg transaction is higher than control group"

# significance level
alpha=0.05#(5%)
z_critical=1.64

# since my z-score > z-critical we can reject our null hypothesis and go with alternate hypothesis
'''
we can say that people are using more new credit card and the product will give positive results when it 
is launched
'''
