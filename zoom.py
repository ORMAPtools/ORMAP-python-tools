"""
Zoom the current map to a taxmap, as specified.

@author: Brian Wilson <brian@wildsong.biz>
"""
from collections import namedtuple
import arcpy

__version__ = "2020-07-08.01"
    
def Zoom(taxmap):
    print("Zooming to taxmap: ", taxmap)

    # Look up the taxmap in our Map Series index
    
    # Zoom to the extent of the index.
    
    return


# ======================================================================
# UNIT TESTING
# You can run this file directly when writing it to aid in debugging.
# For example, "Set as Startup File" when running under Visual Studio.

if __name__ == '__main__':
    arcpy.env.workspace = ".\\test_pro\\test_pro.gdb"
    
    arcpy.AddMessage("Version %s" % __version__)
    arcpy.AddMessage("starting geoprocessing")

    map = ""
    mapseriesindex = "MapIndex - DDP INDEX"

    aprx_file = "C:/Users/bwilson/source/repos/ORMap-ParcelFabric/ClatsopCounty_NO_PF/ClatsopCounty_NO_PF.aprx"
    aprx = arcpy.mp.ArcGISProject(aprx_file)
    #mapview = aprx.activeMap
    mapview = aprx.listMaps('MapView')[0]
    view = aprx.activeView
    extent = arcpy.Extent(
        XMin=7328032.0322, YMin=924661.0315,
        XMax=7329032.0322, YMax=925661.0315)
    view.camera.setExtent(extent)
        
    print("zoom tests successful!")

# That's all
