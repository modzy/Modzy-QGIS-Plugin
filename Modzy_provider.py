# -*- coding: utf-8 -*-
"""
 Modzy
   Modzy QGIS plugin
							  -------------------
		begin				 : 2022-01-01
		copyright			 : (C) 2022 by Modzy
		email				 : support@modzy.com

 This script initializes the plugin, making it known to QGIS.
"""

__author__ = 'Modzy'
__date__ = '2022-01-01'
__copyright__ = '(C) 2022 by Modzy'
__revision__ = '$Format:%H$'

from qgis.core import QgsProcessingProvider
from .VehicleDetection_algorithm import VehicleDetectionAlgorithm
from .GeneralObjectDetection_algorithm import GeneralObjectDetectionAlgorithm
from .BuildingSegmentation_algorithm import BuildingSegmentationAlgorithm

# Add additional models here and make sure to load in loadAlgorithms()

# from .BuildingSegmentation_algorithm import BuildingSegmentationAlgorithm
# from .building_detection_algorithm import ModzyAlgorithm
# from .GeneralObjectDetection_algorithm import GeneralObjectDetectionAlgorithm
# from .SodCoverage_algorithm import SodCoverageAlgorithm
# from .PavementCondition_algorithm import PavementConditionAlgorithm
# from .TreeCoverage_algorithm import TreeCoverageAlgorithm
# from .SARShipDetection_algorithm import SARShipDetectionAlgorithm
# from .GeospatialRegistration_algorithm import GeospatialRegistrationAlgorithm

from modzy import ApiClient

class ModzyProvider(QgsProcessingProvider):
	def __init__(self):
		""" Default constructor. """
		QgsProcessingProvider.__init__(self)

	def client(self):
		auth_configs = QgsApplication.authManager().availableAuthMethodConfigs()
		auth_mgr = QgsApplication.authManager()
		auth_cfg = QgsAuthMethodConfig()
		client = None 
	
		for each in auth_configs:
			if (auth_configs[each].name() == 'ModzyAPI'):
				auth_id = auth_configs[each].id()
				api_url = auth_configs[each].uri()
				auth_mgr.loadAuthenticationConfig(auth_id, auth_cfg, True)
				api_key = auth_cfg.configMap()['password']
	
				client = ApiClient(base_url=api_url, api_key=api_key)
				return client

		if client == None:
			return "error"		

	def unload(self):
		""" Unloads the provider. No additional step required by Modzy """
		pass

	def loadAlgorithms(self):
		"""
		Loads all algorithms belonging to Modzy.
		
		## TODO: check if account is allowed to load each algo!
			if client.model(modelid) then...
		"""
		self.addAlgorithm(VehicleDetectionAlgorithm())
		self.addAlgorithm(GeneralObjectDetectionAlgorithm())
		self.addAlgorithm(BuildingSegmentationAlgorithm())

		# add additional algorithms here
		# self.addAlgorithm(MyOtherAlgorithm())

#		  self.addAlgorithm(BuildingSegmentationAlgorithm())
#		  self.addAlgorithm(ModzyAlgorithm())
#		  self.addAlgorithm(GeneralObjectDetectionAlgorithm())
#		  self.addAlgorithm(SodCoverageAlgorithm())
#		  self.addAlgorithm(TreeCoverageAlgorithm())
#		  self.addAlgorithm(PavementConditionAlgorithm())
#		  self.addAlgorithm(SARShipDetectionAlgorithm())
#		  self.addAlgorithm(GeospatialRegistrationAlgorithm())
		

	def id(self):
		"""
		Returns the unique provider id, used for identifying the provider. 
		"""
		return 'Modzy'

	def name(self):
		"""
		Returns the provider name, which is used within the GUI.
		This string should be short and can be localised.
		"""
		return self.tr('Modzy')

	def icon(self):
		"""
		Returns QIcon displayed inside the Processing toolbox.
		"""
		return QgsProcessingProvider.icon(self)

	def longName(self):
		"""
		Returns the a longer version of the provider name, including
		extra details such as version numbers and localization.
		"""
		return self.name()
