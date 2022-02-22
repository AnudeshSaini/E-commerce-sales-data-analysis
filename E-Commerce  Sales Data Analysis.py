#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import basic libararies which are helpful in  data cleaning , manipulation & visualization .
import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
get_ipython().run_line_magic('matplotlib', 'inline')
import seaborn as sns
matplotlib.rcParams["figure.figsize"] = (18,8)
import klib


# In[2]:


# Import all three datasets 
detail = pd.read_csv("Sales Details.csv")
order = pd.read_csv("Sales Orders.csv")
target = pd.read_csv("Sales Targets.csv")


# In[3]:


detail.head(2)


# In[4]:


order.head(2)


# In[5]:


target.head(2)


# ## Exploring Datasets

# In[6]:


# Show me No. (rows, columns) of datasets
print(detail.shape)
print(order.shape)
print(target.shape)


# In[7]:


# show me basic information about my datasets
print(detail.info())
print(order.info())
print(target.info())


# In[8]:


# show unique values in each coloums
print(detail.nunique())
print(order.nunique())
print(target.nunique())


# In[9]:


# Drop duplicates from  datasets
detail.drop_duplicates(keep="first",inplace = True)
order.drop_duplicates(keep="first",inplace = True)
target.drop_duplicates(keep="first",inplace = True)


# In[10]:


# show me "Null" values in detail dataset
sns.heatmap(detail.isnull())
matplotlib.rcParams["figure.figsize"] = (15,3) 


# In[11]:


# show me "Null" values in order dataset
sns.heatmap(order.isnull())
matplotlib.rcParams["figure.figsize"] = (15,3) 


# In[12]:


# show me "Null" values in target dataset
sns.heatmap(target.isnull())
matplotlib.rcParams["figure.figsize"] = (15,3) 


# In[13]:


# Merge both detail & order dataset on the basis of there order ID
sales = pd.merge(detail, order, on='Order ID', how='left')


# In[14]:


# Show Max columns or Rows
pd.set_option("display.max_columns", None)
pd.set_option("display.max_rows", None)


# In[15]:


#Add new columns for month,year in sales dataset
sales["Year"] = pd.DatetimeIndex(sales["Order Date"]).year
sales["Month"] = pd.DatetimeIndex(sales["Order Date"]).month


# In[16]:


sales.head(2)


# ## Handle Outliers
# 1) Check the distribution of data for  detecting outliers 
# 
# 2) Take action to remove outiers
# 
# 

# In[17]:


sales.describe()


# In[18]:


sales["Amount"].quantile(.99)


# In[19]:


sales["Amount"].quantile(.1)


# In[20]:


sales["Profit"].quantile(.99)


# In[21]:


sales["Profit"].quantile(.01)


# In[22]:


outliers = sales[(sales["Profit"]<=(-400)) & (sales["Amount"] >= (24))].index 
outliers 


# In[23]:


sales.drop(outliers, inplace =True)


# In[24]:


#Nos. of dedecting outliers
outliers.value_counts().sum()


# ## Analysis & Visualization 

# ### Q.1 Which states are generating highest amount of sales ? 
# 

# In[25]:


# Madhya Pradesh is generated highest amount of sales.
sales.groupby("State")["Amount"].sum().sort_values( ascending= False)[:5].plot.bar(color="crimson")
plt.xticks(rotation=0, fontsize=15 , color = "black" )
plt.yticks(rotation=0, fontsize=15 , color = "black" )
plt.rcParams["figure.figsize"] = (18,8)
plt.ylabel("Sales Amount",fontsize=15, color="r")
plt.xlabel("States",fontsize=15, color="r")
plt.title(" Highest Sales Generating States", fontsize=20, color="r")
plt.show()


# ### Q.2 Which are the top most selling sub-categories by amount ? 

# In[26]:


#  Prinetrs are the highest selling subcategory
sales_sub_cat = sales.groupby("Sub-Category")["Amount"].sum().sort_values(ascending = False).plot.bar(color="darkcyan")
plt.xticks(rotation=60, fontsize=15 , color = "black" )
plt.rcParams["figure.figsize"] = (18,8)
plt.xlabel("Name of Products",fontsize=15, color="r")
plt.ylabel("Sales Amount",fontsize=15, color="r")
plt.title("Most Selling Sub-Category", fontsize=20, color="r")
plt.show()


# ### Q.3 Which Category is most Proffitable ?

# In[27]:


# Electronics is most proffitable category
sales_profit = (sales.groupby("Category")["Profit"].sum().sort_values(ascending=False))
sales_profit


# In[28]:


sales_profit = (19634,12018,10189)
cat=["Electronics","Clothing","Furniture"]
plt.pie (x=sales_profit, labels = cat ,colors = ["green" , "blue", "orange",], startangle=90, autopct = "%0.1f%%" ,explode=[0.05,0.05,0.05], radius= .8)
plt.title( "Profit ratio by Category" ,fontsize=20)
plt.show()


# ### Q.4 Which Category genrates most amount of sales ?

# In[29]:


# Electronics category generated highest amount of sales 
sales_amt = sales.groupby(['Category'])['Amount'].sum().reset_index().sort_values(by=["Amount"],ascending=False)
sales_amt


# In[30]:


sales_amount = (150905,137060,116370)
cat=["Electronics","Clothing","Furniture"]
plt.pie (x=sales_amount, labels = cat ,colors = ["yellow" , "violet", "green",], startangle=90, autopct = "%0.1f%%" , explode=[0.05,0.05,0.05], radius= .8)
plt.title( "Sales Ratio by Category " ,fontsize=20)
plt.show()


# ### Q.5 Which are the 10 top most proffitable orders ?

# In[31]:


sales.sort_values(by=["Profit"], ascending= True).reset_index()[:10]


# ### Q.6 Top 5 cutomers who have spent the most amount ?

# In[32]:


# Pooja spent highest amount on orders 
sales.groupby(["CustomerName","State"])["Amount"].sum().sort_values(ascending=False).head(5).plot.bar(color="darkcyan")
plt.xticks(rotation=0, fontsize=15 , color = "black" )
plt.yticks(rotation=0, fontsize=15 , color = "black" )
plt.rcParams["figure.figsize"] = (18,8)
plt.ylabel("Sales Amount",fontsize=15, color="r")
plt.xlabel("Customer name with State",fontsize=15, color="r")
plt.title(" Top 5 Customers", fontsize=20, color="r")
plt.show()


# ### Q.7 Which are the Top 10 states with most number of purchased items/ orders ?

# In[33]:


cat_order = sales.groupby(['State'])['Category'].agg("count").sort_values(ascending=False).head(10)
state = cat_order.keys()
orders = [340,290,87,74,74,68,63,62,60,54]


# In[34]:


sns.barplot(x=state, y=orders, palette="viridis")
plt.xticks (rotation= 0 , fontsize=15 , color = "black" )
plt.yticks(fontsize=15 , color = "black" )
plt.rcParams["figure.figsize"] = (18,8)
plt.ylabel("Nos of orders",fontsize=20, color="r")
plt.xlabel("State Name",fontsize=20, color="r")
plt.title("Top 10 States with highest number of orders ", fontsize=20, color="r")
plt.show()


# ### Q.8 What is total amount of sales genrated per month ?

# In[35]:


# January generates highest amount of sales
sales.groupby("Month")["Amount"].sum().sort_values(ascending=False).plot.bar(color="darkcyan")
plt.xticks (rotation= 0 , fontsize=15 , color = "black" )
plt.yticks(fontsize=15 , color = "black" )
plt.rcParams["figure.figsize"] = (18,8)
plt.ylabel("Sales Amount",fontsize=20, color="r")
plt.xlabel("Months",fontsize=20, color="r")
plt.title("Total Amount of Sales (Per Month)  ", fontsize=20, color="r")
plt.show()


# ### Q.9 What is the amount of Profit generated per month ?

# In[36]:


# January generates highest amount of profit
sales.groupby("Month")["Profit"].sum().plot.bar(color="crimson")
plt.xticks (rotation= 0 , fontsize=15 , color = "black" )
plt.yticks(fontsize=15 , color = "black" )
plt.rcParams["figure.figsize"] = (18,8)
plt.ylabel("Sales Amount",fontsize=20, color="r")
plt.xlabel("Months",fontsize=20, color="r")
plt.title("Total Amount of Profit/Loss (Per Month) ", fontsize=20, color="r")
plt.show()


# ### Q.10  Show me data of Sales Target v/s Actual sales generated ? 

# In[37]:


# Sales Target v/s Actual amount of Sales
target.groupby("Month of Order Date")["Target"].sum().sort_values(ascending=False).plot(color="crimson", label="Target")
sales.groupby("Month")["Amount"].sum().sort_values(ascending=False).plot.bar(color="Darkcyan",label= "Actual Sales")
plt.xticks (rotation= 0 , fontsize=15 , color = "black" )
plt.yticks(fontsize=15 , color = "black" )
plt.rcParams["figure.figsize"] = (18,8)
plt.ylabel("Amount",fontsize=20, color="r")
plt.xlabel("Months",fontsize=20, color="r")
plt.title(" Sales Target v/s Actual Amount of Sales (Per month)", fontsize=20, color="r")
plt.legend(loc="upper right",fontsize=20)
plt.show()


# ### Q.10 Sales target by Categories?

# In[38]:


sales_target = target.groupby("Category")["Target"].sum()
pd.DataFrame(sales_target)


# ### Q.11 Actual sales by Categories ?

# In[39]:


actual_sales = sales.groupby("Category")["Amount"].sum()
pd.DataFrame(actual_sales)


# ### Q.12 Profit/Loss in sales by categories ?

# In[40]:


# Electronics is in loss else two are in profit
Profit_loss = sales_target-actual_sales
pd.DataFrame(Profit_loss)


# ### Q.13 Total amount of revenue generated ?

# In[41]:


total_revenue = sales["Amount"].sum()
total_revenue 


# ### Q.14 Total amount of profit generated ?

# In[42]:


total_profit = sales["Profit"].sum()
total_profit


# ### Q.15 What is the Net profit  ?

# In[43]:


net_profit = total_revenue-total_profit 
net_profit


# ## Finally,we are here with some results:
# 
# ### 1) According to analysis Madhya Pradesh is our best performing  state.
# 
# ### 2) Electronics category generated highest amount of sales & it is most proffitable too.
# 
# ### 3) Our Net Profit is 362494.
# 
# ### 4) January month has highest sales & it is most proffitable too.
# 
# ### 5) We could not reach at our targets in Electronics Category.
# 
# 
# 
