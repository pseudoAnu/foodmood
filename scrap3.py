from re import search
from autoscraper import AutoScraper
import pandas as pd

amazon_scraper = AutoScraper()
amazon_scraper.load('amazon1_in.json')

search = "cardamom"
amazon_url="https://www.amazon.in/s?k={}".format(search)

data = amazon_scraper.get_result_similar(amazon_url, group_by_alias=True)
search_data = tuple(zip(data['Title'],data['ImageUrl'],data['Price']))
# print(search_data)

df = pd.DataFrame(columns=['Title','Price','ImageUrl'])
for i in range(len(search_data)):
    df.loc[len(df)] = [search_data[i][0],search_data[i][-1],search_data[i][-2]]

# print(df.shape)
# print(df.loc[[0],["Title","Price"]])
df.to_csv("searchedData1.csv",index=False)