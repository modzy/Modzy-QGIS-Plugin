# -*- coding: utf-8 -*-
"""
 Modzy
   Modzy QGIS plugin
							  -------------------
		begin				 : 2022-01-01
		copyright			 : (C) 2022 by Modzy
		email				 : support@modzy.com

 Modzy’s General Object Detection model uses cutting-edge deep learning and image segmentation techniques to precisely locate and label objects in satellite imagery.
"""

__author__ = 'Modzy'
__date__ = '2022-01-01'
__copyright__ = '(C) 2022 by Modzy'

__revision__ = '$Format:%H$'

from qgis import processing
from qgis.PyQt.QtCore import QCoreApplication
from qgis.core import QgsField, QgsPoint, QgsGeometry, QgsFeature, QgsMessageLog
from qgis.utils import iface
from qgis.core import (QgsProcessing,
					   QgsFeatureSink,
					   QgsProject,
					   QgsPointXY,
					   QgsFillSymbol,
					   QgsRasterPipe,
					   QgsRasterLayer,
					   QgsVectorLayer,
					   QgsLayerTreeLayer,
					   QgsRasterFileWriter,
					   QgsProcessingAlgorithm,
					   QgsProcessingOutputNumber,
					   QgsProcessingException,
					   QgsProcessingParameterFeatureSink,
					   QgsProcessingParameterFeatureSource,
					   QgsProcessingParameterVectorDestination,
					   QgsProcessingParameterRasterLayer,
					   QgsApplication, 
					   QgsAuthMethodConfig,
					   QgsProcessingRegistry,
					   QgsProcessingParameterRasterDestination)

from PyQt5.QtCore import QVariant

import os
from osgeo import gdal, osr
from .modzy_login import get_client

pluginPath = os.path.split(os.path.dirname(__file__))[0]

class GeneralObjectDetectionAlgorithm(QgsProcessingAlgorithm):
	"""
	Detect Objects
	"""
	OUTPUT = 'OUTPUT'
	INPUT = 'INPUT'
		
	def initAlgorithm(self, config):
		"""
		Define the inputs and output of the algorithm
		"""		

		QgsMessageLog.logMessage("Initializing...", "Modzy")

		# Add the input features source. 
		self.addParameter(
			QgsProcessingParameterRasterLayer(
				self.INPUT,
				self.tr('Input Imagery'),
				[QgsProcessing.TypeRaster]
			)
		)

		# Add a feature sink in which to store our processed features
		self.addParameter(
			QgsProcessingParameterVectorDestination(
				self.OUTPUT,
				self.tr('Vector output layer')
			)
		)
		
		self.addOutput(
			QgsProcessingOutputNumber(
				'OUTPUT_COUNT',
				self.tr('Number of features processed')
			)
		)

	def processAlgorithm(self, parameters, context, feedback):
		"""
		Here is where the processing itself takes place.
		"""

		source = self.parameterAsLayer(parameters, self.INPUT, context)
		
		feedback.pushInfo('Starting Inference...')
		
		try:
			extents = source.extent()
			height = source.height()
			mwidth = source.width()
			
			if height > 416 or mwidth > 416:
				feedback.pushInfo('invalid image: image width and height must be less than or equal to 416px: {}, {}'.format(height, mwidth))
				return {self.OUTPUT: "invalid image: image width and height must be less than or equal to 416px"}
				
			mmetadata = source.htmlMetadata()
			feedback.pushInfo('Input extents: {}'.format(extents))
		except Exception as E:
			QgsMessageLog.logMessage('Error in source data: '+str(E), "Modzy")
			
		try:
			feedback.pushInfo('Starting inference, may take a few minutes...')
			QgsMessageLog.logMessage("Processing...", "Modzy")

			model_output = self.general_object_detection(source.source())
			
			if model_output == None:
				feedback.pushInfo("Error initializing Modzy Client, check authentication")
				QgsMessageLog.logMessage('Error initializing Modzy Client, check authentication', "Modzy")

				return {'OUTPUT_COUNT': 0}
			elif model_output['completed']:
				feedback.pushInfo('Inference complete: {},	version:{},	 by {}'.format(model_output['model_name'],model_output['model_version'],model_output['model_author']))
				feedback.pushInfo("Job ID: {}".format(model_output['jobIdentifier']))
			else:
				feedback.pushInfo("Error in inference {}".format(model_output['jobIdentifier']))
				return {'OUTPUT_COUNT': 0}
		except Exception as E:
			feedback.pushInfo('Error when running model {}'.format(E))
			QgsMessageLog.logMessage('Error when running model '+str(E), "Modzy")
		
		try:
			feedback.pushInfo('Model run complete, drawing outlines...')
			QgsMessageLog.logMessage("Rendering...", "Modzy")
			outlines = self.plot_objects(model_output, source.source())
			feedback.pushInfo('Recognized {} objects'.format(outlines))
		except Exception as E:
			feedback.pushInfo('Error getting outlines {}'.format(E))
			QgsMessageLog.logMessage('Error building objects: '+str(E), "Modzy")
			return {'OUTPUT_COUNT': 0}
			
		return {'OUTPUT_COUNT': outlines}


	def general_object_detection(self, filePath):
		client = get_client()
		if client == None:
			return None

		model_id = 'zi2wvziln1'
		model_version = '0.0.2'
		input_name = 'input'
		model_info = client.models.get(model_id)

		job = client.jobs.submit_files(model_id, model_version, {input_name: filePath})
		result = client.results.block_until_complete(job, timeout=None)	  
	
		result['model_info'] = model_info
		result['model_version'] = model_version
		result['model_name'] = model_info.name
		result['model_author'] = model_info.author
	
		return result


	def name(self):
		"""
		Returns the algorithm name, used for identifying the algorithm.
		"""
		return 'General Object Detection'

	def displayName(self):
		"""
		Returns the translated algorithm name, used for
		user-visible display of the algorithm name.
		"""
		return self.tr(self.name())

	def group(self):
		"""
		Returns the name of the group this algorithm belongs to.
		"""
		return self.tr(self.groupId())

	def groupId(self):
		"""
		Returns the unique ID of the group this algorithm belongs to.
		"""
		return 'Satellite Imagery'

	def tr(self, string):
		return QCoreApplication.translate('Processing', string)

	def createInstance(self):
		return GeneralObjectDetectionAlgorithm()


	def plot_objects(self, result, source):
		if source[0] != '/':
			img_name = source
		else:
			img_name = os.path.splitext(source)[0].split('/')[-1]
		
		geoImage = gdal.Open(source)
		geoData = geoImage.GetGeoTransform()
	
		try:
			src_projection =  osr.SpatialReference(wkt=geoImage.GetProjection())
			src_spatial_reference = int(src_projection.GetAttrValue("AUTHORITY", 1))
		except:
			src_spatial_reference = 4326

		src = osr.SpatialReference()
		tgt = osr.SpatialReference()
		src.ImportFromEPSG(src_spatial_reference)
		tgt.ImportFromEPSG(src_spatial_reference)
		transform = osr.CoordinateTransformation(src, tgt)

		object_layer = QgsVectorLayer('Polygon?crs=EPSG:'+str(src_spatial_reference), img_name + ' Objects', "memory")
		object_layer.setOpacity(0.65)
		object_symbol = QgsFillSymbol.createSimple({'color':'140,206,205',
				'color_border':'30,47,63', 
				'width_border':'1'})
		object_layer.renderer().setSymbol(object_symbol)
		object_dp = object_layer.dataProvider()
	
		object_name = object_dp.addAttributes([QgsField("className",QVariant.String)])
		object_prob = object_dp.addAttributes([QgsField("probability",QVariant.Double)])

		object_layer.updateFields()
		object_feat = QgsFeature(object_layer.fields())
	
		output = result.get_first_outputs()["results.json"]
	
		for gobject in output['images'][0]['detections']:
			lat_1 = geoData[3] + gobject['ymin'] * geoData[5]
			lon_1 = geoData[0] + gobject['xmin'] * geoData[1]
			lat_2 = geoData[3] + gobject['ymax'] * geoData[5]
			lon_2 = geoData[0] + gobject['xmax'] * geoData[1]

			raw_points = [(lon_1,lat_1),(lon_1,lat_2),(lon_2,lat_2),(lon_2,lat_1)]
		
			if not src_spatial_reference == 4326:
				coords = [(transform.TransformPoint(x,y))[0:2] for x,y in raw_points]
				raw_points = coords
		
			object_feat = QgsFeature(object_layer.fields())
			bounding_box = QgsGeometry.fromPolygonXY([[QgsPointXY(point[0], point[1]) for point in raw_points]])
			object_feat.setGeometry(bounding_box)
			try:
				object_feat['className'] = gobject['className']
				object_feat['probability'] = gobject['probability']
			except Exception as E:
				print('error adding features', E)
				print(gobject)
			object_dp.addFeatures([object_feat])
		
		object_layer.updateExtents()
		QgsProject.instance().addMapLayers([object_layer])
		
		return(len(output['images'][0]['detections']))
