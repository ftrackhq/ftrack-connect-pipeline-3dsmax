# :coding: utf-8
# :copyright: Copyright (c) 2014-2020 ftrack

from ftrack_connect_pipeline import constants
from ftrack_connect_pipeline.host.engine import AssetManagerEngine
from ftrack_connect_pipeline_3dsmax.asset import FtrackAssetNode
from ftrack_connect_pipeline.asset.asset_info import FtrackAssetInfo
from ftrack_connect_pipeline_3dsmax.utils import custom_commands as max_utils
from ftrack_connect_pipeline_3dsmax.constants import asset as asset_const


class MaxAssetManagerEngine(AssetManagerEngine):
    ftrack_asset_class = FtrackAssetNode
    engine_type = 'asset_manager'

    def __init__(self, event_manager, host, hostid, asset_type=None):
        '''Initialise AssetManagerEngine with *event_manager*, *host*, *hostid*
        and *asset_type*'''
        super(MaxAssetManagerEngine, self).__init__(
            event_manager, host, hostid, asset_type=asset_type
        )

    def discover_assets(self, assets=None, options=None, plugin=None):
        '''
        Discover all the assets in the scene:
        Returns status and result
        '''
        status = constants.UNKNOWN_STATUS

        ftrack_asset_nodes = max_utils.get_ftrack_helpers()
        ftrack_asset_info_list = []

        for ftrack_object in ftrack_asset_nodes:
            obj = ftrack_object.Object
            param_dict = FtrackAssetNode.get_parameters_dictionary(
                ftrack_object
            )
            node_asset_info = FtrackAssetInfo(param_dict)
            ftrack_asset_info_list.append(node_asset_info)

        if not ftrack_asset_info_list:
            status = constants.ERROR_STATUS
        else:
            status = constants.SUCCESS_STATUS
        result = ftrack_asset_info_list

        return status, result

    def remove_asset(self, asset_info, options=None, plugin=None):
        '''
        Removes the given *asset_info* from the scene.
        Returns status and result
        '''
        status = constants.UNKNOWN_STATUS
        result = []

        deleted_nodes = []

        ftrack_asset_object = self.get_ftrack_asset_object(asset_info)

        try:
            # TODO: check if I have to get the object or not needed
            # ftrack_object = ftrack_asset_object.ftrack_object.Object
            deleted_nodes = max_utils.delete_all_children(ftrack_asset_object.ftrack_object)
            status = constants.SUCCESS_STATUS
        except Exception as error:
            self.logger.error('Could not delete nodes, error: {}'.format(error))
            status = constants.ERROR_STATUS

        bool_status = constants.status_bool_mapping[status]
        if not bool_status:
            return status, result

        try:
            ftrack_asset_object.ftrack_object.Delete()
            status = constants.SUCCESS_STATUS
        except Exception as error:
            self.logger.error(
                'Could not delete the ftrack_object, error: {}'.format(error)
            )
            status = constants.ERROR_STATUS

        bool_status = constants.status_bool_mapping[status]
        if not bool_status:
            return status, result
        deleted_nodes.append(ftrack_asset_object.ftrack_object)
        result = deleted_nodes

        return status, result

    def select_asset(self, asset_info, options=None, plugin=None):
        '''
        Selects the given *asset_info* from the scene.
        *options* can contain clear_selection to clear the selection before
        select the given *asset_info*.
        Returns status and result
        '''
        status = constants.UNKNOWN_STATUS
        result = []

        selected_nodes=[]

        ftrack_asset_object = self.get_ftrack_asset_object(asset_info)

        if options.get('clear_selection'):
            max_utils.deselect_all()

        #max_utils.deselect_all()
        try:
            # TODO: check if I have to get the object or not needed
            # ftrack_object = ftrack_asset_class.ftrack_object.Object
            selected_nodes = max_utils.add_all_children_to_selection(
                ftrack_asset_object.ftrack_object
            )
            status = constants.SUCCESS_STATUS
        except Exception as error:
            self.logger.error(
                'Could not delete the ftrack_object, error: {}'.format(error)
            )
            status = constants.ERROR_STATUS

        bool_status = constants.status_bool_mapping[status]
        if not bool_status:
            return status, result

        result = selected_nodes

        return status, result