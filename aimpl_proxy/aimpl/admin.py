# -*- coding: utf-8 -

from django import forms
from django.contrib import admin
from django.shortcuts import render_to_response as render
from django.template import RequestContext, loader, Context
from django.utils.translation import ugettext_lazy, ugettext as _

from aimpl_proxy.aimpl.models import ProblemList, Section, Block, Remark

def create_revision(modeladmin, request, queryset):
    opts = modeladmin.model._meta
    app_label = opts.app_label
    
    context = {
        "title": _("Create revisions?"),
        "opts": opts,
        "app_label": app_label,
    }
    
    return render("proxy/admin/make_revision.html", context, 
        context_instance=RequestContext(request))
create_revision.short_description = "Create revision of selected problem lists"    

class ProblemLisAdmin(admin.ModelAdmin):
    actions = [create_revision]

 
admin.site.register(ProblemList)
admin.site.register(Section)
admin.site.register(Block)
admin.site.register(Remark)