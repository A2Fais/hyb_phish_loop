import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn import metrics
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.dummy import DummyClassifier
import joblib

data_frame = pd.read_csv('./data/PhiUSIIL_Phishing_URL_Dataset.csv')
data_frame = data_frame.drop_duplicates()
data_frame = data_frame.drop(columns=['FILENAME', 'URL', 'Domain', 'TLD', 'Title', 'URLSimilarityIndex'], errors='ignore')

columns = data_frame.select_dtypes(include=[np.number]).columns.drop('label')
data_frame = data_frame.drop_duplicates(subset=columns, keep='first')
X = data_frame[columns]
y = data_frame['label']

correlation = X.assign(label=y).corr()['label'].sort_values(ascending=False)
leaky = correlation[abs(correlation) > 0.8].index.tolist()
if leaky:
    X = X.drop(columns=leaky, errors='ignore')

drop_cols = [c for c in X.columns if any(s in c.lower() for s in ['domain', 'title', 'url'])]
X = X.drop(columns=drop_cols, errors='ignore')

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

pipeline = make_pipeline(
    StandardScaler(),
    LogisticRegression(max_iter=3000, solver='lbfgs', random_state=42, class_weight='balanced')
)

pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)

print(f"Accuracy: {metrics.accuracy_score(y_test, y_pred):.4f}\n")

print("Classification Report:")
print(metrics.classification_report(y_test, y_pred))

print(f"Duplicated Rows: {data_frame.duplicated().sum()}\n")

print("Confusion Matrix:")
print(f"{metrics.confusion_matrix(y_test, y_pred)}\n")

dummy = DummyClassifier(strategy='most_frequent').fit(X_train, y_train)
print(f"Baseline Accuracy: {metrics.accuracy_score(y_test, dummy.predict(X_test)):.4f}\n")

y_perm = y.sample(frac=1.0, random_state=0).reset_index(drop=True)
scores = cross_val_score(pipeline, X, y_perm, cv=5, scoring='f1', n_jobs=-1)
print(f"Label-Shuffled F1 Mean: {np.mean(scores)}\n")

scores = cross_val_score(pipeline, X, y, cv=5, scoring='f1', n_jobs=-1)
print(f"Cross-validation F1 scores: {scores}\n")
print(f"Mean F1: {np.mean(scores)}\n")

try:
    joblib.dump(pipeline, 'url_phishing_model.joblib')
    print("Model saved successfully!")
except Exception as e:
    print(f"Error saving model: {e}")
