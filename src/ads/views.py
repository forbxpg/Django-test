"""Модуль представлений для работы с объявлениями."""

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render, get_object_or_404, redirect, reverse

from core import config
from .filters import AdFilter
from .forms import AdForm
from .models import Ad, Category
from .services import get_excluded_ad_ids


def ads_list_view(request):
    """Отображает список объявлений."""
    excluded_ids = get_excluded_ad_ids()
    ads = Ad.objects.select_related(
        "user",
        "category",
    ).exclude(
        id__in=excluded_ids,
    )
    ad_filter = AdFilter(request.GET, queryset=ads)
    paginator = Paginator(ad_filter.qs, config.ADS_PER_PAGE)
    page_num = request.GET.get("page")
    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        page_obj = paginator.page(config.FIRST_PAGE)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    return render(
        request,
        "ads/list.html",
        {
            "filter": ad_filter,
            "categories": Category.objects.all(),
            "page_obj": page_obj,
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


@login_required
def ad_create_view(request):
    """Создает новое объявление."""
    if request.method == "POST":
        form = AdForm(request.POST, request.FILES)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            return redirect(
                reverse("ads:ad-detail", kwargs={"ad_id": ad.id}),
            )
    else:
        form = AdForm()

    return render(
        request,
        "ads/form.html",
        {"form": form},
    )


@login_required
def ad_update_view(request, ad_id):
    """Редактирует существующее объявление."""
    ad = get_object_or_404(Ad, id=ad_id)
    if ad.user != request.user:
        raise PermissionDenied(
            _("У вас нет прав на редактирование этого объявления."),
        )
    if request.method == "POST":
        form = AdForm(request.POST, request.FILES, instance=ad)
        if form.is_valid():
            form.save()
            return redirect("ads:ad-detail", ad_id=ad.id)
    else:
        form = AdForm(instance=ad)
    return render(
        request,
        "ads/form.html",
        {"form": form, "ad": ad},
    )


@login_required
def ad_delete_view(request, ad_id):
    """Удаляет существующее объявление."""
    ad = get_object_or_404(Ad, id=ad_id)
    if ad.user != request.user:
        raise PermissionDenied(
            _("У вас нет прав на удаление этого объявления."),
        )
    if request.method == "POST":
        ad.delete()
        return redirect(reverse("ads:ads-list"))
    return render(
        request,
        "ads/detail.html",
        {"ad": ad},
    )
