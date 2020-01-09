# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
autos.info()
autos.head()


# %%
import pandas as pd
import numpy as np 

autos = pd.read_csv('not_cleaned_autos.csv', encoding='Latin-1')



# %%
autos.columns 

#manually change column names
autos.columns = ['date_crawled', 'name', 'seller', 'offer_type', 'price', 'abtest', 'vehicle_type', 'year_of_registration', 'gearbox','power_pS', 'model','odometer', 'month_of_registration', 'fuel_type', 'brand', 'not_repaired_damage', 'date_created', 'num_pictures', 'postal_code','last_seen']

#confirming edits
autos.head()


# %%
autos.describe(include='all') #both numerical and categorical cols
# num pictures col has many NaN values
# odometer col and price are text values






# %%
#Looking into areas that can be cleaned
autos['num_pictures'].value_counts() #all values are zero
autos['seller'].value_counts() # 99.99% of values are 'private'
autos['offer_type'].value_counts() #99.99$ of values are the same
#Nearly all vals in above columns are the same, will remove them in next cell


# %%
autos = autos.drop(["num_pictures", "seller", "offer_type"], axis=1)


# %%
#Converting text values to numeric 
autos["price"] = (autos["price"]).str.replace("$","").str.replace(",","").astype(int)
autos["price"].head() #confirm changes






# %%
#Converting text values to numeric 
autos["odometer"] = (autos["odometer"]).str.replace("km","").str.replace(",","").astype(int)


# %%
#renaming and checking new values
autos.rename({"odometer": "odometer_km"}, axis=1, inplace=True)
autos["odometer_km"].head()


# %%
#Exploring values in odometer_km column, values are rounded. Many more high mileage than low mileage
autos["odometer_km"].value_counts()


# %%
#Price col analysis
print(autos["price"].unique().shape)
print(autos["price"].describe())
print(autos["price"].value_counts())
#1421 cars with 0$ price, remove these rows
#Max car price is 100,000,000. Excessively high 


# %%
#20 highests prices from price column and show counts
autos["price"].value_counts().sort_index(ascending=False).head(20)


# %%
#Sort prices by 20 lowest values and show counts
autos["price"].value_counts().sort_index(ascending=True).head(20)


# %%
#For accuracy, remove any prices above 350000 (unrealistic prices above this) and remove all prices below 1$
autos = autos[autos["price"].between(1, 350001)]
autos["price"].describe()


# %%
#Columns with date values
'''
- `date_crawled`: added by the crawler
- `last_seen`: added by the crawler
- `date_created`: from the website
- `registration_month`: from the website
- `registration_year`: from the website
'''
#Of these 5, date_crawled, ad_created, & last_seen use string values. View how they are formatted
autos[['date_crawled', 'date_created', 'last_seen']][0:5]


# %%
#Select characters that represent only the day. Find distribution of dates 
print(autos['date_crawled']
.str[:10]
.value_counts(normalize=True, dropna=False) #percentages instead of counts
.sort_index()) #sort by earliest to latest (date)

#Site was crawled daily from 2016 March 5th, to 2016 April 7th


# %%
#Select characters that represent only the day. Find distribution of dates 
print(autos['date_crawled']
.str[:10]
.value_counts(normalize=True, dropna=False) #percentages instead of counts
.sort_values()) #sort by distribution in ascending order


# %%
#Similar process as above applied to last_seen col
(autos["last_seen"]
.str[:10]
.value_counts(normalize=True, dropna=False)
.sort_index()
)

#Increased 'last_seen' values in last 3 days of crawler data. Likely because of crawling period ending


# %%
print(autos['date_created'].str[:10].unique().shape) #Num of unique values
(autos['date_created']
.str[:10]
.value_counts(normalize=True, dropna=False)
.sort_index()
)


# %%
autos.rename({'yearOfRegistration': 'registration_year'}, axis=1, inplace=True)
autos["registration_year"].head()


# %%


