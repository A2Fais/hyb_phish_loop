import joblib
import numpy as np
from sklearn.model_selection import cross_val_score
from sklearn import metrics
from sklearn.dummy import DummyClassifier

def evaluate_model(data_frame, pipeline, X, y, X_train, X_test, y_train, y_test, y_pred, model_name, save_model=False):
    print(f"Accuracy: {metrics.accuracy_score(y_test, y_pred):.4f}\n")

    print("Classification Report:")
    print(metrics.classification_report(y_test, y_pred, target_names=["Benign", "Phishing"]))

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

    if save_model:
        joblib.dump(pipeline, f"models/trained/{model_name}")
        print("Model saved successfully!")
