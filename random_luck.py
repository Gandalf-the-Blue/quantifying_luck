import pandas as pd
import random
import warnings

simulations = 1000
pool_size = 1000
selection_size = 10
luck_weight = 0.1

# Filter out FutureWarnings
warnings.simplefilter(action='ignore', category=FutureWarning)

overall_data = pd.DataFrame(columns=['simulation_number','count'])

for j in range(0,simulations):


    data = pd.DataFrame(columns=['skill_level', 'luck_level', 'combined_weight'])

    for i in range(pool_size):
        skill = random.random()
        luck = random.random()
        combined_weight = skill * (1 - luck_weight) + luck * luck_weight
        row_data = {'skill_level': skill, 'luck_level': luck, 'combined_weight': combined_weight}
        data = pd.concat([data, pd.DataFrame([row_data])], ignore_index=True)

    # Sort the DataFrame by the 'combined_weight' column in descending order
    data = data.sort_values(by='combined_weight', ascending=False)

    data['luck_inclusive'] = 0
    data.iloc[:selection_size, -1] = 1  

    # Reset the index of the DataFrame
    data = data.reset_index(drop=True)

    # Sort the DataFrame by the 'combined_weight' column in descending order
    data = data.sort_values(by='skill_level', ascending=False)

    data['skill_only'] = 0
    data.iloc[:selection_size, -1] = 1  

    # Reset the index of the DataFrame
    data = data.reset_index(drop=True)

    # Use boolean indexing to filter the rows where both 'skill_only' and 'luck_inclusive' are 1
    filtered_data = data[(data['skill_only'] == 1) & (data['luck_inclusive'] == 1)]

    # Count the number of rows in the filtered DataFrame
    count_rows = len(filtered_data)

    row_data = {'simulation_number': j+1,'count':count_rows}
    print(j)
    overall_data = pd.concat([overall_data, pd.DataFrame([row_data])],ignore_index=True)

overall_data.to_csv('output.csv', index=False)
overall_data['count'] = pd.to_numeric(overall_data['count'])
column_stats = overall_data['count'].describe()

print(f"Summary statistics:")
print(column_stats)