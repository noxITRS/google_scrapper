from django.conf import settings
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.urls import path
from django.views.decorators.cache import cache_page
from .views import HomePageView, SearchResultsView


CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)

urlpatterns = [
    path(
        "search/",
        cache_page(CACHE_TTL)(SearchResultsView.as_view()),
        name="search_results",
    ),
    path("", HomePageView.as_view(), name="search_view"),
]
