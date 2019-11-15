# 
# core/models.py
#
# Author: Mihai Ionut Deaconu
#

# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, FileExtensionValidator, RegexValidator
from django.urls import reverse

class Disease(models.Model):
  name = models.CharField(max_length=50, unique=True)
  abbreviation = models.CharField(max_length=6, unique=True)
  description = models.TextField()
  url = models.URLField(verbose_name = 'URL', blank=True)

  class Meta:
    verbose_name = 'Disease'
    verbose_name_plural = 'Diseases'
    ordering = ['name']
  def __str__(self):
    return "%s (%s)" % (self.name, self.abbreviation)
  def get_absolute_url(self):
    return reverse('disease_detail', args=[str(self.abbreviation)])

class Study(models.Model):
  DOI = models.CharField(max_length=50, unique=True,
                          validators=[RegexValidator(r'^doi:[0-9]{2}.[0-9]{4}\/[a-zA-Z0-9.]{0,40}$')], 
                          help_text='Please use format "doi:prefix/suffix"')
  title = models.CharField(max_length=200)
  url = models.URLField(verbose_name = 'URL', blank=True, null=True)
  publication_date = models.DateField(blank=True, null=True)
  journal = models.CharField(max_length=200, blank=True, null=True)

  class Meta:
    verbose_name = 'Study'
    verbose_name_plural = 'Studies'
    ordering = ['-publication_date']
  def __str__(self):
    return "%s %s" % (self.title, self.DOI)
  def get_absolute_url(self):
    return reverse('study_detail', args=[str(self.title)])

class CountData(models.Model):
  def directory_path(instance, filename):
    return 'count_data/{0}/{1}.csv'.format(instance.study.pk, instance.name)

  name = models.CharField(max_length=50, unique=True)
  study = models.ForeignKey(Study, to_field='DOI', on_delete=models.CASCADE)
  gene_count = models.FileField(upload_to=directory_path, validators=[FileExtensionValidator(allowed_extensions=['csv', 'tsv'])])
  class Meta:
    verbose_name = 'Count Data'
    verbose_name_plural = 'Count Data'
  def __str__(self):
    return self.name
  def get_absolute_url(self):
    return reverse('count_data_detail', args=[str(self.study.title), str(self.name)])

kernels = (
  ("RBF", "RBF"), 
  ("Linear", "Linear"), 
  ("Polynomial", "Poly"), 
  ("Sigmoid", "Sigmoid")
)

C_values = (
  ("1000", 1000), ("100", 100), ("10", 10), ("1", 1), ("0.1", 0.1), 
  ("0.01", 0.01), ("0.001", 0.001), ("1e-4", 1e-4), ("1e-5", 1e-5), 
  ("1e-6", 1e-6), ("1e-7", 1e-7), ("1e-8", 1e-8), ("1e-9", 1e-9), 
  ("1e-10", 1e-10)
)

gamma_values = (
  ("1000", 1000), ("100", 100), ("10", 10), ("1", 1), ("0.1", 0.1), 
  ("0.01", 0.01), ("0.001", 0.001), ("1e-4", 1e-4), ("1e-5", 1e-5), 
  ("1e-6", 1e-6), ("1e-7", 1e-7), ("1e-8", 1e-8), ("1e-9", 1e-9), ("1e-10", 1e-10)
)

def SVM_directory_path(instance, filename):
    return 'models/SVM/{0}/{1}.sav'.format(instance.count_data.study.id, instance.model_name)

class SVMModel(models.Model):
  model_name = models.CharField(max_length=50, unique=True)
  description = models.TextField()
  count_data = models.ForeignKey(CountData, to_field='name', on_delete=models.CASCADE)
  kernel = models.CharField(max_length=10, choices=kernels, verbose_name="Kernel")
  C = models.CharField(max_length=5, choices=C_values, blank=True)
  gamma = models.CharField(max_length=5, choices=gamma_values, blank=True)
  model_file = models.FileField(upload_to=SVM_directory_path, validators=[FileExtensionValidator(allowed_extensions=['sav'])])

  class Meta:
    verbose_name = 'Support Vector Machine model'
    verbose_name_plural = 'Support Vector Machine models'
  def __str__(self):
    return self.model_name
  def get_absolute_url(self):
    return reverse('svm_model_detail', args=[str(self.model_name)])

criteria = (
  ('Gini', 'Gini'), ('Entropy', 'Entropy')
  )

def RF_directory_path(instance, filename):
    return 'models/RF/{0}/{1}.sav'.format(instance.count_data.study.id, instance.model_name)

class RFModel(models.Model):
  model_name = models.CharField(max_length=50, unique=True)
  description = models.TextField()
  count_data = models.ForeignKey(CountData, to_field='name', on_delete=models.CASCADE)
  n_estimators = models.CharField(max_length=10, verbose_name="NumberOfEstimators", blank=True)
  max_depth = models.CharField(max_length=10, verbose_name="MaxDepth", blank=True)
  criterion = models.CharField(max_length=7, choices=criteria, verbose_name="Criterion")
  bootstrap = models.CharField(max_length=5, choices=(('True', 'True'), ('False', 'False')), verbose_name="Bootstrap")
  model_file = models.FileField(upload_to=RF_directory_path, validators=[FileExtensionValidator(allowed_extensions=['sav'])])

  class Meta:
    verbose_name = 'Random Forest model'
    verbose_name_plural = 'Random Forest models'
  def __str__(self): 
    return self.model_name
  def get_absolute_url(self):
    return reverse('rf_model_detail', args=[str(self.model_name)])

sexes = (
  ('M', 'Male'),
  ('F', 'Female')
)

class Sample(models.Model):
  count_data = models.ForeignKey(CountData, to_field='name', on_delete=models.CASCADE)
  sample_ID = models.CharField(max_length=20, verbose_name='SampleID', unique=True, primary_key=True)
  sample_source = models.CharField(max_length=50, verbose_name='Source')
  brain_region = models.CharField(max_length=50, verbose_name='Tissue')
  RIN = models.CharField(max_length=2, blank=True)
  diagnosis = models.ForeignKey(Disease, default=None, to_field='abbreviation', on_delete=models.CASCADE, verbose_name='Diagnosis', null=True, blank=True)
  sex = models.CharField(max_length=1, choices=sexes, verbose_name='Sex')
  age_at_death = models.CharField(max_length=3, null=True, verbose_name='AgeAtDeath')  
  ApoE = models.CharField(max_length=2, blank=True)
  PMI = models.CharField(max_length=2, blank=True)

  class Meta:
    verbose_name = 'Sample'
    verbose_name_plural = 'Samples'
    ordering = ['sample_ID']
  def __str__(self):
    return self.sample_ID
  def get_absolute_url(self):
    return reverse('sample_detail', args=[str(self.count_data.study.title), str(self.count_data.name), str(self.sample_ID)])

class Gene(models.Model):
  gene_id = models.CharField(max_length=16, verbose_name='Source')
  gene_description = models.CharField(max_length=200, verbose_name='Source', blank=True)
  gene_name = models.CharField(max_length=50, verbose_name='Source', blank=True)
  gene_type = models.CharField(max_length=50, verbose_name='Source', blank=True)

  class Meta:
    verbose_name = 'Gene'
    verbose_name_plural = 'Genes'
    ordering = ['gene_id']
  def __str__(self):
    return self.gene_id