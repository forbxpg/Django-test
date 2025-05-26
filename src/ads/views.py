"""Модуль представлений для работы с объявлениями."""

from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http.response import Http404
from django.utils.translation import gettext_lazy as _
from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.views.decorators.http import require_POST

from core import config
from .filters import AdFilter
from .forms import AdForm
from .models import Ad, Category
from .services import (
    get_not_exchanged_ads_queryset,
    check_is_ad_related_to_sender_or_receiver,
)


def ads_list_view(request):
    """Отображает список объявлений на главной странице,
    которые не были обменены.
    """
    ads = get_not_exchanged_ads_queryset()
    ad_filter = AdFilter(request.GET, queryset=ads)
    paginator = Paginator(ad_filter.qs, config.ADS_PER_PAGE)
    page_num = request.GET.get("page")
    try:
        page_obj = paginator.page(page_num)
    except (PageNotAnInteger, EmptyPage):
        page_obj = paginator.page(1)
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
    """Отображает детальную информацию об объявлении.
    Разрешает просмотр обмененного объявления владельцу
    объявления или пользователю, который инициировал обмен.
    """
    ad = get_object_or_404(
        Ad.objects.select_related(
            "user",
            "category",
        ),
        id=ad_id,
    )
    if ad.is_exchanged and ad.user != request.user:
        if not check_is_ad_related_to_sender_or_receiver(ad, request.user):
            raise Http404(_("Объявление не найдено или уже обменено."))
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
    """Редактирует существующее объявление.
    Если оно не было обменено.
    """
    ads = get_not_exchanged_ads_queryset()
    ad = get_object_or_404(ads, id=ad_id)
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
@require_POST
def ad_delete_view(request, ad_id):
    """Удаляет существующее объявление.
    Если оно не было обменено.
    """
    ads = get_not_exchanged_ads_queryset()
    ad = get_object_or_404(ads, id=ad_id)
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


def category_list_view(request):
    """Отображает список всех категорий объявлений.
    Можно перенести в context_processor.
    """
    return render(
        request,
        "category/list.html",
        {
            "categories": Category.objects.all(),
        },
    )
