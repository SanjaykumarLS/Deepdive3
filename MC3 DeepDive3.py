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


df_json.iloc[114]


# In[ ]:




