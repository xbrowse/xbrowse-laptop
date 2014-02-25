from xbrowse.reference import Reference
from xbrowse.annotation import VariantAnnotator, PopulationFrequencyStore, HackedVEPAnnotator
from xbrowse.datastore.population_datastore import PopulationDatastore
from xbrowse.datastore.project_datastore import ProjectDatastore
from xbrowse.coverage import CoverageDatastore
from xbrowse.datastore import MongoDatastore
from xbrowse.cnv import CNVStore

import os
import pymongo
import imp

from xbrowse_annotation_controls import CustomAnnotator

# django stuff

DEBUG = True
#COMPRESS_ENABLED = True
BASE_URL = 'http://localhost:8000/'
URL_PREFIX = '/'

# TODO: switch to postgres DB - didn't feel like debugging some auth issue 
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': '/home/vagrant/database.sqlite',
        'USER': '',
        'PASSWORD': '',
        'HOST': '',
    }
}

MEDIA_ROOT = os.path.dirname(os.path.realpath(__file__)) + '/../media/'

STATIC_ROOT = os.path.dirname(os.path.realpath(__file__)) + '/../static_root/'

STATICFILES_DIRS = (
    os.path.dirname(os.path.realpath(__file__)) + '/staticfiles/',
)

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# other server stuff

VEP_CACHE_DIR = '/home/vagrant'
VEP_PL_PATH = '/home/vagrant/variant_effect_predictor/variant_effect_predictor.pl'
DEFAULT_CONTROL_COHORT = None
COMMON_SNP_FILE = "/home/vagrant/markers.txt"


# data files
REFERENCEDATA_DIR = '/home/vagrant/server_files/'
HGMD_OMIM_FILE = REFERENCEDATA_DIR + 'hgmd_omim_genes.txt'
REFSEQ_DESCRIPTION_FILE = REFERENCEDATA_DIR + "refseq_descriptions.txt"
ESP_TARGET_FILE = REFERENCEDATA_DIR + 'esp_target.interval_list'

#
# xbrowse stuff
#

SETTINGS_DIR = '/opt/xbrowse/'

reference_settings = imp.load_source(
    'reference_settings',
    SETTINGS_DIR + 'reference_settings.py'
)
REFERENCE = Reference(reference_settings)

population_frequency_store_settings = imp.load_source(
    'popfreq_store_settings',
    SETTINGS_DIR + 'popfreq_store_settings.py'
)
POPULATION_FREQUENCY_STORE = PopulationFrequencyStore(population_frequency_store_settings)

vep_settings = imp.load_source(
    'vep_settings',
    SETTINGS_DIR + 'vep_settings.py'
)
VEP_ANNOTATOR = HackedVEPAnnotator(vep_settings)

annotator_settings = imp.load_source(
    'annotator_settings',
    SETTINGS_DIR + 'annotator_settings.py'
)
ANNOTATOR = VariantAnnotator(
    settings_module=annotator_settings,
    reference=REFERENCE,
    population_frequency_store=POPULATION_FREQUENCY_STORE,
    vep_annotator=VEP_ANNOTATOR,
)

_conn = pymongo.Connection()
datastore_db = _conn['xbrowse_datastore']
population_datastore_db = _conn['xbrowse_pop_datastore']

DATASTORE = MongoDatastore(datastore_db, ANNOTATOR)
POPULATION_DATASTORE = PopulationDatastore(population_datastore_db, ANNOTATOR)

coverage_db = _conn['xbrowse_coverage']
COVERAGE_STORE = CoverageDatastore(coverage_db, REFERENCE)

project_datastore_db = _conn['xbrowse_proj_store']
PROJECT_DATASTORE = ProjectDatastore(project_datastore_db, ANNOTATOR)

cnv_store_settings = imp.load_source(
    'cnv_store_settings',
    SETTINGS_DIR + 'cnv_store_settings.py'
)
CNV_STORE = CNVStore(cnv_store_settings, REFERENCE)