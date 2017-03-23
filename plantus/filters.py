from rest_framework.filters import BaseFilterBackend


class DateFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        if start_date and end_date:
            return queryset.filter(date__lte=end_date, date__gte=start_date)
        else:
            return queryset


class CompletedFilter(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        completed = request.query_params.get('completed', None)

        if completed is None:
            return queryset

        try:
            completed = bool(int(completed))
            return queryset.filter(completed_at__isnull=not completed)
        except ValueError:
            return queryset
