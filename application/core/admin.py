# 
# core/admin.py
#
# Author: Mihai Ionut Deaconu
#

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.contrib import admin
from .models import Disease, Study, CountData, Sample, SVMModel, RFModel, Gene
from import_export import resources
from import_export.admin import ImportExportModelAdmin
from import_export.fields import Field
from import_export.forms import ImportForm
from django import forms
from django.template.response import TemplateResponse
from django.utils.translation import gettext as _
from import_export.formats.base_formats import DEFAULT_FORMATS

class DiseaseAdmin(admin.ModelAdmin):
  list_display = ('name', 'abbreviation')
  search_fields = ('name', 'abbreviation')

class StudyAdmin(admin.ModelAdmin):
  list_display = ('title', 'DOI', 'publication_date')
  search_fields = ('title', 'DOI')
  date_hierarchy = 'publication_date'
  ordering = ('-publication_date',)

class SVMModelAdmin(admin.ModelAdmin):
  list_display = ('model_name', 'count_data')
  search_fields = ('model_name', 'diseases', 'kernel')
  ordering = ('-kernel',)

class RFModelAdmin(admin.ModelAdmin):
  list_display = ('model_name', 'count_data')
  search_fields = ('model_name', 'diseases', 'criterion')
  ordering = ('-criterion',)

class CountDataAdmin(admin.ModelAdmin):
  list_display = ('name',)

class SampleResource(resources.ModelResource):
  class Meta:
    model = Sample
    import_id_fields = ('sampleID',)
    exclude = ('id', )
    skip_unchanged = True
    report_skipped = False
    verbose_name = True

class SampleAdmin(ImportExportModelAdmin):
  resource_class = SampleResource
  def import_action(self, request, *args, **kwargs):
    super().import_action(request, *args, **kwargs)
    form = SampleImportForm(self, Study, DEFAULT_FORMATS, request.POST or None, request.FILES or None)

class GeneResource(resources.ModelResource):
  class Meta:
    model = Gene
    exclude = ('id',)
    import_id_fields = ('gene_id', 'gene_description', 'gene_name', 'gene_type',)

class GeneAdmin(ImportExportModelAdmin):
  resource_class = GeneResource
  pass

admin.site.register(Disease, DiseaseAdmin)
admin.site.register(Study, StudyAdmin)
admin.site.register(Sample, SampleAdmin)
admin.site.register(CountData, CountDataAdmin)
admin.site.register(SVMModel, SVMModelAdmin)
admin.site.register(RFModel, RFModelAdmin)
admin.site.register(Gene, GeneAdmin)