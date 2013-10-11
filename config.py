from Products.CMFCore.permissions import ManagePortal

PROJECTNAME = 'TagCloud'
TOOLNAME = 'tagcloud_tool'
SKINS_DIR = 'skins'

GLOBALS = globals()

LEVELS = 5

CACHE_MANAGER = 'TagCloudCache'
CACHE_MANAGER_SETTINGS = {
    'request_vars'     : ('AUTHENTICATED_USER',),
    'threshold'        : 100,
    'max_age'          : 60,
    'cleanup_interval' : 300,
}

PORTLETS = (
    'here/portlet_tag_cloud_cache',
)

CONFIGLETS = (
   { 'id'         : 'tagcloud'
   , 'name'       : 'Tag Cloud Settings'
   , 'action'     : 'string:${portal_url}/prefs_tagcloud_form'
   , 'condition'  : ''
   , 'category'   : 'Products'    # section to which the configlet should be added:
                                  # (Plone,Products,Members)
   , 'visible'    : 1
   , 'appId'      : PROJECTNAME
   , 'permission' : ManagePortal
   , 'imageUrl'   : 'skins/tagcloud_images/cloud_icon.png'
   },
)

# CHANGE this tuple of python dictionnaries to list the stylesheets that
#  will be registered with the portal_css tool.
#  'id' (required):
#    it must respect the name of the css or DTML file (case sensitive).
#    '.dtml' suffixes must be ignored.
#  'expression' (optional - default: ''): a tal condition.
#  'media' (optional - default: ''): possible values: 'screen', 'print',
#    'projection', 'handheld'...
#  'rel' (optional - default: 'stylesheet')
#  'title' (optional - default: '')
#  'rendering' (optional - default: 'import'): 'import', 'link' or 'inline'.
#  'enabled' (optional - default: True): boolean
#  'cookable' (optional - default: True): boolean (aka 'merging allowed')
#  See registerStylesheet() arguments in
#  ResourceRegistries/tools/CSSRegistry.py
#  for the latest list of all available keys and default values.
STYLESHEETS = (
    {'id': 'tagcloud.css', 'media': 'screen', 'rendering': 'import'},
)

# CHANGE this tuple of python dictionnaries to list the javascripts that
#  will be registered with the portal_javascripts tool.
#  'id' (required): same rules as for stylesheets.
#  'expression' (optional - default: ''): a tal condition.
#  'inline' (optional - default: False): boolean
#  'enabled' (optional - default: True): boolean
#  'cookable' (optional - default: True): boolean (aka 'merging allowed')
#  See registerScript() arguments in ResourceRegistries/tools/JSRegistry.py
#  for the latest list of all available keys and default values.
JAVASCRIPTS = (
#    {'id': 'myjavascript.js.dtml',},
)
