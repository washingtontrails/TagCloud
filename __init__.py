from Products.CMFCore.DirectoryView import registerDirectory

from Products.TagCloud.config import GLOBALS, SKINS_DIR
from Products.TagCloud.tool.tagcloud import TagCloudTool

registerDirectory(SKINS_DIR, GLOBALS)
 
from Products.CMFCore.utils import ToolInit

def initialize(context):
    ToolInit(
        'TagCloud Tool',
        tools=(TagCloudTool, ),
        icon='skins/tagcloud_images/cloud_icon.png', ).initialize(context)
