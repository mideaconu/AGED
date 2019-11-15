# 
# core/test_views.py
#
# Author: Mihai Ionut Deaconu
#

import unittest
from unittest.mock import MagicMock
from core.models import Disease, Study, CountData, SVMModel, RFModel, Sample
from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.files import File

class DiseaseListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='username', password='password')
        number_of_diseases = 13
        for disease_id in range(number_of_diseases):
            Disease.objects.create(name=f"Test Disease {disease_id}", 
              abbreviation=f"TD{disease_id}", 
              description="Neurodegenerative disorder",
              url=f"https://www.diseasetest.co.uk")
           
    def test_disease_list_url(self):
        self.client.login(username='username', password='password')
        response = self.client.get('/diseases/')
        self.assertEqual(response.status_code, 200)

    def test_disease_pagination_is_ten(self):
        self.client.login(username='username', password='password')
        response = self.client.get(reverse('diseases'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['disease_list']) == 10)

    def test_number_of_disease_on_last_page(self):
        self.client.login(username='username', password='password')
        response = self.client.get(reverse('diseases') +'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['disease_list']) == 3)

class DiseaseDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='username', password='password')
        Disease.objects.create(name="Test Disease", 
            abbreviation="TD", 
            description="Neurodegenerative disorder",
            url=f"https://www.diseasetest.co.uk")
           
    def test_disease_detail_url(self):
        disease = Disease.objects.get(abbreviation="TD")
        self.client.login(username='username', password='password')
        response = self.client.get(reverse('disease_detail', 
            kwargs={"abbreviation": disease.abbreviation}))
        self.assertEqual(response.status_code, 200)

class DiseaseCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='username', password='password')

    def test_create_disease(self):
        self.client.login(username='username', password='password')
        response = self.client.post(
            reverse('create_disease'), 
            {'name': "Test Disease", 'abbreviation': "TD", 
            'description': "Neurodegenerative disorder", 
            'url': "https://www.diseasetest.co.uk"})
        disease = Disease.objects.get(abbreviation='TD')
        self.assertEqual(disease.abbreviation, 'TD')

class DiseaseUpdateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='username', password='password')
        Disease.objects.create(name="Test Disease", 
            abbreviation="TD", 
            description="Neurodegenerative disorder")

    def test_update_disease(self):
        disease = Disease.objects.get(abbreviation="TD")
        self.client.login(username='username', password='password')
        response = self.client.post(
            reverse('disease_update', kwargs={'abbreviation': disease.abbreviation}), 
            {'name': "Test Disease", 'abbreviation': "TD", 
            'description': "Neurodegenerative disorder", 
            'url': 'https://www.diseasetest.co.uk'})
        self.assertEqual(response.status_code, 302)
        disease.refresh_from_db()
        self.assertEqual(disease.url, 'https://www.diseasetest.co.uk')

#class StudyListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='username', password='password')
        number_of_studies = 13
        for study_id in range(number_of_studies):
            Study.objects.create(DOI=f"doi:10.0000/test{study_id}", 
                title=f"Test Study {study_id}", 
                url="https://www.studytest.co.uk",
                publication_date=None,
                journal="Test Journal")
           
    def test_study_list_url(self):
        self.client.login(username='username', password='password')
        response = self.client.get('/studies/')
        self.assertEqual(response.status_code, 200)

    def test_study_pagination_is_ten(self):
        self.client.login(username='username', password='password')
        response = self.client.get(reverse('studies'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['study_list']) == 10)

    def test_number_of_studies_on_last_page(self):
        self.client.login(username='username', password='password')
        response = self.client.get(reverse('studies') +'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['study_list']) == 3)

class StudyDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='username', password='password')
        Study.objects.create(DOI="doi:10.0000/test", 
            title="Test Study",
            publication_date=None,
            journal="Test Journal")
           
    def test_study_detail_url(self):
        study = Study.objects.get(title="Test Study")
        self.client.login(username='username', password='password')
        response = self.client.get(reverse('study_detail', kwargs={"title": study.title}))
        self.assertEqual(response.status_code, 200)

class StudyCreateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='username', password='password')

    def test_create_study(self):
        self.client.login(username='username', password='password')
        response = self.client.post(
            reverse('create_study'), 
            {'DOI': "doi:10.0000/test", 'title': "Test Study", 
            'journal': "Test Journal", 
            'url': "https://www.studytest.co.uk"})
        study = Study.objects.get(title="Test Study")
        self.assertEqual(study.DOI, "doi:10.0000/test")

class StudyUpdateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='username', password='password')
        Study.objects.create(DOI="doi:10.0000/test", 
            title="Test Study",
            publication_date=None,
            journal="Test Journal")

    def test_update_study(self):
        study = Study.objects.get(title="Test Study")
        self.client.login(username='username', password='password')
        response = self.client.post(
            reverse('study_update', kwargs={'title': study.title}), 
            {'DOI': "doi:10.0000/test", 'title': "Test Study", 
            'journal': "Test Journal", 
            'url': "https://www.studytest.co.uk"})
        self.assertEqual(response.status_code, 302)
        study.refresh_from_db()
        self.assertEqual(study.url, 'https://www.studytest.co.uk')

class CountDataDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        mock_file = MagicMock(spec=File)
        mock_file.name = 'gene_count.csv'
        user = User.objects.create_user(username='username', password='password')
        Study.objects.create(DOI="doi:10.0000/test", 
            title="Test Study", 
            url="https://www.studytest.co.uk",
            publication_date=None,
            journal="Test Journal")
        CountData.objects.create(name="Test Count Data", 
                study=Study.objects.get(title="Test Study"), 
                gene_count=mock_file)
           
    def test_count_data_detail_url(self):
        study = Study.objects.get(title="Test Study")
        count_data = CountData.objects.get(name="Test Count Data")
        self.client.login(username='username', password='password')
        response = self.client.get(reverse('count_data_detail', 
            kwargs={"title": study.title, "name": count_data.name}))
        self.assertEqual(response.status_code, 200)

class CountDataUpdateViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        mock_file = MagicMock(spec=File)
        mock_file.name = 'gene_count.csv'
        user = User.objects.create_user(username='username', password='password')
        Study.objects.create(DOI="doi:10.0000/test", 
            title="Test Study", 
            url="https://www.studytest.co.uk",
            publication_date=None,
            journal="Test Journal")
        CountData.objects.create(name="Test Count Data", 
                study=Study.objects.get(title="Test Study"), 
                gene_count=mock_file)

    def test_update_count_data(self):
        mock_file = MagicMock(spec=File)
        mock_file.name = 'gene_count.csv'
        study = Study.objects.get(title="Test Study")
        count_data = CountData.objects.get(name="Test Count Data")
        self.client.login(username='username', password='password')
        response = self.client.post(
            reverse('count_data_update', kwargs={'title': study.title, 'name': count_data.name}), 
            {'name': "Count Data Update", 'study': study, 'gene_count': mock_file})
        self.assertEqual(response.status_code, 302)
        count_data.refresh_from_db()
        self.assertEqual(count_data.name, "Count Data Update")

class SVMModelListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='username', password='password')
        number_of_svm_models = 13
        for svm_id in range(number_of_svm_models):
            mock_file = MagicMock(spec=File)
            mock_file.name = f"gene_count_{svm_id}.csv"
            mock_file_2 = MagicMock(spec=File)
            mock_file_2.name = f"svm_model_{svm_id}.sav"
            Study.objects.create(DOI=f"doi:10.0000/test{svm_id}", 
                title=f"Test Study {svm_id}", 
                url="https://www.studytest.co.uk",
                publication_date=None,
                journal="Test Journal")
            CountData.objects.create(name=f"Test Count Data {svm_id}", 
                    study=Study.objects.get(title=f"Test Study {svm_id}"), 
                    gene_count=mock_file)
            SVMModel.objects.create(model_name=f"Test Model {svm_id}", 
                description="Test", 
                count_data=CountData.objects.get(name=f"Test Count Data {svm_id}"),
                kernel="Linear", C="1", gamma="1",
                model_file=mock_file_2)
           
    def test_svm_model_list_url(self):
        self.client.login(username='username', password='password')
        response = self.client.get('/models/svm/')
        self.assertEqual(response.status_code, 200)

    def test_svm_model_pagination_is_ten(self):
        self.client.login(username='username', password='password')
        response = self.client.get(reverse('svm_models'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['svm_model_list']) == 10)

    def test_number_of_svm_models_on_last_page(self):
        self.client.login(username='username', password='password')
        response = self.client.get(reverse('svm_models') +'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['svm_model_list']) == 3)

class SVMModelDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='username', password='password')
        mock_file = MagicMock(spec=File)
        mock_file.name = 'gene_count.csv'
        mock_file_2 = MagicMock(spec=File)
        mock_file_2.name = 'svm_model.sav'
        Study.objects.create(DOI="doi:10.0000/test", 
            title="Test Study", 
            url="https://www.studytest.co.uk",
            publication_date=None,
            journal="Test Journal")
        CountData.objects.create(name="Test Count Data", 
                study=Study.objects.get(title="Test Study"), 
                gene_count=mock_file)
        SVMModel.objects.create(model_name="Test Model", 
            description="Test", 
            count_data=CountData.objects.get(name="Test Count Data"),
            kernel="Linear", C="1", gamma="1",
            model_file=mock_file_2)
           
    def test_svm_model_detail_url(self):
        svm_model = SVMModel.objects.get(pk=1)
        self.client.login(username='username', password='password')
        response = self.client.get(reverse('svm_model_detail', 
            kwargs={"model_name": svm_model.model_name}))
        self.assertEqual(response.status_code, 200)

class RFModelListViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='username', password='password')
        number_of_rf_models = 13
        for rf_id in range(number_of_rf_models):
            mock_file = MagicMock(spec=File)
            mock_file.name = f"gene_count_{rf_id}.csv"
            mock_file_2 = MagicMock(spec=File)
            mock_file_2.name = f"svm_model_{rf_id}.sav"
            Study.objects.create(DOI=f"doi:10.0000/test{rf_id}", 
                title=f"Test Study {rf_id}", 
                url="https://www.studytest.co.uk",
                publication_date=None,
                journal="Test Journal")
            CountData.objects.create(name=f"Test Count Data {rf_id}", 
                    study=Study.objects.get(title=f"Test Study {rf_id}"), 
                    gene_count=mock_file)
            RFModel.objects.create(model_name=f"Test Model {rf_id}", 
                description="Test", 
                count_data=CountData.objects.get(name=f"Test Count Data {rf_id}"),
                n_estimators="100", max_depth="100", criterion="Entropy", bootstrap='True',
                model_file=mock_file_2)
           
    def test_rf_model_list_url(self):
        self.client.login(username='username', password='password')
        response = self.client.get('/models/rf/')
        self.assertEqual(response.status_code, 200)

    def test_rf_model_pagination_is_ten(self):
        self.client.login(username='username', password='password')
        response = self.client.get(reverse('rf_models'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['rf_model_list']) == 10)

    def test_number_of_rf_models_on_last_page(self):
        self.client.login(username='username', password='password')
        response = self.client.get(reverse('rf_models') +'?page=2')
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['rf_model_list']) == 3)

class RFModelDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(username='username', password='password')
        mock_file = MagicMock(spec=File)
        mock_file.name = 'gene_count.csv'
        mock_file_2 = MagicMock(spec=File)
        mock_file_2.name = 'rf_model.sav'
        Study.objects.create(DOI="doi:10.0000/test", 
            title="Test Study", 
            url="https://www.studytest.co.uk",
            publication_date=None,
            journal="Test Journal")
        CountData.objects.create(name="Test Count Data", 
                study=Study.objects.get(title="Test Study"), 
                gene_count=mock_file)
        RFModel.objects.create(model_name=f"Test Model", 
            description="Test", 
            count_data=CountData.objects.get(name=f"Test Count Data"),
            n_estimators="100", max_depth="100", criterion="Entropy", bootstrap='True',
            model_file=mock_file_2)
           
    def test_rf_model_detail_url(self):
        rf_model = RFModel.objects.get(pk=1)
        self.client.login(username='username', password='password')
        response = self.client.get(reverse('rf_model_detail', 
            kwargs={"model_name": rf_model.model_name}))
        self.assertEqual(response.status_code, 200)