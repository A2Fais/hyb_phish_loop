import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier
from sklearn import metrics
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

data = pd.read_csv('./data/PhiUSIIL_Phishing_URL_Dataset.csv')
columns = data.select_dtypes(include=[np.number]).columns.tolist()
columns = [col for col in columns if col != 'label']

X = data[columns]
y = data['label']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

logreg = make_pipeline(
    StandardScaler(),
    XGBClassifier(random_state=16, n_estimators=3000, learning_rate=0.1)                      
)

logreg.fit(X_train, y_train)
y_pred = logreg.predict(X_test)

print(f"Accuracy: {metrics.accuracy_score(y_test, y_pred)}\n")

print("Classification Report:")
print(f"{metrics.classification_report(y_test, y_pred, target_names=['BENIGN', 'LEGITIMATE'])}")

print("Confusion Matrix:")
print(metrics.confusion_matrix(y_test, y_pred))