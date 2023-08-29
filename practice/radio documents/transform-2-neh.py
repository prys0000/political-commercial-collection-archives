import pandas as pd

# Read source and target excel files
df_source = pd.read_excel(r'C:\Users\user\Desktop\NEH ACSC\Process-1-NEH-Test\corrected_file.xlsx')
df_target = pd.read_excel(r'C:\Users\user\Desktop\NEH ACSC\Owen_test\ACDAP_test_Owen.xlsx')


# list of column mappings. Each entry is a tuple: (target_column_name, source_column_name)
column_mappings = [
    ('Title', 'Title'),
    ('Created', 'Date_1_Label'),
    ('Date', 'Date_1_ Begin'),
    ('Creator', 'Agent_1_header_string'),
    ('Language', 'Language'),
    ('Congress', 'Subject_2_Term'),
    ('Physical Location', 'Component Unique Identifier'),
    ('Identifier', 'Component Unique Identifier'),
    ('Preview', 'URL of thumbnail'),
    ('Available at', 'URL of Linked-out digital object'),
    ('Record type', 'Container Instance Type'),
    ('Format Type', 'Grandchild type'),
    ('Topic', 'Subject_1_Term'),
    ('Extent', 'Extent number'),
    ('Description', 'Scope and Contents'),
    ('Policy Area', 'General')
]

for target_col, source_col in column_mappings:
    if source_col in df_source.columns:
        df_target[target_col] = df_source[source_col]

df_source['Date_1_ Begin'] = pd.to_datetime(df_source['Date_1_ Begin'])

# For 'Contributing institution', as this is a static string, directly assign it.
df_target['Contributing institution'] = "Carl Albert Congressional Research and Studies Center Archives"

# For 'Rights', as this is a static string, directly assign it.
df_target['Rights'] = "Materials from the Carl Albert Center Archives are available free of charge and are open to the public for use, unless otherwise indicated in the collection finding aid."

# For 'Collection title', as this is a static string, directly assign it.
df_target['Collection title'] = "Robert L. Owen Collection CAC_CC_043"

# For 'Collection finding aid', as this is a static string, directly assign it.
df_target['Collection finding aid'] = "https://arc.ou.edu/repositories/3/resources/32"

# handle other columns as necessary
# ...

# Write the modified target DataFrame to a new Excel file
df_target.to_excel('NEWowentest_updated_target.xlsx', index=False)
