#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests

import pandas as pd


# In[2]:


url = 'https://globalmart-api.onrender.com/mentorskool/v1/sales'
headers = {
    'accept': 'application/json',
    'access_token': 'fe66583bfe5185048c66571293e0d358'
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


# In[4]:


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


# In[5]:


url = 'https://globalmart-api.onrender.com/mentorskool/v1/sales'
token = 'fe66583bfe5185048c66571293e0d358'
x = api_call(url,token)


# In[6]:


json_data = x['records']
df_json = pd.json_normalize(json_data)
df_json.head()


# In[7]:


df_json['product.sizes']


# In[8]:


new = df_json['product.sizes'].str.split(",", expand = True)
new


# In[9]:


new[55].notnull()


# In[10]:


new[new[[55]].notnull().all(1)]


# In[11]:


df_json.iloc[114]


# In[12]:


def search_product(product_name,df = df_json):
    for i in range(0,len(df_json)):
        if (df_json['product.product_name'][i] == product_name):
            print(i)


# In[13]:


search_product("Mitel 5320 IP Phone VoIP phone")


# In[14]:


df_json.iloc[7]


# In[15]:


df_json['order.order_purchase_date'] = pd.to_datetime(df_json['order.order_purchase_date'])


# In[16]:


df_json['month'] = pd.DatetimeIndex(df_json['order.order_purchase_date']).month
df_json


# In[17]:


highest_month_sales = df_json.groupby('month')['sales_amt'].apply(lambda x: x.sum()).idxmax()
highest_month_sales


# In[18]:


y=df_json.groupby(df_json['month'])['profit_amt'].apply(lambda x: x.sum()).idxmax()
y


# In[19]:


profit_margin =df_json.groupby('month')['profit_amt'].sum().reset_index().sort_values('month')


# In[20]:


profit_margin


# In[21]:


profit_margin['MoM']= profit_margin['profit_amt'].pct_change()


# In[22]:


profit_margin


# In[23]:


import numpy as np
df_json.replace('null', None, inplace=True)
df_json


# In[24]:



df_json['expected_delivery_date'] = pd.to_datetime(df_json['order.order_estimated_delivery_date'])
df_json['delivered_date'] = pd.to_datetime(df_json['order.order_delivered_customer_date'])

# Create a new column 'delivery_status' using a lambda function
df_json['delivery_status'] = df_json.apply(lambda row: 'Late' if row['delivered_date'] > row['expected_delivery_date'] else 'On Time', axis=1)
df_json


# In[25]:


len(df_json[df_json['delivery_status']=='Late'])


# In[26]:


late_delivery_count = df_json[df_json['delivery_status'] == 'Late'].groupby('order.vendor.VendorID').size().reset_index(name='late_delivery_count')
late_delivery_count


# In[ ]:





# In[ ]:




