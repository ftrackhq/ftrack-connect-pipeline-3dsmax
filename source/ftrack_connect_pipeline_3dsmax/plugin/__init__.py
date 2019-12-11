# :coding: utf-8
# :copyright: Copyright (c) 2019 ftrack

from ftrack_connect_pipeline import constants
from ftrack_connect_pipeline_3dsmax import constants as max_constants
from ftrack_connect_pipeline import plugin
from ftrack_connect_pipeline_qt import plugin as pluginWidget


class _BaseMax(plugin._Base):
    host = max_constants.HOST


class BaseMaxPlugin(plugin.BasePlugin, _BaseMax):
    type = 'plugin'


class BaseMaxWidget(pluginWidget.BasePluginWidget, _BaseMax):
    type = 'widget'
    ui = max_constants.UI


class ContextMaxPlugin(BaseMaxPlugin):
    plugin_type = constants.CONTEXT


class ContextMaxWidget(BaseMaxWidget):
    plugin_type = constants.CONTEXT


# TODO(spetterborg) figure out why he likes this construction
from ftrack_connect_pipeline_3dsmax.plugin.publish import *
