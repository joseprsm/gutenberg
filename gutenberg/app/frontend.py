from typing import Dict, List

import os
import requests
import streamlit as st

URL = os.environ.get('URL', 'http://backend:8001')

st.sidebar.title('Gutenberg 🪶')

target_audience = st.sidebar.text_input(label='Target audience', value='Small businesses')
item_name = st.sidebar.text_input(label='Product/Service name')
item_description = st.sidebar.text_area(label='Product/Service description')
platform = st.sidebar.selectbox(
    label='Platform',
    options=['LinkedIn', 'Facebook', 'Google Search']
)

submitted = st.sidebar.button('Submit')

if submitted:

    response: Dict[str, List[str]] = requests.post(
        url=URL,
        json={
            "item_name": item_name,
            "item_description": item_description,
            "platform": platform,
            "target_audience": target_audience
        }
    ).json()

    for choice in response['choices']:
        st.code(choice)
