#! /usr/bin/python

import sys
import logging

logging.basicConfig(stream=sys.stderr)
sys.path.insert(0,"/home/groupm/mediaops-project/mediaops/")

from templates.webapp import app as application


