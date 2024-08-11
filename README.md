# Web - Search - Py
### Overview
WebSearch Py is python library for scrapping search engine results from multiple search engines, providing additional information for each search result such as search engine used, page number of result, resulting ranking on said page etc.

---
### Supported Search Engines
- Google
- Bing
- Duckduckgo
- Yahoo
  
### QuickStart
1. **INITILIZATION**
First import the WebSearch object from the websearch module and initialize it. The constructor of the WebSearch object takes an optional SearchEngine enum as an argument. This enums specifies the search engine to be used. If not SearchEngine enum is passed, the WebSearch object will default to google search.

```python
import websearch

wsp = WebSearch(SearchEngine.GOOGLE)

```
2. **Executing a Search**
To execute a search, simply pass your search term as a python string into the WebSearch object's `search()` function. This function returns a list of Result objects.

```python

wsp = WebSearch(SearchEngine.GOOGLE)
all_results = wsp.search("Dekompiler")

```

### The WebSearch Object
The WebSearch object has various methods that allow you to specify how your searches will be executed
1. **Changing the Search Engine**
To changne the search engine being used, you can use any one of the WebSearch objects following methods:

```python

wsp = WebSearch()
wsp.use_google()
wsp.use_bing()
wsp.use_duckduckgo()
wsp.use_yahoo()

```

2. **Specifying The Page To Search From**
To specify the page from which search results should be scrapped, you can pass a second argument to the WebSearch.search() method. This argument must be an integer.

```python

wsp = WebSearch()
wsp.search("Dekompiler", 5)
wsp.search("Dekomipler", start_page=5)

```

### The Result Object
Each result returned by the WebSearch's search method is a Reulst object. The Result object has various methods that allow you to extract infomration associated with the search result.
1. **Getting the URL**
Perhaps the most import peice of information assocaited with each search result is it's url. This can be extracted using the Result Object's `get_url()` method.

```python

wsp.WebSearch()
all_results  = wsp.search("Dekompiler")
print(all_results[0].get_url())

```
2. **Getting the Page Number**
The page number from which the result was scrapped can be extracted using the `get_page_number()` method.

```python

wsp. WebSearch()
all_results  = wsp.search("Dekompiler")
print(all_results[0].get_page_number())

```

3. **Getting the Ranking**
This allows you to extract the page's rank from the Result object.

```python

wsp.WebSearch()
all_results  = wsp.search("Dekompiler")
print(all_results[0].get_rank())

```

### Disclaimer
This web scraper is intended for educational and personal use only. It is designed to collect data from publicly available sources. The use of this tool must comply with the terms of service, robots.txt directives, and legal guidelines of the websites being scraped. The author is not responsible for any misuse, unauthorized data collection, or legal issues that arise from the use of this scraper. Always obtain permission from website owners before scraping their content.

### To Do List
1. Add support for searching multiple pages at once.
2. Add supoort for more search engines (Yandex, Baidu, Kagi).

### Contact Info
I can be contaced on X [here](https://x.com/dekompiler)
