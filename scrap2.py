from autoscraper import AutoScraper
import pandas as pd

search = "tomato"
amazon_url="https://www.amazon.in/s?k={}".format(search)

# print(amazon_url)


wanted_list=["https://m.media-amazon.com/images/I/71xAN3RgwQL._AC_UL320_.jpg","Dabur Hommade Tomato Puree, 200g","25"]
scraper=AutoScraper()
result=scraper.build(amazon_url,wanted_list)
data = scraper.get_result_similar(amazon_url,grouped=True)
# print(data)
keys = list(data.keys())
# print(keys)
scraper.set_rule_aliases({str(keys[0]):'ImageUrl',str(keys[1]):'Title',str(keys[-1]):'Price'})
scraper.save("amazon1_in.json")
