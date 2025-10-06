import pandas as pd
import glob

files = sorted(glob.glob("html_features_batch_*.csv"))

dfs = [pd.read_csv(f) for f in files]
combined = pd.concat(dfs, ignore_index=True)

combined.to_csv("html_features_all.csv", index=False)

print(f"[✔] Combined {len(files)} batch files → html_features_all.csv")
