import pandas as pd
from pathlib import Path

is_html_content = True
dir = "./data_sets/html_content_features" if is_html_content else "./data_sets/dom_content_features"
output_file = f"{dir}/HTML_CONTENT_FULL.csv" if is_html_content else f"{dir}/DOM_CONTENT_FULL.csv"

file_name = "HTML_CONTENT_BATCH_*" if is_html_content else "DOM_CONTENT_BATCH_*"
dir_content = Path(dir)
limit = 210 
files = list(dir_content.glob(file_name))

data_frame = [pd.read_csv(file) for file in files]
combined = pd.concat(data_frame, ignore_index=True)
combined.to_csv(output_file, index=False)

print(f"[✔] Combined {len(files)} batch files → {output_file}")