import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
df_cust=pd.read_csv(r"C:\Users\skd53\Downloads\maths and stats for DS\AtliQo bank project phase 1\datasets\customers.csv")
print(df_cust.describe())
df_tran=pd.read_csv(r"C:\Users\skd53\Downloads\maths and stats for DS\AtliQo bank project phase 1\datasets\transactions.csv")
print(df_tran.head())
print(df_tran.shape)
print(df_tran.isnull().sum())
print(df_tran[df_tran.platform.isnull()])

# to fill the na value we have to see which is the most used platform for shopping
sns.countplot(df_tran.platform)
plt.tight_layout()
plt.show()#here we get amazon is the most used platform for the shooping  
print(df_tran.platform.mode())#we will use mode function as to replace the na value with most occuring value  
df_tran["platform"].fillna(df_tran["platform"].mode()[0],inplace=True)
print(df_tran.isnull().sum())

# now lets handle the outlier 
print(df_tran.describe())#here we can see transaction amt is 0 which is seems to be outlier
print(df_tran[df_tran.tran_amount==0])#here i can see that they have same platform , category and payment type
# lets see all the coloumn having platform ,category and payment type is same 
# and then we will take mean or median of that
df_tran_1=df_tran[(df_tran.platform=="Amazon")&(df_tran.product_category=="Electronics")&(df_tran.payment_type=="Credit Card")]
print(df_tran_1)
# we will see all no zeros value and remove their median 
median_value=df_tran_1[df_tran_1.tran_amount>0].tran_amount.median()
print(median_value)
# now we will replace the zero with the median value
df_tran.loc[df_tran.tran_amount==0,"tran_amount"]=median_value
print(df_tran.iloc[[120,141]])
print(df_tran.describe())#now we have minikum transaction amt 2
# we will plot the data in histplot
sns.histplot(df_tran.tran_amount,kde=True)
# plt.show()#we are seeing that the data visualisation is not proper and it is little bit right skewed
# now we will use IQR method to remove outlier and make it normla distribution
Q1,Q3=df_tran.tran_amount.quantile([0.25,0.75])
print(Q1,Q3)
IQR=Q3-Q1
print(IQR)
# upper=Q3+1.5*IQR
# lower=Q1-1.5*IQR
# print(upper,lower)

# here we have seen upper value 933 which is less as point of transaction so here we will use 3*IQR
upper=Q3+3*IQR
lower=Q1-3*IQR
print(upper,lower)#now it is showing 1454 as upper value & do not worry about lower value
# now  we will see values greater than upper value and treat them as a outlier
df_tran_outlier=df_tran[df_tran.tran_amount>upper]
print(df_tran_outlier)#we are seeing transaction of 60000 which could be an outlier

#so to treat this we will take mean of per category product
# why product only ? becoz the average transation amt would be diff for diff product category
df_tran_normal=df_tran[df_tran.tran_amount<upper]
print(df_tran_normal.head())
# now to get mean we will group product with the tran_amount
df_tran_2=(df_tran_normal.groupby("product_category")["tran_amount"].mean())
print(df_tran_2)

df_tran.loc[df_tran_outlier.index,"tran_amount"]=df_tran_outlier["product_category"].map(df_tran_2)
# print(df_tran.loc[df_tran_outlier.index])
print(df_tran.iloc[[26,49]])
print(df_tran.head())

sns.histplot(df_tran.tran_amount,kde=True)
# plt.show()#now it is giving proper graph

# visualising the data
#lets see which payment type is used more
sns.countplot(df_tran["payment_type"]) 
plt.tight_layout()
plt.show() 


# payment type used by age group 
#we need to merge the customer df and transaction df
bins = [18,25,45,65]
labels = ['18-24', '25-44', '45-64']

df_cust['age_group'] = pd.cut(df_cust['age'], bins=bins, labels=labels, right=False)
print(df_cust.head())

merge=pd.merge(df_cust,df_tran,on="cust_id",how="inner")
print(merge.shape)

sns.countplot(data=merge, x='age_group', hue='payment_type')
plt.title(" payment type used by age group")
plt.tight_layout()
plt.show()


sns.countplot(data=merge, x='age_group', hue='product_category')
plt.title(" product category used by age group")
plt.tight_layout()
plt.show()

sns.barplot(data=df_cust,x="age_group",y="annual_income")
plt.title(" annual income of particular age group")
plt.tight_layout()
plt.show()

sns.countplot(data=df_cust,x="age_group",hue="occupation")
plt.title("occupaiton of particular age group")
plt.tight_layout()
plt.show()


# you can draw more insights as per your product manager demands 
