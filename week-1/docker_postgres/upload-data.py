#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


pd.__version__


# In[3]:


df = pd.read_csv('yellow_tripdata_2021-01.csv',nrows=100)


# In[5]:


df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)


# In[6]:


from sqlalchemy import create_engine


# In[7]:


engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')


# In[8]:


engine.connect()


# In[9]:


print(pd.io.sql.get_schema(df, name='yellow_taxi_data', con=engine))


# In[10]:


df_iter = pd.read_csv('yellow_tripdata_2021-01.csv', iterator=True, chunksize=100000)


# In[11]:


df = next(df_iter)


# In[12]:


len(df)


# In[13]:


df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)


# In[14]:


df


# In[15]:


df.head(n=0).to_sql(name='yellow_taxi_data', con=engine, if_exists='replace')


# In[16]:


from time import time


# In[17]:


while True: 
    t_start = time()

    df = next(df_iter)

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
    
    df.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')

    t_end = time()

    print('inserted another chunk, took %.3f second' % (t_end - t_start))


# In[ ]:




