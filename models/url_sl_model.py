import pandas as pd
import numpy as np

data = pd.read_csv('./data/PhiUSIIL_Phishing_URL_Dataset.csv')

feature_cols = [d for d in data if d != 'label']

print(feature_cols)