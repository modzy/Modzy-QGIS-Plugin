# -*- coding: utf-8 -*-
"""
 Modzy
   Modzy QGIS plugin
                              -------------------
        begin                : 2022-01-01
        copyright            : (C) 2022 by Modzy
        email                : support@modzy.com

 This script initializes the plugin, making it known to QGIS.
"""

__author__ = 'Modzy'
__date__ = '2022-01-01'
__copyright__ = '(C) 2022 by Modzy'
__revision__ = '$Format:%H$'

import os, sys, inspect

from qgis.core import QgsProcessingAlgorithm, QgsApplication
from .Modzy_provider import ModzyProvider

cmd_folder = os.path.split(inspect.getfile(inspect.currentframe()))[0]
if cmd_folder not in sys.path:
    sys.path.insert(0, cmd_folder)

class ModzyPlugin(object):

    def __init__(self):
        self.provider = None

    def initProcessing(self):
        self.provider = ModzyProvider()
        QgsApplication.processingRegistry().addProvider(self.provider)

    def initGui(self):
        self.initProcessing()

    def unload(self):
        QgsApplication.processingRegistry().removeProvider(self.provider)
