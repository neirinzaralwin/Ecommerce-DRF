from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


DEFAULT_PAGE = 1
DEFAULT_PAGE_SIZE = 10


class CustomPagination(PageNumberPagination):
    page = DEFAULT_PAGE
    page_size = DEFAULT_PAGE_SIZE
    page_size_query_param = "limit"

    def calculateHasMorePages(self, total=0):
        result = total % DEFAULT_PAGE_SIZE
        if result > DEFAULT_PAGE_SIZE:
            return True
        else:
            return False

    def get_paginated_response(self, data):
        return Response(
            {
                "total": self.page.paginator.count,
                "page": int(self.request.GET.get("page", DEFAULT_PAGE)),
                "has_more_pages": self.calculateHasMorePages(
                    total=self.page.paginator.count
                ),
                "limit": int(self.request.GET.get("limit", self.page_size)),
                "data": data,
            }
        )


class PaginationHandlerMixin(object):
    @property
    def paginator(self):
        if not hasattr(self, "_paginator"):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        else:
            pass
        return self._paginator

    def paginate_queryset(self, queryset):
        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset, self.request, view=self)

    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)

    def custom_paginated_response(self, serializer_class, queryset):
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_paginated_response(
                serializer_class(page, many=True).data
            )
            return Response(serializer.data)
        else:
            serializer = serializer_class(instance, many=True)
            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )
