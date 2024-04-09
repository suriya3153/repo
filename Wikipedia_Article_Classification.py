import pandas as pd
import numpy as np
import pickle
import streamlit as st
from PIL import Image
import requests
import wikipediaapi

st.header("Wikipedia Article Classification")
  
# loading in the model to predict on the data
pickle_in = open('model_pickles_wiki', 'rb')
classifier = pickle.load(pickle_in)
name = st.text_input("Enter Your Article Name")
wiki = wikipediaapi.Wikipedia(language='en', extract_format=wikipediaapi.ExtractFormat.WIKI)

if(st.button("predict")):
    def numofword(title):
      page_title = title
      page = wiki.page(page_title)
      text = page.text
      words = len(text.split())
      return words
    numof=numofword(name)
    def numrevision(TITLE):
      BASE_URL = "http://en.wikipedia.org/w/api.php"
    
    
      parameters = { 'action': 'query',
                'format': 'json',
                'continue': '',
                'titles': TITLE,
                'prop': 'revisions',
                'rvprop': 'ids|userid',
                'rvlimit': 'max'}
    
      wp_call = requests.get(BASE_URL, params=parameters)
      response = wp_call.json()
    
      total_revisions = 0
    
      while True:
        wp_call = requests.get(BASE_URL, params=parameters)
        response = wp_call.json()
    
        for page_id in response['query']['pages']:
          try:
            total_revisions += len(response['query']['pages'][page_id]['revisions'])
          except KeyError:
            return 0
    
        if 'continue' in response:
          parameters['continue'] = response['continue']['continue']
          parameters['rvcontinue'] = response['continue']['rvcontinue']
    
        else:
          break
    
      return total_revisions
    
    numofrevision=numrevision(name)
    data = [[numof,numofrevision]]
    
    value=classifier.predict([[numof,numofrevision]])
    final=value[0]
    if final==1:
        st.write("{} is featured".format(name))
    else:
        st.write("{} is non-featured".format(name))







