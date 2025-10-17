import pandas as pd
import numpy as np
import joblib

url_pipe = joblib.load('./models/trained/url_lexical_model.pkl')
html_pipe = joblib.load('./models/trained/html_content_model.pkl')
dom_pipe = joblib.load('./models/trained/dom_content_model.pkl')

url_df = pd.read_csv('./data/phiusiil.csv')
url_df = url_df.drop_duplicates()
url_df = url_df.drop(columns=['FILENAME', 'URL', 'Domain', 'TLD', 'Title', 'URLSimilarityIndex'], errors='ignore')

url_cols = url_df.select_dtypes(include=[np.number]).columns.drop('label')
url_df = url_df.drop_duplicates(subset=url_cols, keep='first')
X_url = url_df[url_cols]
y_url = url_df['label']
drop_cols = [c for c in X_url.columns if any(s in c.lower() for s in ['domain', 'title', 'url'])]
X_url = X_url.drop(columns=drop_cols, errors='ignore')

html_df = pd.read_csv("./data/html_content.csv")
html_df = html_df.drop(columns=["url"])
columns = html_df.select_dtypes(include=[np.number, np.float32]).columns.drop('label')
X_html = html_df[columns]
y_html = html_df['label']

dom_df = pd.read_csv("./data/dom_content.csv")
dom_df = dom_df.drop(columns=["URL"])
is_nans = dom_df.isna().sum()
dom_df = dom_df.fillna(dom_df.mean())
bool_columns = dom_df.select_dtypes(include=["bool"]).columns
dom_df[bool_columns] = dom_df[bool_columns].astype(int)
dom_cols = dom_df.select_dtypes(include=[np.number, np.float32]).columns.drop('label')
X_dom = dom_df[dom_cols]
y_dom = dom_df['label']

y_pred_url = url_pipe.predict_proba(X_url)[:,1]
y_pred_html = html_pipe.predict_proba(X_html)[:,1]
y_pred_dom = dom_pipe.predict_proba(X_dom)[:,1]

min_len = min(len(y_pred_url), len(y_pred_html), len(y_pred_dom), len(y_url))
combined_df = pd.DataFrame({
    'URL': y_pred_url[:min_len],
    'HTML': y_pred_html[:min_len],
    'DOM': y_pred_dom[:min_len],
    'LABEL': y_url.values[:min_len]
})

print(combined_df.head(50))
print(combined_df.describe())