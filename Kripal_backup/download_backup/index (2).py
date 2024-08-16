import bs4
import requests
import pandas as pd
from datetime import datetime
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import copy
import re


def remove_special_characters(input_string):
    # Define a pattern to match non-alphanumeric characters
    pattern = r"[^a-zA-Z0-9]"

    # Use the sub() function to replace matching characters with an empty string
    cleaned_string = re.sub(pattern, "", input_string)

    return cleaned_string


def max_matching_continuous_characters(string1, string2):
    string1 = string1.lower()
    string1 = remove_special_characters(string1)
    string2 = remove_special_characters(string2)
    string2 = string2.lower()
    len1 = len(string1)
    len2 = len(string2)

    # Initialize a matrix to store lengths of matching substrings
    match_lengths = [[0] * (len2 + 1) for _ in range(len1 + 1)]

    max_length = 0

    for i in range(1, len1 + 1):
        for j in range(1, len2 + 1):
            if string1[i - 1] == string2[j - 1]:
                match_lengths[i][j] = match_lengths[i - 1][j - 1] + 1
                max_length = max(max_length, match_lengths[i][j])
            else:
                match_lengths[i][j] = 0

    return max_length


def remove_words_inside_brackets(text):
    # Define a regular expression pattern to match words inside square brackets
    pattern = re.compile(r"\[.*?\]")

    # Use sub() method to replace the matched pattern with an empty string
    result = re.sub(pattern, "", text)

    return result


def clean_string(input_string):
    # Remove '\n' and '\t'
    cleaned_string = input_string.replace("\n", "").replace("\t", "")

    # Remove trailing spaces
    cleaned_string = cleaned_string.strip()

    return cleaned_string


df1 = pd.read_csv("./Top 100 Exams - Sheet1.csv")
df2 = pd.read_csv("./Top 100 Exams - Sheet2.csv")

Exam_name_list = list(df1.iloc[:, 1])


Exam_full_name_list = list(df1.iloc[:, 2])

Exam_other_names_list = list(df1.iloc[:, -1])

for i in range(0, len(Exam_full_name_list)):
    Exam_full_name_list[i] = clean_string(
        remove_words_inside_brackets(Exam_full_name_list[i])
    )

Exam_ID_list = list(df1.iloc[:, 0])


title_list = list(df2.iloc[:, 1])

# for i in title_list:
#     i = clean_string(i)

n = len(title_list)

id_list = [0] * n

for i in range(len(Exam_name_list)):
    for j in range(0, n):
        if type(title_list[j]) != float:
            Exam_name = clean_string(Exam_name_list[i])
            Exam_full_name = clean_string(Exam_full_name_list[i]).lower()
            title = clean_string(title_list[j]).lower()
            print("Exam_full_name  :" + Exam_full_name)
            print("Exam_name: " + Exam_name)
            print("title: " + title)
            if (Exam_name in title) or (Exam_full_name in title):
                id_list[j] = Exam_ID_list[i]
                print(Exam_ID_list[i])

            elif type(Exam_other_names_list[i]) != float:
                temp_list = Exam_other_names_list[i].split(",")
                for other_name in temp_list:
                    other_name = clean_string(other_name).lower()
                    if other_name in title:
                        id_list[j] = Exam_ID_list[i]
            match_len = max_matching_continuous_characters(title, Exam_name)
            match_percent = (match_len / len(Exam_name.replace(" ", ""))) * 100
        elif match_percent >= 70:
            id_list[j] = Exam_ID_list[i]
headers = ["Exam ID"]
data = pd.DataFrame(columns=headers)
for i in id_list:
    data.loc[len(data)] = i
data.to_excel("data.xlsx", index=False)
