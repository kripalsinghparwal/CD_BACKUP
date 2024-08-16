import pandas as pd

names_data = pd.read_csv(r"C:\Users\Kripal\Desktop\testing\indianNamesInputData.csv")

first_name_list = names_data['Name'].unique().tolist()
last_name_list = names_data['Surname'].unique().tolist()
# print(last_name_list)
combined_names_list = []
for i in first_name_list:
    if type(i)!= float:
        for j in last_name_list:
            if type(j) != float:
                combined_names_list.append(i.strip() + " " + j.strip())

print(len(combined_names_list))
print(len(set(combined_names_list)))

output_df = pd.DataFrame(combined_names_list, columns=['Full Name'])
print(output_df)
output_df.to_csv("indianNamesOutputData.csv")