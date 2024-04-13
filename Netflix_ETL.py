#!/usr/bin/env python
# coding: utf-8

# In[101]:


import pandas as pd
import boto3


# In[8]:


# Loading csv
df = pd.read_csv(r"C:\Users\tomar\Downloads\netflix_titles.csv.zip")


# In[14]:


df


# In[59]:


# Dropping Null Values

df.dropna(inplace = True)


# In[64]:


df


# In[67]:


# transforming duration col for analysis

# Extract the numeric portion from 'duration' column

df['duration_in_min'] = df['duration'].str.extract('(\d+)',expand = False).astype(float)

# df['duration_in_min'] = df['duration_in_min'].fillna(0)

# Convert 'seasons' to minutes (assuming 1 season = 10 episodes and each episode is 30 minutes)

df.loc[df['duration'].str.contains('Seasons'), 'duration_in_min'] *= 10*30


# In[68]:


df.head(50)


# In[24]:


# Convert the 'date_added' column to datetime format

df['date_added'] = pd.to_datetime(df['date_added'])


# In[25]:


df['date_added']


# In[104]:


# Content Analysis by Type

content_type_counts = df['type'].value_counts()
print("Content Type Distribution:")
print(content_type_counts)


# In[103]:


# Top 10 Directors

Top_Directors = df['director'].value_counts().head(10)
print('\n Top 10 Directors')
print(Top_Directors)


# In[23]:


# Geographical Analysis

Content_by_Country = df['country'].value_counts().head(10)
print('\n Content by Country')
print(Content_by_Country)


# In[38]:


# Extracting the year from the 'date_added' column and create a new column 'year_added'

df['year_added'] = df['date_added'].dt.year.astype(str).apply(lambda x: x.replace('.0',''))


# In[39]:


df


# In[88]:


# Counting number of content additions for each year and sorting it by year

content_by_year = df['year_added'].value_counts().sort_index(ascending = True)

print('\n Content added over time:')
print('year', 'content_added')
print(content_by_year)


# In[76]:


# Rating and duration analysis

average_duration_in_min = df.groupby('type')['duration_in_min'].mean().round(2)
print('\n Average duration in mins by content type')
print(average_duration_in_min)


# In[75]:


# Genre analysis

content_by_genre = df['listed_in'].value_counts()
print('\n Content Distribution by Genre')
print(content_by_genre)


# In[96]:


# dropping duration as we have transformed it into a now column
df.drop('duration',axis = 'columns',inplace = True)


# In[81]:


df.head(20)


# In[90]:


# Top 10 Content by rating type

content_by_rating = df['rating'].value_counts().sort_values(ascending = False).head(10)
print('\n Content by Rating')
print(content_by_rating)


# In[91]:


df


# In[98]:


# dropping year_added as it is not required now
df.drop('year_added',axis = 1, inplace = True)


# In[99]:


df


# In[100]:


# Exporting dataset containing Analysis result to a CSV file

df.to_csv('Netflix_analysis.csv', index = False) 


# In[102]:


# Connecting to S3 storage

# Initialize boto3 client for s3

s3 = boto3.client('s3')

# Upload csv file to s3

bucket_name = 'netflix-etl-data'
file_name = 'Netflix_analysis.csv'
s3_key = '************'

s3.upload_file(file_name,bucket_name,s3_key)



# In[ ]:




