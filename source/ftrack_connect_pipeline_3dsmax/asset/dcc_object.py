# :coding: utf-8
# :copyright: Copyright (c) 2014-2022 ftrack

import logging

from ftrack_connect_pipeline.asset.dcc_object import DccObject
from ftrack_connect_pipeline_3dsmax.constants import asset as asset_const
from ftrack_connect_pipeline_3dsmax.utils import custom_commands as max_utils

from pymxs import runtime as rt


class MaxDccObject(DccObject):
    '''MaxDccObject class.'''

    ftrack_plugin_id = asset_const.FTRACK_PLUGIN_ID
    '''Plugin id used on some DCC applications '''

    def __init__(self, name=None, from_id=None, **kwargs):
        '''
        If the *from_id* is provided find an object in the dcc with the given
        *from_id* as assset_info_id.
        If a *name* is provided create a new object in the dcc.
        '''
        self.logger = logging.getLogger(
            '{0}.{1}'.format(__name__, self.__class__.__name__)
        )
        super(MaxDccObject, self).__init__(name, from_id, **kwargs)

    def __setitem__(self, k, v):
        '''
        Sets the given *v* into the given *k* and automatically set the
        attributes of the current self :obj:`name` on the DCC
        '''
        dcc_object = rt.getNodeByName(self.name, exact=True)
        # Get the Max Dcc object
        if not dcc_object:
            self.logger.warning(
                'Could not find MaxDccObject with name {}'.format(self.name)
            )
            return
        # Unfreeze the object to enable modifications
        try:
            rt.unfreeze(dcc_object)
        except:
            self.logger.debug(
                "Could not unfreeze object {0}".format(dcc_object.Name))

        if str(k) == asset_const.REFERENCE_OBJECT:
            rt.setProperty(dcc_object, k, str(self.name))
        elif str(k) == asset_const.IS_LATEST_VERSION:
            rt.setProperty(dcc_object, k, bool(v))
        # TODO: Check if this is necesary, shouldnt be.
        # elif str(k) == asset_const.ASSET_INFO_OPTIONS:
        #     decoded_value = self.asset_info[str(k)]
        #     json_data = json.dumps(decoded_value)
        #     if six.PY2:
        #         encoded_value = base64.b64encode(json_data)
        #     else:
        #         input_bytes = json_data.encode('utf8')
        #         encoded_value = base64.b64encode(input_bytes).decode('ascii')
        #     rt.setProperty(
        #         dcc_object, k, str(encoded_value)
        #     )
        else:
            rt.setProperty(dcc_object, k, v)
        # TODO: This might be necessary.
        # elif k == asset_const.DEPENDENCY_IDS:
        #     cmds.setAttr(
        #         '{}.{}'.format(self.name, k),
        #         *([len(v)] + v),
        #         type="stringArray",
        #         l=True
        #     )
        #

        # Freeze the object to make sure no one make modifications on it.
        try:
            rt.freeze(dcc_object)
        except Exception as e:
            self.logger.debug(
                "Could not freeze object {0}, Error: {1}".format(
                    dcc_object.Name, e
                )
            )

        super(MaxDccObject, self).__setitem__(k, v)

    def create(self, name):
        '''
        Creates a new dcc_object with the given *name* if doesn't exists.
        '''
        if self._name_exists(name):
            error_message = "{} already exists in the scene".format(name)
            self.logger.error(error_message)
            raise RuntimeError(error_message)

        dcc_object = rt.FtrackAssetHelper()
        dcc_object.Name = name

        # Try to freeze the helper object and lock the transform.
        try:
            rt.freeze(dcc_object)
            rt.setTransformLockFlags(dcc_object, rt.name("all"))
        except Exception as e:
            self.logger.debug(
                "Could not freeze object {0}, Error: {1}".format(
                    name, e
                )
            )

        self.logger.debug('Creating new dcc object {}'.format(dcc_object))
        self.name = name
        return self.name

    def _name_exists(self, name):
        '''
        Return true if the given *name* exists in the scene.
        '''

        if rt.getNodeByName(name, exact=True):
            return True

        return False

    def from_asset_info_id(self, asset_info_id):
        '''
        Checks max scene to get all the ftrackAssetNode objects. Compares them
        with the given *asset_info_id* and returns them if matches.
        '''
        ftrack_asset_nodes = max_utils.get_ftrack_nodes()
        for dcc_object_name in ftrack_asset_nodes:

            # id_value = cmds.getAttr(
            #     '{}.{}'.format(dcc_object_name, asset_const.ASSET_INFO_ID)
            # )

            if id_value == asset_info_id:
                self.logger.debug(
                    'Found existing object: {}'.format(dcc_object_name)
                )
                self.name = dcc_object_name
                return self.name

        self.logger.debug(
            "Couldn't found an existing object for the asset info id: {}".format(
                asset_info_id
            )
        )
        return None

    @staticmethod
    def dictionary_from_object(object_name):
        '''
        Static method to be used without initializing the current class.
        Returns a dictionary with the keys and values of the given
        *object_name* if exists.

        *object_name* ftrackAssetNode object type from max scene.
        '''
        logger = logging.getLogger(
            '{0}.{1}'.format(__name__, __class__.__name__)
        )
        param_dict = {}
        # if not cmds.objExists(object_name):
        #    error_message = "{} Object doesn't exists".format(object_name)
        #    logger.error(error_message)
        #    return param_dict
        # all_attr = cmds.listAttr(object_name, c=True, se=True)
        for attr in all_attr:
            # if cmds.attributeQuery(attr, node=object_name, msg=True):
            #    continue
            # attr_value = cmds.getAttr('{}.{}'.format(object_name, attr))
            param_dict[attr] = attr_value
        return param_dict

    def connect_objects(self, objects):
        '''
        Link the given *objects* ftrack attribute to the self
        :obj:`name` object asset_link attribute in max.

        *objects* List of Max DAG objects
        '''
        # for obj in objects:
        # if cmds.lockNode(obj, q=True)[0]:
        #     cmds.lockNode(obj, l=False)
        #
        # if not cmds.attributeQuery('ftrack', n=obj, exists=True):
        #     cmds.addAttr(obj, ln='ftrack', at='message')
        #
        # if not cmds.listConnections('{}.ftrack'.format(obj)):
        #     cmds.connectAttr(
        #         '{}.{}'.format(self.name, asset_const.ASSET_LINK),
        #         '{}.ftrack'.format(obj),
        #     )
