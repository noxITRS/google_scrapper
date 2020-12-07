from django.db import models


class SearchInfo(models.Model):
    user_ip = models.CharField(max_length=45)
    phrase = models.CharField(max_length=255)


class SearchRecord(models.Model):
    position = models.IntegerField()
    link = models.URLField(max_length=500)
    search_info = models.ForeignKey(
        SearchInfo, related_name="records", on_delete=models.CASCADE
    )
