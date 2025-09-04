import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option('display.max_columns', None) #  Show all columns
# # pd.set_option('display.width', 2000)        # Increase display width
# pd.set_option('display.max_colwidth', None) # Full content of each cell


df_cs=pd.read_csv(r"C:\Users\skd53\Downloads\maths and stats for DS\AtliQo bank project phase 1\datasets\credit_profiles.csv")
print(df_cs.head())
print(df_cs.shape)#here we are getting 1004 coloumns but it should be 1000 as in customers tables thir is 1000
# their is duplicates, we need to handle duplicates
print(df_cs[df_cs["cust_id"].duplicated(keep=False)])
# keep function is to find the duplicated values,to remove duplicates
df_cs_new=df_cs.drop_duplicates(subset="cust_id",keep="last")
print(df_cs_new)#now we have 1000 rows

# now checking null values
print(df_cs_new.isnull().sum())#we null values in credit limit
print(df_cs_new[df_cs_new["credit_limit"].isnull()])
# credit limit is depend on the credit score to visualize that we will use scatterplot
plt.scatter(df_cs_new.credit_limit,df_cs_new.credit_score)
plt.xlabel("credit limit")
plt.ylabel("credit score")
plt.grid(axis="y")
# plt.show()#here we can see higher the credit score is higher the credit limit

# now we are going to add new coloumn called credit score range
bin_range=[300,450,500,550,600,650,700,750,800]
label_range=['300–450', '451–500', '501–550', '551–600', '601–650', '651–700', '701–750', '751–800']
df_cs_new['credit_score_range'] = pd.cut(df_cs['credit_score'], bins=bin_range, labels=label_range, right=True)
print(df_cs_new.head(10))

# lets see what is the credit limit of the range 700-749
print(df_cs_new[df_cs_new.credit_score_range=="701–750"])#mostly it is 40000
# lets see what is the credit limit of the range 501–550
print(df_cs_new[df_cs_new.credit_score_range=="501–550"])#mostly it is 1000

# now for given credit score range(eg:701-749) we will find the median of that range
# firstly you should check credit limit it is similar to the mode means the most reoccuring value is same as median
# if it is not same go for mode
median_df=df_cs_new.groupby("credit_score_range")["credit_limit"].median()
print(median_df)
print(df_cs_new[df_cs_new["credit_limit"].isnull()].sample(3))
# merging data frames df_mode,df_cs_new
df_cs_new_2=pd.merge(df_cs_new,median_df,on="credit_score_range",suffixes=("","_median"))
print(df_cs_new_2)

# now lets print the sample rows for new 2 df and null value of new 2 df
print(df_cs_new_2.sample(3))
print(df_cs_new_2[df_cs_new_2["credit_limit"].isnull()].sample(3))
# now usinf fillna method
df_cs_new_3=df_cs_new_2.copy()#making new fresh data frame by copying the material of df 2
df_cs_new_3["credit_limit"].fillna(df_cs_new_3["credit_limit_median"],inplace=True)#the null value has been removed
print(df_cs_new_3.isnull().sum())
print(df_cs_new_3.loc[[690,431]])

# now lets see their is any outlier 
print(df_cs_new_3.describe())
# here we can see that oustanding debt has min 33 and max is 209901
# since the credit limit min is 500 and max is 60000 so how the debt is greater than the limit
# we will use boxplot method to see outlier
sns.boxplot(df_cs_new_3.outstanding_debt)
plt.show()
# now we will how many debt is greater than limit
print(df_cs_new_3[df_cs_new_3.outstanding_debt>df_cs_new_3.credit_limit])
# by busines understanding i  had replaced the outlier value by the credit limit value 
df_cs_new_3.loc[df_cs_new_3.outstanding_debt>df_cs_new_3.credit_limit,"outstanding_debt"]=df_cs_new_3["credit_limit"]
print(df_cs_new_3[df_cs_new_3.outstanding_debt>df_cs_new_3.credit_limit])
print(df_cs_new_3.describe())
print(df_cs_new_3.iloc[[1,19]])

