# file will be exec'd; there can be no encoding tag
# :copyright: Copyright (c) 2019 ftrack

import functools
import logging
import os
from qtpy import QtWidgets, QtCore, QtGui

import MaxPlus

from ftrack_connect_pipeline import session, event, host, utils

from ftrack_connect_pipeline_3dsmax import usage, host as max_host
from ftrack_connect_pipeline_3dsmax.constants import UI, HOST


logger = logging.getLogger('ftrack_connect_pipeline_3dsmax.scripts.init_ftrack_pipeline')

created_dialogs = dict()


def open_dialog(dialog_class, event_manager):
    '''Open *dialog_class* and create if not already existing.'''
    dialog_name = dialog_class

    if dialog_name not in created_dialogs:
        main_window = MaxPlus.GetQMaxMainWindow()
        ftrack_dialog = dialog_class
        created_dialogs[dialog_name] = ftrack_dialog(
            event_manager, parent=main_window
        )
    created_dialogs[dialog_name].show()


def load_and_init():

    event_manager = event.EventManager(
        session=session.get_shared_session(),
        remote=utils.remote_event_mode(),
        ui=UI,
        host=HOST
    )

    host.initialise(event_manager)

    usage.send_event(
        'USED-FTRACK-CONNECT-PIPELINE-3DS-MAX'
    )

    from ftrack_connect_pipeline_3dsmax.client import publish

    # Enable loader and publisher only if is set to run local (default)

    if not event_manager.remote:
        dialogs = [
            (publish.QtPipelineMaxPublishWidget, 'Publisher'),
        ]
    else:
        max_host.notify_connected_client(event_manager)

    menu_name = max_host.get_ftrack_menu()

    if MaxPlus.MenuManager.MenuExists(menu_name):
        MaxPlus.MenuManager.UnregisterMenu(menu_name)

    ftrack_menu_builder = MaxPlus.MenuBuilder(menu_name)

    # Register and hook the dialog in ftrack menu
    for item in dialogs:
        if item == 'divider':
            ftrack_menu_builder.AddSeparator()
            continue

        dialog_class, label = item

        ftrack_menu_builder.AddItem(
            MaxPlus.ActionFactory.Create(
                category='ftrack', name=label, fxn=functools.partial(
                    open_dialog, dialog_class, event_manager
                )
            )
        )
    ftrack_menu_builder.Create(MaxPlus.MenuManager.GetMainMenu())


load_and_init()
