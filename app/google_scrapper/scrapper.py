import requests
import time
from bs4 import BeautifulSoup
from collections import Counter


class Scrapper:
    def __init__(self, phrase, *args, **kwargs):
        self._phrase = phrase
        self._start = 0
        self.user_agent = "Mozilla/5.0 \
            (Macintosh; Intel Mac OS X 11_0_0) \
            AppleWebKit/537.36 (KHTML, like Gecko) \
            Chrome/86.0.4240.198 Safari/537.36"

    @property
    def url(self):
        return f"https://www.google.com/search?q={self._phrase}&num=100&start={self._start}"

    def get_data(self):
        text_data = ""
        results = []

        while True:
            time.sleep(1)
            headers = {"user-agent": self.user_agent}
            response = requests.get(self.url, headers=headers)

            if response.status_code == 200:
                soup = BeautifulSoup(response.content, "html.parser")

                title_and_description = soup.find("div", {"id": "res"})
                data = title_and_description.find_all("div", {"class": "rc"})
                print(data)
                if not data:
                    break
                else:
                    text_data += title_and_description.text
                    for idx, res in enumerate(data):
                        position = self._start + idx + 1
                        link = res.find("div", {"class": "yuRUbf"}).a["href"]
                        results.append({"position": position, "link": link})
                    self._start += 100
            else:
                break

        most_common = self.get_most_common_words(text_data, 10)
        context = {"most_common": most_common, "results": results}
        return context

    def get_most_common_words(self, text, n):
        text = text.translate({ord(c): None for c in '"!@#$%^&*()_+.,?\n'})
        splitted = text.lower().split()
        filtered = filter(lambda x: len(x) > 3, splitted)
        counter = Counter(filtered)
        return counter.most_common(n)
