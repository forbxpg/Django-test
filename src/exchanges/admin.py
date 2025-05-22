from django.contrib import admin

from unfold.admin import ModelAdmin

from .models import ExchangeProposal


@admin.register(ExchangeProposal)
class ExchangeProposalAdmin(ModelAdmin): ...
