# :coding: utf-8
# :copyright: Copyright (c) 2019 ftrack

from ftrack_connect_pipeline import plugin
from ftrack_connect_pipeline import constants
from ftrack_connect_pipeline_qt import plugin as pluginWidget
from ftrack_connect_pipeline_3dsmax.plugin import BaseMaxPlugin, BaseMaxWidget


# PLUGINS
class CollectorMaxPlugin(BaseMaxPlugin, plugin.CollectorPlugin):
    plugin_type = constants.COLLECTORS


class ValidatorMaxPlugin(BaseMaxPlugin, plugin.ValidatorPlugin):
    plugin_type = constants.VALIDATORS


class OutputMaxPlugin(BaseMaxPlugin, plugin.OutputPlugin):
    plugin_type = constants.OUTPUTS


class PublisherMaxPlugin(BaseMaxPlugin, plugin.PublisherPlugin):
    plugin_type = constants.PUBLISHERS


# WIDGET
class CollectorMaxWidget(BaseMaxWidget, pluginWidget.CollectorWidget):
    plugin_type = constants.COLLECTORS


class ValidatorMaxWidget(BaseMaxWidget, pluginWidget.ValidatorWidget):
    plugin_type = constants.VALIDATORS


class OutputMaxWidget(BaseMaxWidget, pluginWidget.OutputWidget):
    plugin_type = constants.OUTPUTS


class PublisherMaxWidget(BaseMaxWidget, pluginWidget.PublisherWidget):
    plugin_type = constants.PUBLISHERS
