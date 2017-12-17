""" Module for record constants """
import os

from sap.cf_logging import defaults
from sap.cf_logging.record import util


LAYER = 'python'
COMPONENT_ID = util.get_vcap_param('application_id', defaults.UNKNOWN)
COMPONENT_NAME = util.get_vcap_param('name', defaults.UNKNOWN)
COMPONENT_INSTANCE = os.getenv('CF_INSTANCE_INDEX', 0)
SPACE_ID = util.get_vcap_param('space_id', defaults.UNKNOWN)
SPACE_NAME = util.get_vcap_param('space_name', defaults.UNKNOWN)
CONTAINER_ID = os.getenv('CF_INSTANCE_IP', defaults.UNKNOWN)
COMPONENT_TYPE = 'application'
