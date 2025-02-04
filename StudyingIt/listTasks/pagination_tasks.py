from rest_framework.pagination import BasePagination

from urllib.parse import urlparse, urlunparse


class PaginTasks(BasePagination):
    def get_next_link(self):
        if not self.has_next():
            return None

        url = self.request.build_absolute_uri()
        parsed_url = urlparse(url)
        new_netloc = 'studyingit-api.ru'
        new_url = parsed_url._replace(netloc=new_netloc)
        return urlunparse(new_url)

    def get_previous_link(self):
        if not self.has_previous():
            return None

        url = self.request.build_absolute_uri()
        parsed_url = urlparse(url)
        new_netloc = 'studyingit-api.ru'
        new_url = parsed_url._replace(netloc=new_netloc)
        return urlunparse(new_url)
