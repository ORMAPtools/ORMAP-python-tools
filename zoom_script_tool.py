"""
Zoom of current map to a taxmap extent
implemented as an ArcGIS Python Toolbox

Parameters:
  0 Map_Number           String  Required Input   Value List
  1 Zoom_to_Map_Number   Boolean Optional Input
"""
import arcpy
from arcgis.features import FeatureLayer

featureLayerUrl = "https://delta.co.clatsop.or.us/server/rest/services/Hosted/MapIndex/FeatureServer/1"

class ToolValidator(object):
    """This class has the methods you need to define
       to use your code as an ArcGIS Python Tool."""
   
    taxmap = None
    mapindex = None

    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Zoom"
        self.description = """Zoom the current map to the extent of the specified taxmap."""
        self.canRunInBackground = False
        #self.category = "ORMAP" # Use your own category here, or an existing one.
        #self.stylesheet = "" # I don't know how to use this yet.

    # build a list here for the UI
        """ Get a dataframe of features indexed by pagename. """
        layer = FeatureLayer(featureLayerUrl)
        fields = ["pagename", "mapnumber", "mapscale"]
        df = layer.query(where="1=1", out_fields=fields).sdf
        df = df.set_index("pagename")
        self.pagenames = df.index.tolist()

        self.aprx = None
        try:
            self.aprx = arcpy.mp.ArcGISProject("CURRENT")
        except Exception as e:
            print(e)
             

    def getParameterInfo(self):
        """Define parameter definitions.
Refer to https://pro.arcgis.com/en/pro-app/latest/arcpy/geoprocessing_and_python/defining-parameters-in-a-python-toolbox.htm
        """       
        # params[0] 
        self.pagename = arcpy.Parameter(name="pagename",
            displayName="Taxmap page name, for example \"8 10 12\".",
            datatype="GPString",
            parameterType="Required", # Required|Optional|Derived
            direction="Input" # Input|Output
        )
        self.pagename.filter.list = self.pagenames

        # params[1]
        self.zoom_flag = arcpy.Parameter(name="zoomToMapNumber", 
            displayName="Zoom to MapNumber on change",
            datatype=["GPBoolean"],
            parameterType="Optional", # Required|Optional|Derived
            direction="Input", # Input|Output
        )
        self.zoom_flag.value = True
 
        return [self.pagename, self.zoom_flag]

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """ This method is called whenever a parameter has been changed."""
        # Did we just get a brand new mapindex feature class?
        #if parameters[1].altered:
        # Yes -- fill in the list
        #    parameters[0].filter.list = ["1", "2", "3"]

        # Did the pagename change?
        if parameters[0].altered:
            # Yes -- change the extent
            print("zoom!!", parameters[0].value)
            try:
                # Get the extent of this map.
                row = self.df.loc[parameters[0].value]
                self.extent = row.SHAPE.extent
                self.mapscale  = row.mapscale
            except Exception as e:
                print(e)
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        error = self.zoom()
        if error:
            messages.addMessage(error)
        return

    def zoom(self):
        try:
            print(self.extent, self.mapscale)
            # I need to convert a scale to a zoom level somehow here
            camera = self.aprx.activeView.camera
            camera.setExtent(self.extent)
        except Exception as e:
            # unit tests always end up coming through here
            # because there's never a current map or an active view.
            print(e)
            return e
        return None

# =============================================================================

if __name__ == "__main__":
    
    class Messenger(object):
        def addMessage(self, message):
            print(message)

    egdb = "C:/Users/bwilson/source/repos/ORMAP-ParcelFabric/ClatsopCounty_NO_PF/cc-gis.sde"
    assert arcpy.Exists(egdb)
    arcpy.env['workspace'] = egdb
    fc = "Clatsop.DBO.mapindex"

    # Get an instance of the tool.
    zoom = Zoom_tool()

    df = zoom.df
    print(df)
    print(df.index.to_list())

    # Read its default parameters.
    params = zoom.getParameterInfo()

    # Set some test values into the instance
    #arcpy.env.workspace = '.\\test_pro\\test_pro.gdb'
    params[0].value = "8 09 8DC"
    zoom.updateParameters(params)

    # Run it.
    zoom.execute(params, Messenger())

# That's all
