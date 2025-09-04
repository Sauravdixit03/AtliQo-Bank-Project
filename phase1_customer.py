import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#firstly clean data by removing outliers and nulll value and than visualize the data

df_cust=pd.read_csv(r"C:\Users\skd53\Downloads\maths and stats for DS\AtliQo bank project phase 1\datasets\customers.csv")
print(df_cust.describe())

print(df_cust.isnull().sum())#always treat null values first than treat outliers
# only annual income have null value
print(df_cust[df_cust.annual_income.isna()].head(4))

# We can handle these null values using different ways,
# 1. **Remove them**: Since there are 50 of them in a dataframe of 1000, we will not remove them as we don't want to loose some important records
# 1. **Replace them with mean or median**: It is suggested with use median in the case of income. This is because in an income data there could be outliers and median is more robust to these outliers
# 1. **Replace them with median per occupation**: Occupation wise median income can vary. It is best to use a median per occupation for replacement

print(df_cust[df_cust.occupation=="Artist"].annual_income.median())
# this is the way we are going to use to remove the median for each occupation
print(df_cust.groupby("occupation")["annual_income"].median())

# the below method is used to fill null value
# chat gpt prompt ( replace the null values in the annual_income column with the median based on each occupation)
df_cust["annual_income"] = df_cust["annual_income"].fillna(df_cust.groupby("occupation")["annual_income"].transform("median"))
print(df_cust.isnull().sum())#no null value remained
print(df_cust.iloc[[14,82]])#now they have anuual income
# now i will plot the annual income 
sns.histplot(df_cust["annual_income"],color="green")
plt.title("Histogram of annual income")
plt.show()

#now Age and annual income both have outliers 


# so lets begin with treating outlier of annual income
#  
# annual income should not be less than 100
print(df_cust[df_cust.annual_income<100])
df_cust.loc[df_cust["annual_income"] < 100, "annual_income"] = df_cust.loc[df_cust["annual_income"] < 100].apply(
    lambda row: df_cust[df_cust["occupation"] == row["occupation"]]["annual_income"].median(), axis=1
)#chat gpt
print(df_cust.iloc[[31,316]])
# lets do data visualisation of average anuual income according to occupation 
anuual_income_data=df_cust.groupby("occupation")["annual_income"].mean().reset_index()
print(anuual_income_data)
sns.barplot(x="occupation",y="annual_income",data=anuual_income_data)
plt.xlabel("occupation")
plt.ylabel("Average anuual income($)")
plt.title('Average Annual Income Per Occupation')
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

# lets plot graph for all the categories coloumn in the data except age because it has outlier
categorical_columns = ['gender', 'location', 'occupation', 'marital_status']
# we will  apply for loop to each coloumn 
for col in categorical_columns:
    anuual_income_data=df_cust.groupby(col)["annual_income"].mean().reset_index()
    sns.barplot(x=col,y="annual_income",data=anuual_income_data)
    plt.xlabel(col.capitalize())
    plt.ylabel("Average anuual income($)")
    plt.title(f'Average Annual Income Per {col.capitalize()} ')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()

# so lets begin with treating outlier of age
print(df_cust.describe())
# age is valid only if it is between 15 and 80 years.
print(df_cust[(df_cust.age<15)|(df_cust.age>80)])
print(df_cust[df_cust.occupation=="Artist"].age.median())
outliers=df_cust.groupby("occupation")["age"].median()
print(outliers)
df_cust.loc[(df_cust.age<15)|(df_cust.age>80), "age"] = df_cust.loc[(df_cust.age<15)|(df_cust.age>80)].apply(
    lambda row: df_cust[df_cust["occupation"] == row["occupation"]]["age"].median(), axis=1)
print(df_cust.iloc[[0,41]])
print(df_cust.age.describe())
print(df_cust.describe())

# from chat gpt prompt(i want to add the new age group in to my df_cust within the age range of 18-65 like )
bins = [18,25,45,65]
labels = ['18-24', '25-44', '45-64']

df_cust['age_group'] = pd.cut(df_cust['age'], bins=bins, labels=labels, right=False)
print(df_cust.head())
#  now we need to find how  many people belongs in which age category
# normalize func is used to convert in percentage
age_group_counts=df_cust.age_group.value_counts(normalize=True)*100
print(age_group_counts)
# now plotting the pie chart of age coloumn
plt.figure()
plt.pie(age_group_counts,labels=age_group_counts.index,autopct="%00.0f%%")
plt.title("Age group distribution")
plt.show()

# Now analyzing customer distribution by gender  and location
customer_location_gender=df_cust.groupby(["location","gender"]).size().unstack()
# Groups the DataFrame by both location and gender.
# size() how many customers are in each (location, gender) pair.
# Converts the grouped data from a Series into a DataFrame
print(customer_location_gender)
customer_location_gender.plot(kind="bar",stacked=True,color=["green","yellow"])
plt.xlabel("Location")
plt.ylabel("count")
plt.title("customer distribution by gender  and location".capitalize())
plt.tight_layout()
plt.show()
