"""Модуль представлений для обменов."""

from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import models
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.urls.base import reverse
from django.utils.translation import gettext_lazy as _

from ads.models import Ad
from ads.services import get_not_exchanged_ads_queryset
from core import config, utils
from .forms import ExchangeForm, ExchangeStatusForm
from .models import ExchangeProposal


@login_required
def exchange_create_view(request, ad_id=None):
    """Cоздает предложение обмена для объявления."""
    ads = get_not_exchanged_ads_queryset()
    user_ads = request.user.ads.all()
    other_ads = ads.exclude(user=request.user)
    if request.method == "POST":
        form = ExchangeForm(request.POST)
        form.fields["ad_sender"].queryset = user_ads
        form.fields["ad_receiver"].queryset = other_ads
        if form.is_valid():
            proposal = form.save()
            return redirect(reverse("exchanges:exchanges-list"))
    else:
        initial = {}
        if ad_id:
            initial["ad_receiver"] = get_object_or_404(ads, id=ad_id)
        form = ExchangeForm(initial=initial)
        form.fields["ad_sender"].queryset = user_ads
        form.fields["ad_receiver"].queryset = other_ads
    return render(
        request,
        "exchanges/create.html",
        {"form": form},
    )


@login_required
def exchange_list_view(request):
    """Отображает список предложений обмена."""
    qs = ExchangeProposal.objects.select_related(
        "ad_sender__user",
        "ad_receiver__user",
    ).filter(
        models.Q(ad_sender__user=request.user)
        | models.Q(ad_receiver__user=request.user)
    )
    sender = request.GET.get("sender")
    receiver = request.GET.get("receiver")
    status = request.GET.get("status")
    if sender:
        qs = qs.filter(ad_sender__id=sender)
    if receiver:
        qs = qs.filter(ad_receiver__id=receiver)
    if status:
        qs = qs.filter(status=status)
    paginator = Paginator(qs, config.EXCHANGES_PER_PAGE)
    page = request.GET.get("page")
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
    context = {
        "page_obj": page_obj,
        "user_ads": request.user.ads.all(),
        "status_choices": utils.ExchangeStatusChoices.choices,
    }
    return render(
        request,
        "exchanges/list.html",
        context,
    )


@login_required
def exchange_detail_view(request, proposal_id):
    """Отображает детальную информацию о предложении обмена."""
    proposal = get_object_or_404(
        ExchangeProposal.objects.select_related(
            "ad_sender__user",
            "ad_receiver__user",
        ),
        id=proposal_id,
    )
    if (
        proposal.ad_sender.user != request.user
        and proposal.ad_receiver.user != request.user
    ):
        raise PermissionDenied(
            _("У вас нет прав на просмотр этого предложения обмена.")
        )
    if request.method == "POST":
        form = ExchangeStatusForm(request.POST, instance=proposal)
        if form.is_valid():
            form.save()
            return redirect(
                reverse(
                    "exchanges:exchange-detail",
                    kwargs={
                        "proposal_id": proposal.id,
                    },
                )
            )
    else:
        form = ExchangeStatusForm(instance=proposal)
    return render(
        request,
        "exchanges/detail.html",
        {
            "proposal": proposal,
            "form": form,
        },
    )
