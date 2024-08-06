import pandas as pd
a=400
b=517
query_data=pd.read_csv('/home/cd_scrapers/aashish/institute/query_data_tranning.csv')
querys=query_data['query'].dropna().to_list()
exams=query_data['exam name'].dropna().to_list()[a:b]
citys=query_data['city name'].dropna().to_list()
input_data=pd.DataFrame(columns=['Keywords'])

for exam in exams:
    for query in querys:
        for city in citys:
            generated_query=query.replace('"Exam Name"',exam).replace('"City Name"',city)             
            input_data = input_data.append({'Keywords': generated_query}, ignore_index=True)
input_data.to_csv(f'/home/cd_scrapers/aashish/institute/genrated_query_tranning{a}-{b}.csv',index=False)            