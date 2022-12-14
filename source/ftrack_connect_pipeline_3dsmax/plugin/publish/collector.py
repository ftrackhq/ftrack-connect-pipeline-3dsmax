# :coding: utf-8
# :copyright: Copyright (c) 2014-2022 ftrack

from ftrack_connect_pipeline import plugin
from ftrack_connect_pipeline_qt import plugin as pluginWidget
from ftrack_connect_pipeline_3dsmax.plugin import (
    MaxBasePlugin,
    MaxBasePluginWidget,
)


class MaxPublisherCollectorPlugin(
    plugin.PublisherCollectorPlugin, MaxBasePlugin
):
    '''Class representing a Collector Plugin

    .. note::

        _required_output a List
    '''


class MaxPublisherCollectorPluginWidget(
    pluginWidget.PublisherCollectorPluginWidget, MaxBasePluginWidget
):
    '''Class representing a Collector Widget

    .. note::

        _required_output a List
    '''
