import pandas as pd
rslt_df = pd.read_csv(r"C:\Users\Kripal\Desktop\testing\cleanedUrlSample.csv")

keyword_list = []
keyword_count_list = []
for item in set(rslt_df['keyword'].tolist()):
    keyword_list.append(item)
    keyword_count_list.append(rslt_df['keyword'].tolist().count(item))

count_df = pd.DataFrame()
count_df['keyword'] = keyword_list
count_df['count'] = keyword_count_list

count_df.to_csv("shikshaKeywordCount2.csv")