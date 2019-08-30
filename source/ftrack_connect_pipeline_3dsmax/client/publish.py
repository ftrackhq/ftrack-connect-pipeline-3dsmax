# :coding: utf-8
# :copyright: Copyright (c) 2019 ftrack

from ftrack_connect_pipeline.client.publish import QtPipelinePublishWidget
from qtpy import QtCore, QtWidgets

from ftrack_connect_pipeline_3dsmax.constants import HOST, UI


class QtPipelineMaxPublishWidget(QtWidgets.QDockWidget):
    '''Dockable maya load widget'''

    def __init__(self, event_manager, parent=None):
        super(QtPipelineMaxPublishWidget, self).__init__(parent=parent)
        self.my_widget = QtPipelinePublishWidget(
            event_manager=event_manager, parent=parent
        )
        self.setWindowTitle('Max Pipeline Publisher {}'.format(event_manager.hostid))
        self.setObjectName('Max Pipeline Publisher')
        self.setWidget(self.my_widget)
        parent.addDockWidget(QtCore.Qt.RightDockWidgetArea, self)
        self.setFloating(True)

    def show(self):
        super(QtPipelineMaxPublishWidget, self).show()
