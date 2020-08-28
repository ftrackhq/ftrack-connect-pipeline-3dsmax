# :coding: utf-8
# :copyright: Copyright (c) 2014-2020 ftrack

import MaxPlus


def import_scene_XRef(file_path, options=None):
    '''Import a Max scene file as a Scene XRef asset.'''
    cmd = '''
    scn = xrefs.addNewXRefFile @"{0}"
    scn
    '''.format(file_path)
    eval_max_script(cmd)


def re_import_scene_XRef(file_path, parent_helper_node_name):
    '''Import a Max scene file as a Scene XRef asset and parent it
    under an existing helper ftrack_object.'''
    cmd = '''
    n = getNodeByName "{0}" exact:true
    scn = xrefs.addNewXRefFile @"{1}"
    scn.parent = n
    '''.format(parent_helper_node_name, file_path)
    eval_max_script(cmd)


def import_obj_XRefs(file_path, options=None):
    '''Import all the objects in a Max scene file as Object XRefs and parent
    them under an existing helper ftrack_object.'''
    cmd = '''
    filename = @"{0}"
    xRefObjs = getMAXFileObjectNames filename
    newObjs =  xrefs.addnewXrefObject filename xRefObjs dupMtlNameAction: #autoRename
    select newObjs
    '''.format(file_path)
    eval_max_script(cmd)


def open_scene(file_path, options=None):
    '''Open a Max scene file.'''
    fm = MaxPlus.FileManager
    return fm.Open(file_path, True, True, True, False)


def eval_max_script(cmd):
    '''Evaluate a string using MAXScript.'''
    return MaxPlus.Core.EvalMAXScript(cmd)


def get_unique_node_name(node_name):
    '''Return a unique scene name for the given *nodeName*'''
    unique_node_name = None
    # Max starts naming objects from 001.
    i = 1
    node_fmt_string = node_name + '%03d'
    while True:
        unique_node_name = node_fmt_string % i
        if not MaxPlus.INode.GetINodeByName(unique_node_name):
            return unique_node_name

        i = i + 1

    return unique_node_name


def scene_XRef_imported(ftrack_node):
    '''Check if a Scene XRef exists under the ftrackAssetHelper ftrack_object.'''
    cmd = '''
    result = false
    numSceneRefs = xrefs.getXRefFileCount()
    for i = 1 to numSceneRefs do (
        sceneRef = xrefs.getXrefFile i
        if sceneRef.parent.Name == "{0}" do (
            result = true
        )
    )
    result
    '''.format(ftrack_node.Name)
    return MaxPlus.Core.EvalMAXScript(cmd).Get()


def merge_max_file(file_path, options=None):
    '''Import a Max scene into the current scene.'''
    return eval_max_script(
        'mergemaxfile @"{0}" #autoRenameDups #neverReparent #select'.format(
            file_path))


def get_current_scene_objects():
    deselect_all()
    select_all()
    scene_objects = []
    for obj in save_selection():
        scene_objects.append(obj)
    deselect_all()
    return set(scene_objects)


def select_all():
    eval_max_script('select $*')


def deselect_all():
    MaxPlus.SelectionManager.ClearNodeSelection()


def save_selection():
    return MaxPlus.SelectionManager.GetNodes()


def restore_selection(saved_selection):
    MaxPlus.SelectionManager.SelectNodes(saved_selection)


def add_node_to_selection(node):
    '''Select Node'''
    MaxPlus.SelectionManager.SelectNode(node, False)


def selection_empty():
    return MaxPlus.SelectionManager.GetNodes().GetCount() == 0


def get_ftrack_helpers():
    saved_selection = save_selection()
    cmd = '''
    selected_helpers =  #()
    for obj in rootScene.world.children do (  
        cl = SuperClassOf obj 
        if (cl == Helper) then  ( 
            append selected_helpers obj
            )
    )
    max select none
    select selected_helpers
    '''
    eval_max_script(cmd)
    helpers = MaxPlus.SelectionManager.GetNodes()
    deselect_all()
    restore_selection(saved_selection)
    return helpers


def _collect_children_nodes(n, nodes):
    for c in n.Children:
        _collect_children_nodes(c, nodes)

    nodes.append(n)


def collect_children_nodes(node):
    '''Return a list of all children of a ftrack_object.'''
    child_nodes = []
    for c in node.Children:
        _collect_children_nodes(c, child_nodes)

    return child_nodes


def delete_all_children(node):
    '''Delete all children ftrack_objects of a ftrack_object.'''
    all_children = collect_children_nodes(node)
    nodes_to_delete = MaxPlus.INodeTab()
    for node in all_children:
        nodes_to_delete.Append(node)

    node.DeleteNodes(nodes_to_delete)
    return all_children


def add_all_children_to_selection(parent_node):
    '''Add all children of a ftrack_object to the current selection.'''
    new_sel = MaxPlus.SelectionManager.GetNodes()
    nodes_to_select = collect_children_nodes(parent_node)
    for node in nodes_to_select:
        new_sel.Append(node)

    MaxPlus.SelectionManager.SelectNodes(new_sel)

    return nodes_to_select


def get_time_range():
    start = eval_max_script('animationRange.start')
    end = eval_max_script('animationRange.end')
    return (start, end)


def select_only_cameras():
    cmd = '''
    selected_cameras = #()
    for obj in selection do (
        if SuperClassOf obj == camera do (
            append selected_cameras obj
        )
    )
    max select none
    select selected_cameras
    '''
    eval_max_script(cmd)


def create_selection_set(set_name):
    '''Create a new selection set containing the selected ftrack_objects.'''
    eval_max_script('selectionSets["{0}"] = selection'.format(set_name))