import requests

url = "https://reddit3.p.rapidapi.com/subreddit"

querystring = {"url":"https://www.reddit.com/r/wallstreetbets"}

headers = {
	"X-RapidAPI-Key": "cdf9ea873fmsh759f999291be613p1b593bjsn008f404997e3",
	"X-RapidAPI-Host": "reddit3.p.rapidapi.com"
}

response = requests.get(url, headers=headers, params=querystring)

print(str(response.json()))