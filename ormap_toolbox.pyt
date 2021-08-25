"""
Python Toolbox for ORMAP map production

@author: Brian Wilson <brian@wildsong.biz>
"""
import arcpy

__version__ = "2021-08-24.0"

# Import all the tool classes that will be included in this toolbox.
#from export_tool import ExportToPDF_tool
from zoom_tool import Zoom

# Uncomment this only if you are actively editing and debugging.
import importlib
import zoom_tool
importlib.reload(zoom_tool)

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of this .pyt file)."""
        self.description = """ORMAP Map Production Tools."""

        self.label = "ORMAP Map Production Tools"
        self.alias = "ORMAPToolbox"  # no special characters including spaces!
        self.description = """ORMAP Map Production Tools"""

        # List of tool classes associated with this toolbox
        self.tools = [
            #ExportToPDF_tool,
            Zoom
        ]

def list_tools():
    toolbox = Toolbox()
    print("toolbox:", toolbox.label)
    print("description:", toolbox.description)
    print("tools:")
    for t in toolbox.tools:
        tool = t()
        print('  ', tool.label)
        print('   description:', tool.description)
        for param in tool.getParameterInfo():
            print('    ',param.name,':',param.displayName)
        print()


if __name__ == "__main__":
    # Running this as a standalone script lists information about the toolbox and each tool.
    # It turns out that it runs when you load the toolbox (or refresh it) in ArcGIS Pro, too.
    print("ormap_toolbox version", __version__)
    list_tools()
    
# That's all!
