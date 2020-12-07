from django.test import TestCase
from django.urls import reverse


class ScrapperTestCase(TestCase):
    def test_home_page_contains_form(self):
        home_page_url = reverse("home_page")
        response = self.client.get(home_page_url)
        self.assertContains(
            response, '<form action="/search/" method="get">', status_code=200
        )

    def test_scrapper_with_wrong_param(self):
        search_results_url = reverse("search_results")
        response = self.client.get(search_results_url, {"pkk": "wrong param"})
        message = "I'm sorry, you passed wrong parameter. There's no results"
        self.assertContains(response, message, status_code=200)
