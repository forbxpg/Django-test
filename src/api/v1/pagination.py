"""Модуль для пагинации запросов к API."""

from rest_framework.pagination import PageNumberPagination as Pagination

from core import config


class PageNumberPagination(Pagination):
    """Пагинация с использованием номера страницы."""

    page_size = config.PAGE_SIZE
    max_page_size = config.MAX_PAGE_SIZE
