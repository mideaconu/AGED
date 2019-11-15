# 
# core/urls.py
#
# Author: Mihai Ionut Deaconu
#

from django.conf.urls import include
from django.contrib.auth.decorators import login_required
from django.urls import path
from . import views

urlpatterns = [

    path('', login_required(views.index), name='index'),
    path('libraries/', login_required(views.libraries), name='libraries'),
    path('models/', login_required(views.models), name='models'),

    path('models/svm/', login_required(views.SVMModelListView.as_view()), name='svm_models'),
    path('models/svm/<model_name>', login_required(views.SVMModelDetailView.as_view()), name='svm_model_detail'),
    path('models/svm/<model_name>/genes', login_required(views.svm_genes), name='svm_genes'),
    
    path('models/rf/', login_required(views.RFModelListView.as_view()), name='rf_models'),
    path('models/rf/<model_name>', login_required(views.RFModelDetailView.as_view()), name='rf_model_detail'),
    path('models/rf/<model_name>/genes', login_required(views.rf_genes), name='rf_genes'),
    
    path('search/diseases', login_required(views.search_disease), name='search_disease'),
    path('search/studies', login_required(views.search_study), name='search_study'),
    path('search/samples', login_required(views.search_sample), name='search_sample'), 

    path('diseases/', login_required(views.DiseaseListView.as_view()), name='diseases'),
    path('diseases/create', login_required(views.DiseaseCreateView.as_view()), name='create_disease'),
    path('diseases/<abbreviation>', login_required(views.DiseaseDetailView.as_view()), name='disease_detail'),
    path('diseases/<abbreviation>/update', login_required(views.DiseaseUpdate.as_view()), name='disease_update'),
    path('diseases/<abbreviation>/confirm_delete', login_required(views.DiseaseDelete.as_view()), name='disease_delete'), 
    
    path('studies/', login_required(views.StudyListView.as_view()), name='studies'),
    path('studies/create', login_required(views.StudyCreateView.as_view()), name='create_study'),
    path('studies/<title>', login_required(views.StudyDetailView.as_view()), name='study_detail'),
    path('studies/<title>/update', login_required(views.StudyUpdate.as_view()), name='study_update'),
    path('studies/<title>/confirm_delete', login_required(views.StudyDelete.as_view()), name='study_delete'),

    path('studies/<title>/count_data/create', login_required(views.CountDataCreateView.as_view()), name='count_data_create'),
    path('studies/<title>/count_data/<name>', login_required(views.CountDataDetailView.as_view()), name='count_data_detail'),
    path('studies/<title>/count_data/<name>/update', login_required(views.CountDataUpdate.as_view()), name='count_data_update'),
    path('studies/<title>/count_data/<name>/confirm_delete', login_required(views.CountDataDelete.as_view()), name='count_data_delete'),  

    path('studies/<title>/count_data/<name>/samples', login_required(views.SampleListView.as_view()), name='samples'),
    path('studies/<title>/count_data/<name>/samples/import', login_required(views.import_sample), name='import_sample'),
    path('studies/<title>/count_data/<name>/samples/<sample_ID>', login_required(views.SampleDetailView.as_view()), name='sample_detail'),
]