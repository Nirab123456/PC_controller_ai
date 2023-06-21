from Data_collection_pandas import pandas_data_collection
import pandas as pd
import time 

# Instantiate the pandas_data_collection class
pdc = pandas_data_collection()

inner_dfs = []  # Create an empty list to store the dataframes for each inner loop
outer_dfs = []  # Create an empty list to store the merged dataframes for each outer loop

for outer_loop in range(2):
    for inner_loop in range(1):
        df = pdc.base_df()
        inner_dfs.append(df)

    # Concatenate the dataframes from the inner loop
    merged_df = pd.concat(inner_dfs, ignore_index=True)
    outer_dfs.append(merged_df)

    inner_dfs = []  # Clear the list of inner dataframes

# Merge the dataframes from the outer loop
result_df = pd.concat(outer_dfs, ignore_index=True)
result_df.to_csv('your_personal_df.csv', index=False)