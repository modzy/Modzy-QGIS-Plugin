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


def classFactory(iface):
    """
    Load ModzyPlugin class from file Modzy.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .Modzy import ModzyPlugin
    return ModzyPlugin()
