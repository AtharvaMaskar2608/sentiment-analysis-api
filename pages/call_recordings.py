import streamlit as st
from db import *
import pandas as pd

response = fetch_all_data()

df = pd.DataFrame(response['data'])

st.table(df)