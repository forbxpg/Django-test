from django.shortcuts import render, get_object_or_404

from core.utils import AdConditionChoices
from .filters import AdFilter
from .models import Ad, Category
from .services import get_excluded_ad_ids


def ads_list_view(request, category_slug=None):
    """Отображает список объявлений."""
    excluded_ids = get_excluded_ad_ids()
    ads = Ad.objects.exclude(id__in=excluded_ids)
    filter = AdFilter(request.GET, queryset=ads)
    return render(
        request,
        "ads/list.html",
        {
            "filter": filter,
            "categories": Category.objects.all(),
            "ads": filter.qs,
        },
    )


def ad_detail_view(request, ad_id):
    """Отображает детальную информацию об объявлении."""
    ad = get_object_or_404(Ad, id=ad_id)
    return render(
        request,
        "ads/detail.html",
        {
            "ad": ad,
        },
    )
