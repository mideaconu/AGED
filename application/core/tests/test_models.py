# 
# core/test_models.py
#
# Author: Mihai Ionut Deaconu
#

import unittest
from unittest.mock import MagicMock
from core.models import Disease, Study, CountData, SVMModel, RFModel, Sample, Gene
from django.test import TestCase
from django.core.exceptions import ValidationError
from django.core.files import File

class DiseaseModelTest(TestCase):
  @classmethod
  def setUpTestData(cls):
    Disease.objects.create(name="Test Disease", 
      abbreviation="TD", 
      description="Neurodegenerative disorder",
      url="https://www.diseasetest.co.uk")

  def test_disease_string(self):
    disease = Disease.objects.get(id=1)
    expected_object_name = f'{disease.name} ({disease.abbreviation})'
    self.assertEquals(expected_object_name, str(disease))

  def test_disease_absolute_url(self):
    disease = Disease.objects.get(id=1)
    self.assertEquals(disease.get_absolute_url(), '/diseases/TD')

class StudyModelTest(TestCase):
  @classmethod
  def setUpTestData(cls):
    Study.objects.create(DOI="doi:10.0000/test", 
      title="Test Study", 
      url="https://www.studytest.co.uk",
      publication_date=None,
      journal="Test Journal")

  def test_DOI_validation_1(self):
    invalid_study = Study(DOI="invalid", 
      title="Test Study", 
      url="https://www.studytest.co.uk",
      publication_date=None,
      journal="Test Journal")
    with self.assertRaises(ValidationError):
      if invalid_study.full_clean():
        invalid_study.save()
    self.assertEqual(Study.objects.filter(DOI="invalid").count(), 0)

  def test_DOI_validation_2(self):
    invalid_study = Study(DOI="doi:invalid", 
      title="Test Study", 
      url="https://www.studytest.co.uk",
      publication_date=None,
      journal="Test Journal")
    with self.assertRaises(ValidationError):
      if invalid_study.full_clean():
        invalid_study.save()
    self.assertEqual(Study.objects.filter(DOI="invalid").count(), 0)

  def test_DOI_validation_3(self):
    invalid_study = Study(DOI="invalid/invalid", 
      title="Test Study", 
      url="https://www.studytest.co.uk",
      publication_date=None,
      journal="Test Journal")
    with self.assertRaises(ValidationError):
      if invalid_study.full_clean():
        invalid_study.save()
    self.assertEqual(Study.objects.filter(DOI="invalid").count(), 0)

  def test_study_string(self):
    study = Study.objects.get(id=1)
    expected_object_name = f'{study.title} {study.DOI}'
    self.assertEquals(expected_object_name, str(study))

  def test_study_absolute_url(self):
    study = Study.objects.get(id=1)
    self.assertEquals(study.get_absolute_url(), '/studies/Test%20Study')

class CountDataModelTest(TestCase):
  @classmethod
  def setUpTestData(cls):
    study = Study.objects.create(DOI="doi:10.0000/test", 
      title="Test Study", 
      url="https://www.studytest.co.uk",
      publication_date=None,
      journal="Test Journal")
    mock_file = MagicMock(spec=File)
    mock_file.name = 'gene_count.csv'
    count_data = CountData.objects.create(name="Test Count Data", 
      study=study,
      gene_count=mock_file)

  def test_count_data_string(self):
    countdata = CountData.objects.get(id=1)
    expected_object_name = f'{countdata.name}'
    self.assertEquals(expected_object_name, str(countdata))

  def test_count_data_absolute_url(self):
    countdata = CountData.objects.get(id=1)
    self.assertEquals(countdata.get_absolute_url(), '/studies/Test%20Study/count_data/Test%20Count%20Data')

class SVMModelTest(TestCase):
  @classmethod
  def setUpTestData(cls):
    mock_file_cd = MagicMock(spec=File)
    mock_file_cd.name = 'gene_count.csv'
    mock_file_svm = MagicMock(spec=File)
    mock_file_svm.name = 'model.sav'
    study = Study.objects.create(DOI="doi:10.0000/test", 
      title="Test Study", 
      url="https://www.studytest.co.uk",
      publication_date=None,
      journal="Test Journal")
    count_data = CountData.objects.create(name="Test Count Data", 
      study=study,
      gene_count=mock_file_cd)
    SVMModel.objects.create(model_name="Test SVM", 
      description="Test", 
      count_data=count_data,
      kernel="Linear",
      C="10",
      gamma="0.1",
      model_file=mock_file_svm)

  def test_kernel(self):
    svm = SVMModel.objects.get(id=1)
    svm.kernel = "Invalid Kernel"
    self.assertEqual(SVMModel.objects.filter(kernel="Invalid Kernel").count(), 0)

  def test_C_1(self):
    svm = SVMModel.objects.get(id=1)
    svm.C = "Invaid C"
    self.assertEqual(SVMModel.objects.filter(C="Invalid C").count(), 0)

  def test_C_2(self):
    svm = SVMModel.objects.get(id=1)
    svm.C = "7"
    self.assertEqual(SVMModel.objects.filter(C="7").count(), 0)

  def test_gamma_1(self):
    svm = SVMModel.objects.get(id=1)
    svm.gamma = "Invaid Gamma"
    self.assertEqual(SVMModel.objects.filter(gamma="Invalid Gamma").count(), 0)

  def test_gamma_2(self):
    svm = SVMModel.objects.get(id=1)
    svm.gamma = "7"
    self.assertEqual(SVMModel.objects.filter(gamma="7").count(), 0)

  def test_svm_model_string(self):
    svm = SVMModel.objects.get(id=1)
    expected_object_name = f'{svm.model_name}'
    self.assertEquals(expected_object_name, str(svm))

  def test_svm_model_absolute_url(self):
    svm = SVMModel.objects.get(id=1)
    self.assertEquals(svm.get_absolute_url(), '/models/svm/Test%20SVM')

class RFModelTest(TestCase):
  @classmethod
  def setUpTestData(cls):
    mock_file_cd = MagicMock(spec=File)
    mock_file_cd.name = 'gene_count.csv'
    mock_file_svm = MagicMock(spec=File)
    mock_file_svm.name = 'model.sav'
    study = Study.objects.create(DOI="doi:10.0000/test", 
      title="Test Study", 
      url="https://www.studytest.co.uk",
      publication_date=None,
      journal="Test Journal")
    count_data = CountData.objects.create(name="Test Count Data", 
      study=study,
      gene_count=mock_file_cd)
    RFModel.objects.create(model_name="Test RF", 
      description="Test", 
      count_data=count_data,
      n_estimators="100",
      max_depth="10",
      criterion="Entropy",
      bootstrap="True",
      model_file=mock_file_svm)

  def test_criterion(self):
    rf = RFModel.objects.get(id=1)
    rf.criterion = "Invalid Criterion"
    self.assertEqual(RFModel.objects.filter(criterion="Invalid Criterion").count(), 0)

  def test_bootstrap(self):
    rf = RFModel.objects.get(id=1)
    rf.bootstrap = "Invalid Boolean"
    self.assertEqual(RFModel.objects.filter(bootstrap="Invalid Boolean").count(), 0)

  def test_rf_model_string(self):
    rf = RFModel.objects.get(id=1)
    expected_object_name = f'{rf.model_name}'
    self.assertEquals(expected_object_name, str(rf))

  def test_rf_model_absolute_url(self):
    rf = RFModel.objects.get(id=1)
    self.assertEquals(rf.get_absolute_url(), '/models/rf/Test%20RF')

class SampleModelTest(TestCase):
  @classmethod
  def setUpTestData(cls):
    mock_file = MagicMock(spec=File)
    mock_file.name = 'gene_count.csv'
    disease = Disease.objects.create(name="Test Disease", 
      abbreviation="TD", 
      description="Neurodegenerative disorder",
      url="https://www.diseasetest.co.uk")
    study = Study.objects.create(DOI="doi:10.0000/test", 
      title="Test Study", 
      url="https://www.studytest.co.uk",
      publication_date=None,
      journal="Test Journal")
    count_data = CountData.objects.create(name="Test Count Data", 
      study=study,
      gene_count=mock_file)
    Sample.objects.create(count_data=count_data,
      sample_ID="TEST_0000",
      sample_source="Test Source",
      brain_region="Test Region",
      RIN="10",
      diagnosis=disease,
      sex="M",
      age_at_death="78",
      ApoE="34",
      PMI="3")

  def test_gender(self):
    sample = Sample.objects.get(sample_ID="TEST_0000")
    sample.sex = "Invalid Gender"
    self.assertEqual(Sample.objects.filter(sex="Invalid Gender").count(), 0)

  def test_sample_string(self):
    sample = Sample.objects.get(sample_ID="TEST_0000")
    expected_object_name = f'{sample.sample_ID}'
    self.assertEquals(expected_object_name, str(sample))

  def test_sample_absolute_url(self):
    sample = Sample.objects.get(sample_ID="TEST_0000")
    self.assertEquals(sample.get_absolute_url(), '/studies/Test%20Study/count_data/Test%20Count%20Data/samples/TEST_0000')

class GeneModelTest(TestCase):
  @classmethod
  def setUpTestData(cls):
    Gene.objects.create(gene_id="ENSG00000000000", 
      gene_description="Test",
      gene_name="Test Gene", 
      gene_type="Test")

  def test_gene_string(self):
    gene = Gene.objects.get(gene_id="ENSG00000000000")
    expected_object_name = f'{gene.gene_id}'
    self.assertEquals(expected_object_name, str(gene))
