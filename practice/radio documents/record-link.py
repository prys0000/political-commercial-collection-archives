import pandas as pd
import recordlinkage

# Load the Excel data into pandas DataFrames
df1 = pd.read_excel(r'D:\GITHUB\Practice\state-ad-modified.xlsx', index_col=0)  # Replace with your actual file path
df2 = pd.read_excel(r'D:\GITHUB\Practice\names-states-mod.xlsx', index_col=0)  # Replace with your actual file path

# Indexation step
indexer = recordlinkage.Index()
indexer.full()
pairs = indexer.index(df1, df2)

# Comparison step
compare = recordlinkage.Compare()

for col in df1.columns:
    if df1[col].dtype == object:  # if column has text
        compare.string(col, col, method='jarowinkler', threshold=0.85, label=col)
    else:  # if column has numeric or boolean values
        compare.exact(col, col, label=col)

features = compare.compute(pairs, df1, df2)

# Classification step
matches = features[features.sum(axis=1) > len(df1.columns) * 0.75]  # Adjust this threshold according to your needs
print(matches)
