import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from utils.evaluation_metrics import evaluate_model

data_frame = pd.read_csv("./data/html_content.csv")
data_frame = data_frame.drop(columns=["url"])

columns = data_frame.select_dtypes(include=[np.number, np.float32]).columns.drop('label')
X = data_frame[columns]
y = data_frame['label']

correlation = X.assign(label=y).corr()['label'].sort_values(ascending=False)
leaky = correlation[abs(correlation) > 0.8].index.tolist()
if leaky:
    X = X.drop(columns=leaky, errors='ignore')


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

pipeline = make_pipeline(
    StandardScaler(),
    LogisticRegression(max_iter=3000, solver='lbfgs', random_state=42, class_weight='balanced')
)

pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)

evaluate_model(data_frame, pipeline, X, y, X_train, X_test, y_train, y_test, y_pred, save_model=True)