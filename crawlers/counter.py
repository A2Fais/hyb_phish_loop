import pandas as pd
from pathlib import Path

is_html_content = True
dir = "./data_sets/html_content_features" if is_html_content else "./data_sets/dom_content_features"
output_file = f"{dir}/HTML_CONTENT_FULL.csv"

file_name = "HTML_CONTENT_BATCH_*" if is_html_content else "DOM_CONTENT_BATCH_*"
dir_content = Path(dir)
files = list(dir_content.glob(file_name))

data_frame = pd.concat([pd.read_csv(file) for file in files], ignore_index=True)
label_counts = data_frame['label'].value_counts()
print(label_counts)

read_file = pd.read_csv("./data_sets/html_content_features/HTML_CONTENT.csv")
print(read_file['label'].value_counts())

read_file = pd.read_csv("./data_sets/dom_content_features/DOM_CONTENT.csv")
print(read_file['label'].value_counts())
