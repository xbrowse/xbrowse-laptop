from xbrowse.reference import Reference
from xbrowse.annotation import VariantAnnotator
from xbrowse.datastore.population_datastore import PopulationDatastore
from xbrowse.datastore.project_datastore import ProjectDatastore
from xbrowse.coverage import CoverageDatastore
from xbrowse.datastore import MongoDatastore
from xbrowse.cnv import CNVStore

import os
import pymongo
import imp

#from xbrowse_server.xbrowse_annotation_controls import CustomAnnotator

# django stuff

DEBUG = True
#COMPRESS_ENABLED = False
BASE_URL = 'http://localhost:8000/'
URL_PREFIX = '/'

GENERATED_FILES_DIR = os.path.join(os.path.dirname(__file__), 'generated_files')

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(os.path.dirname(__file__), 'database.sqlite'),
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

MEDIA_ROOT = GENERATED_FILES_DIR + '/media/'
STATIC_ROOT = GENERATED_FILES_DIR + '/static_root/'

STATICFILES_DIRS = (
    os.path.dirname(os.path.realpath(__file__)) + '/xbrowse_server/staticfiles/',
)

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


#
# xbrowse stuff
#
COMMON_SNP_FILE = "/vagrant/xbrowse-laptop-downloads/markers.txt"

REFERENCEDATA_DIR = os.path.dirname(os.path.realpath(__file__)) + '/'
HGMD_OMIM_FILE = '/vagrant/xbrowse-laptop-downloads/hgmd_omim_genes.txt'

reference_settings = imp.load_source(
    'reference_settings',
    os.path.dirname(os.path.realpath(__file__)) + '/reference_settings.py'
)
REFERENCE = Reference(reference_settings)

CUSTOM_ANNOTATOR = None

annotator_settings = imp.load_source(
    'annotator_settings',
    os.path.dirname(os.path.realpath(__file__)) + '/annotator_settings.py'
)
ANNOTATOR = VariantAnnotator(
    settings_module=annotator_settings,
    custom_annotator=CUSTOM_ANNOTATOR,
)

_conn = pymongo.Connection()
datastore_db = _conn['xbrowse_datastore']
population_datastore_db = _conn['xbrowse_pop_datastore']

# datastore_settings = imp.load_source(
#     'datastore_settings',
#     os.path.dirname(os.path.realpath(__file__)) + '/datastore_settings.py'
# )
DATASTORE = MongoDatastore(datastore_db, ANNOTATOR)


POPULATION_DATASTORE = PopulationDatastore(population_datastore_db, ANNOTATOR)

coverage_db = _conn['xbrowse_coverage']
COVERAGE_STORE = CoverageDatastore(coverage_db, REFERENCE)

project_datastore_db = _conn['xbrowse_proj_store']
PROJECT_DATASTORE = ProjectDatastore(project_datastore_db, ANNOTATOR)


CNV_STORE = CNVStore('xbrowse_cnvs', REFERENCE)