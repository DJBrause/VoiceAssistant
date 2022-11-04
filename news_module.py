from newsapi import NewsApiClient
import os
from dotenv import load_dotenv


load_dotenv()
categories = ['business', 'entertainment', 'general', 'health', 'science', 'sports', 'technology']
# # Init
newsapi = NewsApiClient(api_key=str(os.environ.get('news_api')))

# # # /v2/top-headlines
# top_headlines = newsapi.get_top_headlines(language='en')
# #
# # # # /v2/everything
# all_articles = newsapi.get_everything(q='bitcoin',
#                                       sources='bbc-news,the-verge',
#                                       domains='bbc.co.uk,techcrunch.com',
#                                       language='en',
#                                       sort_by='relevancy',
#                                       page=1)
#
#
# x = newsapi.get_everything(q='minecraft', sort_by='relevancy', exclude_domains='https://russian.rt.com, https://lenta.ru, https://www.rbc.ru', from_param='2022-10-16', language='en')
# print(x.keys())
# # print(x['totalResults'])
# for i in x['articles']:
#     print("==================")
#     print(i['source'])
#     print(i['title'])
#     if i['title'] == 'Moscow blocked access to a Ukrainian website for Russian soldiers who want to surrender after it was bombarded with requests':
#         print(i['content'])

# print(top_headlines['articles'][0]['source']['name'])
# s = newsapi.get_sources()
# for i in s['sources']:
#     if i['country'] == 'ru':
#         print(i)


def top_news():
    top_headlines = newsapi.get_top_headlines(page_size=5, page=1, language='en')
    print(top_headlines)
    print(f"top headlines lenght: {len(top_headlines)}")
    headlines_list = []
    for h in range(len(top_headlines)):
        headlines_list.append([top_headlines['articles'][h]['source']['name'], top_headlines['articles'][h]['title']])
    return headlines_list

# top_headlines = newsapi.get_top_headlines(category='business', page_size=5, page=1, language='en', country='us')
#
# x = top_headlines['articles'][]['source']['name']

print(top_news())