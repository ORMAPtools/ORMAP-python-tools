"""
Python code that implements implements an ArcGIS Tool,
to be included in an ArcGIS Python Toolbox.

@author: Brian Wilson <brian@wildsong.biz>
"""
import os
import arcpy
from export_to_pdf import ExportToPDF

class ExportToPDF_tool(object):
    """This class has the methods you need to define
       to use your code as an ArcGIS Python Tool."""
        
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Export To PDF"
        self.description = """EXport the specified taxmap from the current map
    to a PDF file."""
        self.canRunInBackground = False
        #self.category = "ORMAP" # Use your own category here, or an existing one.
        #self.stylesheet = "" # I don't know how to use this yet.
        
    def getParameterInfo(self):
        """Define parameter definitions.
Refer to https://pro.arcgis.com/en/pro-app/latest/arcpy/geoprocessing_and_python/defining-parameters-in-a-python-toolbox.htm
        """       
        # params[0] 
        taxmap = arcpy.Parameter(name="taxmap",
            displayName="Taxmap code, for example \"8 10 12\".",
            # Using a composite type here means I can 
            # enter either a feature class or a string into the form.
            datatype=["GPString"],
            parameterType="Required", # Required|Optional|Derived
            direction="Input", # Input|Output
        )
        # You can set filters here for example
        #input_fc.filter.list = ["Polygon"]
        # You can set a default if you want -- this makes debugging a little easier.
        taxmap.value = "8 9 10"

        # params[1] 
        output_file = arcpy.Parameter(name="output_file",
            displayName="Output file",
            datatype="DEFile",
            parameterType="Required", # Required|Optional|Derived
            direction="Output", # Input|Output
        )

        return [taxmap, output_file]

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""

        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""

        return

    def execute(self, parameters, messages):
        
        # Let's dump out what we know here.
        for param in parameters:
            messages.addMessage("Parameter: %s = %s" % (param.name, param.valueAsText) )
        
        # Get the parameters from our parameters list,
        # then call a generic python function.
        #
        # This separates the code doing the work from all
        # the crazy code required to talk to ArcGIS.
        
        # See http://resources.arcgis.com/en/help/main/10.2/index.html#//018z00000063000000

        taxmap = parameters[0].valueAsText
        output_file = parameters[1].valueAsText
        
        ExportToPDF(taxmap, output_file)

        return
    
# =============================================================================
if __name__ == "__main__":
    # This is an example of how you could set up a unit test for this tool.
    # You can run this tool from a debugger or from the command line
    # to check it for errors before you try it in ArcGIS.
    
    class Messenger(object):
        def addMessage(self, message):
            print(message)

    # Get an instance of the tool.
    export = ExportToPDF_tool()
    # Read its default parameters.
    params = export.getParameterInfo()

    # Set some test values into the instance
    #arcpy.env.workspace = '.\\test_pro\\test_pro.gdb'
    params[0].value = "8 9 10"
    params[1].value = "bill_and_teds_excellent_taxmap.pdf"

    # Run it.
    export.execute(params, Messenger())

# That's all
