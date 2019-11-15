# 
# core/views.py
#
# Author: Mihai Ionut Deaconu
#

import logging
from core.models import Disease, Study, Sample, CountData, SVMModel, RFModel, Gene
from django.shortcuts import render, render_to_response
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.http import HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.db.models import Q
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from . import machine_learning

def index(request):
    return render(request, 'index.html', context={})

def libraries(request):
    number_of_diseases = Disease.objects.all().count()
    number_of_studies = Study.objects.all().count()
    context = {
        'number_of_diseases': number_of_diseases,
        'number_of_studies': number_of_studies,
    }
    return render(request, 'libraries.html', context=context)

def models(request):
    return render(request, 'models.html', context={})

class DiseaseListView(generic.ListView):
    model = Disease
    context_object_name = 'disease_list'
    template_name = 'disease_templates/disease_list.html'
    paginate_by = 10

class StudyListView(generic.ListView):
    model = Study
    context_object_name = 'study_list'
    template_name = 'study_templates/study_list.html'
    paginate_by = 10

class SampleListView(generic.ListView):
    model = Sample
    template_name = 'sample_templates/sample_list.html'
    paginate_by = 10
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        samples = []
        # Display the samples in the current study only
        study = Study.objects.get(title=self.kwargs['title'])
        count_data = CountData.objects.get(name=self.kwargs['name'])
        for sample in count_data.sample_set.all():
            samples.append(sample)
        # Paginate according to the samples in the current study
        p = Paginator(samples, self.paginate_by)
        context['sample_list'] = p.page(context['page_obj'].number)
        context['title'] = study.title
        context['name'] = count_data.name
        return context

class SVMModelListView(generic.ListView):
    model = SVMModel
    context_object_name = 'svm_model_list'
    template_name = 'svm_model_templates/svm_model_list.html'
    paginate_by = 10

class RFModelListView(generic.ListView):
    model = RFModel
    context_object_name = 'rf_model_list'
    template_name = 'rf_model_templates/rf_model_list.html'
    paginate_by = 10

class DiseaseDetailView(generic.DetailView):
    model = Disease
    template_name = 'disease_templates/disease_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        studies = []
        # Add the studies that include the disease to the context
        # This will be displayed on the disease detail page
        for sample in self.object.sample_set.all():
            if sample.count_data.study not in studies:
                studies.append(sample.count_data.study)
        context['study_list'] = studies
        return context
    slug_field = 'abbreviation'
    slug_url_kwarg = 'abbreviation'

class StudyDetailView(generic.DetailView):
    model = Study
    template_name = 'study_templates/study_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        diseases = []
        # Add the diseases that the study covers to the context
        # This will be displayed on the disease detail page
        for count_data in self.object.countdata_set.all():
            samples = count_data.sample_set.all()
            for sample in samples:
                if sample.diagnosis not in diseases:
                    diseases.append(sample.diagnosis)
        context['disease_list'] = diseases
        context['count_data_list'] = CountData.objects.all()
        return context
    slug_field = 'title'
    slug_url_kwarg = 'title'

class SampleDetailView(generic.DetailView):
    model = Sample
    template_name = 'sample_templates/sample_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Add the study it belongs to to the context data
        # This will be displayed on the disease detail page
        context['study_list'] = Study.objects.all()
        return context
    slug_field = 'sample_ID'
    slug_url_kwarg = 'sample_ID'

class CountDataDetailView(generic.DetailView):
    model = CountData
    template_name = 'countdata_templates/countdata_detail.html'
    slug_field = 'name'
    slug_url_kwarg = 'name'

class SVMModelDetailView(generic.DetailView):
    model = SVMModel
    template_name = 'svm_model_templates/svm_model_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        diseases = []
        # Add the diseases that the model is based on to the context
        # This will be displayed on the disease detail page
        count_data = self.object.count_data
        study = count_data.study
        for count_data in study.countdata_set.all():
            samples = count_data.sample_set.all()
            for sample in samples:
                if sample.diagnosis not in diseases:
                    diseases.append(sample.diagnosis)
        context['diseases'] = diseases
        return context
    slug_field = 'model_name'
    slug_url_kwarg = 'model_name'

class RFModelDetailView(generic.DetailView):
    model = RFModel
    template_name = 'rf_model_templates/rf_model_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        diseases = []
        # Add the diseases that the model is based on to the context data
        # This will be displayed on the disease detail page
        count_data = self.object.count_data
        study = count_data.study
        for count_data in study.countdata_set.all():
            samples = count_data.sample_set.all()
            for sample in samples:
                if sample.diagnosis not in diseases:
                    diseases.append(sample.diagnosis)
        context['diseases'] = diseases
        return context
    slug_field = 'model_name'
    slug_url_kwarg = 'model_name'

class DiseaseCreateView(CreateView):
    model = Disease
    template_name = 'disease_templates/disease_form.html'
    fields = ['name', 'abbreviation', 'description', 'url']

class StudyCreateView(CreateView):
    model = Study
    template_name = 'study_templates/study_form.html'
    fields = ['DOI', 'title', 'url', 'publication_date', 'journal']

class CountDataCreateView(CreateView):
    model = CountData
    template_name = 'countdata_templates/countdata_form.html'
    fields = ['name', 'study', 'gene_count']
    def get_initial(self):
        super(CreateView, self).get_initial()
        # Automatically set the study of a new Count Data object to be the study
        # this was created from
        self.initial = { 'study' : Study.objects.get(title=self.kwargs['title']) }
        return self.initial

def import_sample(request, title, name):
    context = { "title" : title, "name" : name }
    if request.method == 'GET':
        return render(request, "sample_templates/import_sample.html", context)
    try:
        csv_file = request.FILES["csv_file"]
        # Check if the file has the right extension
        if not csv_file.name.endswith('.csv'):
            messages.error(request,'File is not CSV type')
            return HttpResponseRedirect(reverse("import_sample"))
        # Check the size of the file
        if csv_file.multiple_chunks():
            messages.error(request,"Uploaded file is too big (%.2f MB)." % (csv_file.size / (1000 * 1000),))
            return HttpResponseRedirect(reverse("import_sample"))

        file_data = csv_file.read().decode("utf-8")
        lines = file_data.split("\n")
        
        for line in lines:
            row = line.split(",")
            # Set control subject to diagnosis None, otherwise give them the proper diagnosis
            if str(row[4]) == "Control":
                new_sample = Sample.objects.create(
                    count_data = CountData.objects.get(study=Study.objects.get(title=title)),
                    sample_ID = str(row[0]),
                    sample_source = str(row[1]),
                    brain_region = str(row[2]),
                    RIN = str(row[3]),
                    diagnosis = None,
                    sex = str(row[5]),
                    age_at_death = int(row[6]),
                    ApoE = str(row[7]),
                    PMI = str(row[8]))
            else:
                new_sample = Sample.objects.create(
                    count_data = CountData.objects.get(study=Study.objects.get(title=title)),
                    sample_ID = str(row[0]),
                    sample_source = str(row[1]),
                    brain_region = str(row[2]),
                    RIN = str(row[3]),
                    diagnosis = Disease.objects.get(abbreviation=row[4]),
                    sex = str(row[5]),
                    age_at_death = int(row[6]),
                    ApoE = str(row[7]),
                    PMI = str(row[8]))                 
    except Exception as e:
        logging.getLogger("error_logger").error("Unable to upload file.")
        messages.error(request, "Unable to upload file.")

    return HttpResponseRedirect(reverse("samples", kwargs={"title" : title, "name" : name }))

class DiseaseUpdate(UpdateView):
    model = Disease
    template_name = 'disease_templates/disease_update_form.html'
    fields = ['name', 'abbreviation', 'description', 'url']
    template_name_suffix = '_update_form'
    slug_field = 'abbreviation'
    slug_url_kwarg = 'abbreviation'

class StudyUpdate(UpdateView):
    model = Study
    template_name = 'study_templates/study_update_form.html'
    fields = ['DOI', 'title', 'url', 'publication_date']
    template_name_suffix = '_update_form'
    slug_field = 'title'
    slug_url_kwarg = 'title'

class CountDataUpdate(UpdateView):
    model = CountData
    template_name = 'countdata_templates/countdata_update_form.html'
    fields = ['name', 'gene_count']
    template_name_suffix = '_update_form'
    slug_field = 'name'
    slug_url_kwarg = 'name'

class DiseaseDelete(DeleteView):
    model = Disease
    template_name = 'disease_templates/disease_confirm_delete.html'
    success_url = reverse_lazy('diseases')
    slug_field = 'abbreviation'
    slug_url_kwarg = 'abbreviation'

class StudyDelete(DeleteView):
    model = Study
    template_name = 'study_templates/study_confirm_delete.html'
    success_url = reverse_lazy('studies')
    slug_field = 'title'
    slug_url_kwarg = 'title'

class CountDataDelete(DeleteView):
    model = CountData
    template_name = 'countdata_templates/countdata_confirm_delete.html'
    success_url = reverse_lazy('studies')
    slug_field = 'name'
    slug_url_kwarg = 'name'

def search_disease(request):
    diseases = Disease.objects.all()
    query = request.GET.get("q")
    if query:
        diseases = diseases.filter(
        Q(name__icontains=query) |
        Q(abbreviation__icontains=query)
        ).distinct()
    return render(request, 'search_templates/search_disease.html', {'diseases' : diseases})

def search_study(request):
    studies = Study.objects.all()
    query = request.GET.get("q")
    if query:
        studies = studies.filter(
        Q(title__icontains=query) |
        Q(DOI__icontains=query)
        ).distinct()
    return render(request, 'search_templates/search_study.html', {'studies' : studies})

def search_sample(request):
    samples = Sample.objects.all()
    query = request.GET.get("q")
    if query:
        samples = samples.filter(
        Q(sample_ID__icontains=query) |
        Q(sample_source__icontains=query) |
        Q(brain_region__icontains=query)
        ).distinct()
    return render(request, 'search_templates/search_sample.html', {'samples' : samples})

def genesearch(gene, ensembl, first, last):
    if last < first:
        return None
    else:
        middle = first + (last - first) // 2
        if gene > ensembl[middle].gene_id:
            return genesearch(gene, ensembl, middle + 1, last)
        else:
            if gene < ensembl[middle].gene_id:
                return genesearch(gene, ensembl, first, middle - 1)
            else: 
                return ensembl[middle]

def svm_genes(request, model_name):
    model = SVMModel.objects.get(model_name=model_name)
    selected_genes = machine_learning.select_genes_svm(model.model_file, model.count_data.gene_count)
    ensembl_genes = Gene.objects.all()
    my_genes = []

    # For each selected gene, associate it with the corresponding Ensembl entry database entry
    # in the order of importance
    for selected_gene in selected_genes:
        my_genes.append(genesearch(selected_gene, ensembl_genes, 0, len(ensembl_genes) - 1))
    
    # Paginate the selected genes (5 per page)
    paginator = Paginator(my_genes, 5)
    page = request.GET.get('page')
    try:
        genes = paginator.page(page)
    except PageNotAnInteger:
        genes = paginator.page(1)
    except EmptyPage:
        genes = paginator.page(paginator.num_pages)

    context = {
        'genes': genes,
    }
    return render(request, 'gene_templates/gene_list.html', context=context)

def rf_genes(request, model_name):
    model = RFModel.objects.get(model_name=model_name)
    selected_genes = machine_learning.select_genes_rf(model.model_file, model.count_data.gene_count)
    ensembl_genes = Gene.objects.all()
    my_genes = []

    # For each selected gene, associate it with the corresponding Ensembl entry database entry
    # in the order of importance
    for selected_gene in selected_genes:
        my_genes.append(genesearch(selected_gene, ensembl_genes, 0, len(ensembl_genes) - 1))
    
    # Paginate the selected genes (5 per page)
    paginator = Paginator(my_genes, 5)
    page = request.GET.get('page')
    try:
        genes = paginator.page(page)
    except PageNotAnInteger:
        genes = paginator.page(1)
    except EmptyPage:
        genes = paginator.page(paginator.num_pages)

    context = {
        'genes': genes,
    }
    return render(request, 'gene_templates/gene_list.html', context=context)

# Page not fount error
def handler404(request, template_name="error_templates/404.html"):
    response = render_to_response("error_templates/404.html")
    response.status_code = 404
    return response
    
# Internal server error
def handler500(request, template_name="error_templates/500.html"):
    response = render_to_response("error_templates/500.html")
    response.status_code = 500
    return response