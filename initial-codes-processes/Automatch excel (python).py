import pandas as pd

# Assuming your data is in two separate lists or columns
column_A = ['value1', 'value2', 'value3', 'value4', 'value5']
column_D = ['value2', 'value4', 'value1', 'value5', 'value3']
column_E = ['result2', 'result4', 'result1', 'result5', 'result3']

# Create a DataFrame from the lists
df = pd.DataFrame({'A': column_A, 'D': column_D, 'E': column_E})

# Perform the matching using pandas indexing and matching functions
result = df.loc[df['D'] == df.at[0, 'A'], 'E'].values[0]

print(result)
