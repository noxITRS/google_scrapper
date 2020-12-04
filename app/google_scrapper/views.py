from google_scrapper.models import SearchInfo, SearchRecord
from google_scrapper.scrapper import Scrapper
from django.views.generic import TemplateView


class HomePageView(TemplateView):
    template_name = "index.html"


class SearchResultsView(TemplateView):
    template_name = "search_results.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        user_ip = self.get_client_ip()
        context["user_ip"] = user_ip

        phrase = self.request.GET.get("q")
        if phrase:
            scrapper = Scrapper(phrase=phrase)
            scrapper_results = scrapper.get_data()

            context["most_common"] = scrapper_results["most_common"]
            context["results"] = scrapper_results["results"]

            search_info = SearchInfo(user_ip=user_ip, phrase=phrase)
            search_info.save()

            record_objs = [
                SearchRecord(
                    position=obj["position"], link=obj["link"], search_info=search_info
                )
                for obj in scrapper_results["results"]
            ]

            SearchRecord.objects.bulk_create(record_objs)
        return context

    def get_client_ip(self):
        x_forwarded_for = self.request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = self.request.META.get("REMOTE_ADDR")
        return ip
