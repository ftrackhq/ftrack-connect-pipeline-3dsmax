# :coding: utf-8
# :copyright: Copyright (c) 2014-2020 ftrack

from Qt import QtCore, QtWidgets

from ftrack_connect_pipeline_qt.client.asset_manager import QtAssetManagerClient
import ftrack_connect_pipeline.constants as constants
import ftrack_connect_pipeline_qt.constants as qt_constants
import ftrack_connect_pipeline_3dsmax.constants as max_constants


class MaxAssetManagerClient(QtAssetManagerClient):
    ui = [constants.UI, qt_constants.UI, max_constants.UI]

    '''Dockable maya load widget'''
    def __init__(self, event_manager, parent=None):
        super(MaxAssetManagerClient, self).__init__(
            event_manager=event_manager, parent=parent
        )
        self.dock_widget = QtWidgets.QDockWidget(parent=parent)
        self.setWindowTitle('Max Pipeline Asset Manager')
        self.setObjectName('Max Pipeline Asset Manager')
        self.dock_widget.setWidget(self)
        parent.addDockWidget(QtCore.Qt.RightDockWidgetArea, self.dock_widget)
        self.dock_widget.setFloating(True)

    def show(self):
        self.dock_widget.show()
        super(MaxAssetManagerClient, self).show()
