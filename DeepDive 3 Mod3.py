#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests

import pandas as pd

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Now you can access the API key using the environment variable
api_key = os.getenv('API_KEY')
# In[2]:


url = 'https://globalmart-api.onrender.com/mentorskool/v1/sales'
headers = {
    'accept': 'application/json',
    'access_token': api_key
}
try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Check for any HTTP errors
    data = response.json()
    # Process and work with the data here
    print(data)
except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
    
# Fetch 500 records

url = 'https://globalmart-api.onrender.com/mentorskool/v1/sales'
headers = {
    'accept': 'application/json',
    'access_token': 'fe66583bfe5185048c66571293e0d358'
}
pages = []
for offset in range(1, 500, 100):
    parameters = {
        'limit': 100,
        'offset': offset
    }
    response = requests.get(url, headers=headers, params=parameters)
    data = response.json()
    pages.extend(data['data'])
main_dict = {'records': pages}


# In[3]:


def api_call(url,token):
    
    headers = {
        'accept': 'application/json',
        'access_token': token
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Check for any HTTP errors
        data = response.json()
        # Process and work with the data here
        print(data)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

    # Fetch 500 records

    headers = {
        'accept': 'application/json',
        'access_token': token
    }
    pages = []
    for offset in range(1, 500, 100):
        parameters = {
            'limit': 100,
            'offset': offset
        }
        response = requests.get(url, headers=headers, params=parameters)
        data = response.json()
        pages.extend(data['data'])
    main_dict = {'records': pages}
    return main_dict


# In[4]:


url = 'https://globalmart-api.onrender.com/mentorskool/v1/sales'
token = 'fe66583bfe5185048c66571293e0d358'
x = api_call(url,token)


# In[5]:


json_data = x['records']
df_json = pd.json_normalize(json_data)
df_json.head()


# In[6]:


df_json['product.sizes']


# In[7]:


new = df_json['product.sizes'].str.split(",", expand = True)
new


# In[8]:


new[55].notnull()


# In[9]:


new[new[[55]].notnull().all(1)]


# In[10]:


def search_product(product_name,df = df_json):
    for i in range(0,len(df_json)):
        if (df_json['product.product_name'][i] == product_name):
            print(i)


# In[11]:


search_product("Mitel 5320 IP Phone VoIP phone")


# In[12]:


df_json['order.order_purchase_date'] = pd.to_datetime(df_json['order.order_purchase_date'])


# In[13]:


df_json['month'] = pd.DatetimeIndex(df_json['order.order_purchase_date']).month
df_json


# In[ ]:





# In[14]:


highest_month_sales = df_json.groupby('month')['sales_amt'].apply(lambda x: x.sum()).idxmax()
highest_month_sales


# In[15]:


y=df_json.groupby(df_json['month'])['profit_amt'].apply(lambda x: x.sum()).idxmax()
y


# In[16]:


profit_margin =df_json.groupby('month')['profit_amt'].sum().reset_index().sort_values('month')


# In[17]:


profit_margin['MoM']= profit_margin['profit_amt'].pct_change()


# In[18]:


profit_margin


# In[19]:


import numpy as np
df_json.replace('null', None, inplace=True)
df_json


# In[20]:


df_json['expected_delivery_date'] = pd.to_datetime(df_json['order.order_estimated_delivery_date'])
df_json['delivered_date'] = pd.to_datetime(df_json['order.order_delivered_customer_date'])

# Create a new column 'delivery_status' using a lambda function
df_json['delivery_status'] = df_json.apply(lambda row: 'Late' if row['delivered_date'] > row['expected_delivery_date'] else 'On Time', axis=1)
df_json


# In[21]:


len(df_json[df_json['delivery_status']=='Late'])


# In[22]:


late_delivery_count = df_json[df_json['delivery_status'] == 'Late'].groupby('order.vendor.VendorID').size().reset_index(name='late_delivery_count')
late_delivery_count


# In[23]:


df_json[['First Name', 'Last Name', 'blank']]=df_json['order.customer.customer_name'].str.strip().str.split(' ', expand=True)
names = [name for name in df_json['order.customer.customer_name'].unique() if name.split(' ')[0] == 'Alan']
pd.Series(names)


# In[ ]:




