from rest_framework.pagination import PageNumberPagination


class ProjectResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'


class ContactMeResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'


class ResumeProjectPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'


class ResumeAwardsAndAchievementsPagination(PageNumberPagination):
    page_size = 3
    page_size_query_param = 'page_size'