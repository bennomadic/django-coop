# -*- coding:utf-8 -*-
from django.contrib import admin
from coop_local.models import Membre,Role,Engagement,Initiative
from skosxl.models import Term
from django_extensions.admin import ForeignKeyAutocompleteAdmin
from django_extensions.admin.widgets import ForeignKeySearchInput
from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple


admin.site.register(Role)


class EngagementInline(admin.TabularInline):
    model = Engagement
    extra=1


class InitiativeAdminForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Term.objects.all().order_by('literal'),
        widget=FilteredSelectMultiple('tags', False)
    )
    class Meta:
        model = Initiative


class InitiativeAdmin(admin.ModelAdmin):
    form = InitiativeAdminForm
    list_display = ('title','uri')
    list_display_links =('title',)
    list_filter = ('active',)
    ordering = ('title',)
    inlines = [
            EngagementInline,
        ]
    
admin.site.register(Initiative, InitiativeAdmin)

class MembreAdmin(admin.ModelAdmin):
    list_display = ('nom','prenom','email',)
    list_display_links =('nom','prenom')
    ordering = ('nom',)
    inlines = [
            EngagementInline,
        ]
 
admin.site.register(Membre, MembreAdmin)


