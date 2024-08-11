import requests
from enum import Enum
from bs4 import BeautifulSoup
from typing import List
import pprint
import urllib.parse


class Result:
    """
    Result class that represents a single result from a search engine.
    """
    def __init__(self, url, page, rank, retrieved_from):
        self.url = url
        self.retrieved_from = retrieved_from
        self.page = page
        self.rank = rank

    def __str__(self) -> str:
        return f"{self.url}"

    def print_info(self):
        pprint.pprint({"url": self.url, "retrieved_from": self.retrieved_from, "page": self.page, "rank": self.rank
                       }, sort_dicts=False)

    def get_url(self) -> str:
        return self.url

    def get_page(self) -> int:
        return self.page

    def get_rank(self) -> int:
        return self.rank

    def get_retrieved_from(self) -> str:
        return self.retrieved_from


class SearchEngine(Enum):
    """
    Enum representation of search engines.
    """
    GOOGLE = 1
    BING = 2
    DUCKDUCKGO = 3
    YAHOO = 4


class WebSearch:
    """
    WebSearch class used to make web searches. Multiple search engines supported.
    """
    def __init__(self, search_engine=SearchEngine.GOOGLE):
        self.search_engine = search_engine
        self.user_agents = {
            "google": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:126.0) Gecko/20100101 Firefox/126.0",
            "bing": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/123.0.0.0 Safari/537.36",
            "duckduckgo": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/123.0.0.0 Safari/537.36",
            "yahoo": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                     "Chrome/123.0.0.0 Safari/537.36 OPR/109.0.0.0",
        }

    def get_search_engine(self) -> str:
        match self.search_engine:
            case SearchEngine.GOOGLE:
                return "google"
            case SearchEngine.BING:
                return "bing"
            case SearchEngine.DUCKDUCKGO:
                return "duckduckgo"
            case SearchEngine.YAHOO:
                return "yahoo"

    def search(self, search_term, start_page=1) -> List[Result]:
        headers = {"user-agent": self.user_agents[self.get_search_engine()]}
        payload = {"q": search_term}
        results = ""
        match self.search_engine:
            case SearchEngine.GOOGLE:
                if start_page > 1:
                    payload["start"] = (start_page * 10) - 10
                results = requests.get("https://www.google.com/search", params=payload, headers=headers)
                results = WebSearch.parse_google_results(results, page_number=start_page)
            case SearchEngine.BING:
                if start_page > 1:
                    payload["first"] = (start_page * 10) - 10
                payload["rdr"] = "1"
                results = requests.get("https://www.bing.com/search", params=payload, headers=headers)
                results = WebSearch.parse_bing_results(results, page_number=start_page)
            case SearchEngine.DUCKDUCKGO:
                if start_page > 1:
                    payload["s"] = 73 + ((start_page-1) * 50)
                    payload["dc"] = payload["s"] + 1
                    payload["v"] = "l"
                    payload["o"] = "json"
                    payload["api"] = "d.js"
                    payload["vqd"] = "4-53414639616023508354840431374019649335"
                    payload["kl"] = "wt-wt"
                results = requests.post('https://html.duckduckgo.com/html/', data=payload, headers=headers)
                results = WebSearch.parse_duckduckgo_results(results, page_number=start_page)
            case SearchEngine.YAHOO:
                if start_page > 1:
                    payload["b"] = 1 + (start_page * 7)
                payload["fr2"] = "sb-top"
                payload["iscqry"] = ""
                results = requests.get("https://search.yahoo.com/search;_ylt=AwrFGXE_3rdmG7ElnKBDDWVH;_ylc=X1MDMTE5Nz"
                                       "gwNDg2NwRfcgMyBGZyAwRmcjIDcDpzLHY6c2ZwLG06c2ItdG9wBGdwcmlkAzVaTFdBM2c5UXppNlZH"
                                       "elNOeTk0bkEEbl9yc2x0AzAEbl9zdWdnAzEwBG9yaWdpbgNzZWFyY2gueWFob28uY29tBHBvcwMwBH"
                                       "Bxc3RyAwRwcXN0cmwDMARxc3RybAM2BHF1ZXJ5A2dvb2dsZQR0X3N0bXADMTcyMzMyNjUxNg--",
                                       params=payload, headers=headers)
                results = WebSearch.parse_yahoo_results(results, page_number=start_page)

        return results

    def use_google(self):
        self.search_engine = SearchEngine.GOOGLE

    def use_bing(self):
        self.search_engine = SearchEngine.BING

    def use_duckduckgo(self):
        self.search_engine = SearchEngine.DUCKDUCKGO

    def use_yahoo(self):
        self.search_engine = SearchEngine.YAHOO

    @staticmethod
    def parse_google_results(results, page_number) -> List[Result]:
        page = BeautifulSoup(results.text, "html.parser")
        link_tags = page.find_all("a", attrs={"jsname": "UWckNb"})
        results = []
        for (index, link_tag) in enumerate(link_tags):
            results.append(Result(link_tag["href"], page_number, (index+1), "Google"))
        return results

    @staticmethod
    def parse_bing_results(results, page_number) -> List[Result]:
        page = BeautifulSoup(results.text, "html.parser")
        # Bing results' link tags lack a specific attribute that makes them easy to search for.
        # The simplest way to find them is to first locate the <li> tag that contains them.
        result_containers = page.find_all("li", class_="b_algo")
        link_tags = [container.find("a") for container in result_containers]
        results = []
        for (index, link_tag) in enumerate(link_tags):
            results.append(Result(link_tag["href"], page_number, (index+1), "Bing"))
        return results

    @staticmethod
    def parse_duckduckgo_results(results, page_number) -> List[Result]:
        page = BeautifulSoup(results.text, "html.parser")
        link_tags = page.find_all("a", class_="result__a")
        results = []
        for (index, link_tag) in enumerate(link_tags):
            results.append(Result(link_tag["href"], page_number, (index + 1), "Duckduckgo"))
        return results

    @staticmethod
    def parse_yahoo_results(results, page_number) -> List[Result]:
        page = BeautifulSoup(results.text, "html.parser")
        link_tags = page.find_all("a", class_="fz-20")
        results = []
        for (index, link_tag) in enumerate(link_tags):
            # Yahoo links are embedded in Yahoo URLs that redirect to the actual result URLs
            # These urls must be extracted from the yahoo url and decoded
            # The Yahoo URLs have a URL parameter "RU" (redirect URL) whose value is  the redirect URL
            # Sometimes Yahoo's own links such as links to yahoo maps are in the results
            # These do not have the "RU" parameter and shouldn't be parsed the same way
            url_beginning_index = link_tag["href"].find("RU=") + 3 if link_tag["href"].find("RU=") != -1 else None
            url_end_index = link_tag["href"].find("/RK=2") if link_tag["href"].find("RU=") != -1 else None
            results.append(
                Result(
                    urllib.parse.unquote(link_tag["href"][url_beginning_index:url_end_index]),
                    page_number,
                    (index+1),
                    "Yahoo"
                )
            )
        return results











