from collections import Counter
import time

from bs4 import BeautifulSoup
import requests
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import HardwareType


class Scrapper:
    def __init__(self, *args, **kwargs):
        self._phrase = kwargs.get("phrase")
        self._start = 0
        self._text_data = ""
        self._results = []
        self._init_random_user_agent()
        self._init_context()

    @property
    def url(self):
        return f"https://www.google.com/search?q={self._phrase}&num=100&start={self._start}"

    def _get_response(self):
        headers = {"user-agent": self.user_agent}
        return requests.get(self.url, headers=headers)

    def _get_data_from_html(self, html):
        soup = BeautifulSoup(html, "html.parser")
        title_and_description = soup.find("div", {"id": "res"})
        if not title_and_description:
            text_data = ""
        else:
            text_data = title_and_description.text
        rows = title_and_description.find_all("div", {"class": "rc"})
        return {"text_data": text_data, "rows": rows}

    def _init_random_user_agent(self):
        hardware_types = [HardwareType.COMPUTER.value]
        user_agent_rotator = UserAgent(hardware_types=hardware_types, limit=100)
        self.user_agent = user_agent_rotator.get_random_user_agent()

    def _init_context(self):
        self.context = {"most_common": None, "results": None}

    def _switch_to_next_page(self):
        self._start += 100

    def _update_context(self):
        self.context["most_common"] = self._most_common
        self.context["results"] = self._results

    def _update_most_common(self, n):
        text = self.text_data.translate({ord(c): None for c in '"!@#$%^&*()_+.,?\n'})
        splitted = text.lower().split()
        filtered = filter(lambda x: len(x) > 3, splitted)
        counter = Counter(filtered)
        self.most_common = counter.most_common(n)

    def _update_results(self, rows):
        for idx, res in enumerate(rows):
            position = self._start + idx + 1
            link = res.find("div", {"class": "yuRUbf"}).a["href"]
            self._results.append({"position": position, "link": link})

    def _update_text_data(self, text_data):
        self._text_data += text_data

    def process(self):
        while True:
            time.sleep(1)
            response = self._get_response()

            if response.status_code == 200:
                data = self._get_data_from_html(response.content)
                rows = data.get("rows")
                text_data = data.get("text_data")

                if rows:
                    self._update_results(rows)
                    self._update_text_data(text_data)
                    self._switch_to_next_page()

                else:
                    break

            else:
                break

        self._update_most_common()
        self._update_context()
        return self.context
