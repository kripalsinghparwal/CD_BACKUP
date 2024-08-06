#################################### filtering shiksha links ###################
import pandas as pd
df1 = pd.read_csv(r"C:\Users\Kripal\Desktop\testing\input_folder\shiksha_url_1.csv")
df2 = pd.read_csv(r"C:\Users\Kripal\Desktop\testing\input_folder\shiksha_url_2.csv")
frames = [df1, df2]
df = pd.concat(frames).drop_duplicates()
print(len(df))

url_list = df['url'].to_list()
filter1_url_list = []
for url in url_list:
    if url.startswith("https://www.shiksha.com/college/") or url.startswith("https://www.shiksha.com/university/"):
        if url.count("/") == 4:
            filter1_url_list.append(url)

rslt_df = df[df['url'].isin(filter1_url_list)]
rslt_df.to_csv("outputShiksha.csv")

# separated_url_list = []
# for url in rslt_df['url'].tolist():
#     splited_list = url.split("/")[:5]
#     separated_url_list.append('/'.join(splited_list))

