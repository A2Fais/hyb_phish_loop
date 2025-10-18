import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from xgboost import XGBClassifier
from utils.evaluation_metrics import evaluate_model

data_frame = pd.read_csv("./data/html_content.csv")
data_frame = data_frame.drop(columns=["url"])
drop_cols = [
    "num_images",
    "image_alt_anomaly_ratio",
    "external_css_count",
    "num_images",
    "external_js_count",
    "external_css_count",
    "num_meta_refresh",
    "inline_script_ratio",
]
data_frame = data_frame.drop(columns=[c for c in drop_cols if c in data_frame.columns])
columns = data_frame.select_dtypes(include=[np.number, np.float32]).columns.drop('label')

X = data_frame[columns]
y = data_frame['label']

correlation = X.assign(label=y).corr()['label'].sort_values(ascending=False)
leaky = correlation[abs(correlation) > 0.8].index.tolist()
leaky = [col for col in leaky if col != 'label']
if leaky:
    print(f"Removing potentially leaky features: {leaky}")
    X = X.drop(columns=leaky, errors='ignore')

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

pipeline = make_pipeline(
    StandardScaler(),
    XGBClassifier(
        n_estimators=600,
        learning_rate=0.05,
        max_depth=7,
        subsample=0.9,
        colsample_bytree=0.9,
        min_child_weight=2,
        reg_lambda=1.0,
        reg_alpha=0.3,
        gamma=0.1,
        scale_pos_weight=(y_train.value_counts()[0] / y_train.value_counts()[1]),
        eval_metric="logloss",
        random_state=42,
        n_jobs=-1
    )
)

pipeline.fit(X_train, y_train)
y_pred = pipeline.predict(X_test)

evaluate_model(
    data_frame, pipeline, X, y,
    X_train, X_test, y_train, y_test, y_pred,
    model_name="html_content_model", save_model=True
)
