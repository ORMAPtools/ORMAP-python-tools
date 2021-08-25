"""
Zoom current map or layout to a taxmap extent
implemented as an ArcGIS Python Toolbox

Parameters:
  0 Map_Number        String  Optional Input   Value List
  1 Taxlot            String  Optional Input   Value List
  2 Zoom_now          Boolean Optional Input

Read this!
  https://proceedings.esri.com/library/userconf/devsummit19/papers/DevSummitPS_51.pdf

"""
import os
import arcpy

__version__ = '2021-08-24.4'

class Zoom(object):
    """This class has the methods you need to define
       to use your code as an ArcGIS Python Tool."""
   
    # chose the field to use as a taxmap index
    # in my data, I have mapnumber in every parcel so I use it
    indexfield = 'mapnumber' # has dots like "4.9.27"
    #indexfield = 'pagename' # has spaces and leading zero like "4 09 27"

    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Zoom" + " " + __version__
        self.description = """Zoom the current map to the extent of the specified taxmap."""
        self.canRunInBackground = False
        #self.category = "ORMAP" # Use your own category here, or an existing one.
        #self.stylesheet = "" # I don't know how to use this yet.

        arcpy.AddMessage("Zoom version %s" % __version__)

        # get the current map
        try:
            self.aprx = arcpy.mp.ArcGISProject('CURRENT')
        except OSError as e:
            # FIXME
            aprxfile="C:\\Users\\bwilson\\source\\ORMAP\\ORMAP-ParcelFabric\\ClatsopCounty_NO_PF\\ClatsopCounty_NO_PF.aprx"
            self.aprx = arcpy.mp.ArcGISProject(aprxfile)

        map = self.aprx.activeMap
        if not map:
            map = self.aprx.listMaps('MapView')[0]

        mapindex = map.listLayers('MapIndex')[0]
        datasource = mapindex.dataSource
        connection = mapindex.connectionProperties

        taxlot   = map.listLayers('Taxlots')[0]

        # FIXME
#        workspace = arcpy.env['workspace']
        workspace = "C:\\Users\\bwilson\\source\\ORMAP\\ORMAP-ParcelFabric\\ClatsopCounty_NO_PF\\cc-gis.sde"
        arcpy.AddMessage("Workspace is %s" % workspace)
        self.mapindex_path = os.path.join(workspace, 'Sandbox.DBO.mapindex')
        self.taxlots_path = os.path.join(workspace, 'Sandbox.DBO.taxlots')

        # Load a list of pages
        self.page_list = []
        try:
            n = arcpy.da.TableToNumPyArray(self.mapindex_path, self.indexfield)
            self.page_list = [tuple[0] for tuple in n]
        except Exception as e:
            arcpy.AddMessage("Can't access the data. " + str(e))

             
    def getParameterInfo(self):
        """Define parameter definitions.
Refer to https://pro.arcgis.com/en/pro-app/latest/arcpy/geoprocessing_and_python/defining-parameters-in-a-python-toolbox.htm
        """       
        # params[0] 
        page = arcpy.Parameter(name=self.indexfield,
            displayName="Taxmap page index",
            datatype="GPString",
            parameterType="Optional", # Required|Optional|Derived
            direction="Input" # Input|Output
        )
        page.filter.list = self.page_list
        if len(self.page_list)>0:
            page.value = self.page_list[0]

        # params[1]
        taxlot = arcpy.Parameter(name="taxlot", 
            displayName="Taxlot",
            datatype="GPString",
            parameterType="Optional", # Required|Optional|Derived
            direction="Input", # Input|Output
        )
#        taxlot.filter.list = ['1', '2']
#        taxlot.value = taxlot.filter.list[0]
 
        # params[2]
        zoom_now = arcpy.Parameter(name="zoom_now", 
            displayName="Zoom now",
            datatype="GPBoolean",
            parameterType="Optional", # Required|Optional|Derived
            direction="Input", # Input|Output
        )
        zoom_now.value = True
 
        return [page, taxlot, zoom_now]

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """ This method is called whenever a parameter has been changed."""
        # Did we just get a brand new mapindex feature class?
        #if parameters[1].altered:
        # Yes -- fill in the list
        #    parameters[0].filter.list = ["1", "2", "3"]

        # Did the taxlot number change
        if (parameters[1].altered and parameters[2].value) or (parameters[2].altered and parameters[2].value): 
            # Find the taxlot and possibly change the page index
            try:
                taxlotvalue = parameters[1].ValueAsText
                print("taxlot", taxlotvalue)
                taxmap = self.findtaxmap(taxlotvalue)
                parameters[0].value = taxmap
                print("taxlot zoom!!", taxmap)
                self.zoom(taxmap)
            except Exception as e:
                print("Just na.", e)
            return

        # Did the page index change? Is "zoom now" set?
        #   or
        # Did the "zoom now" flag become True?
        if (parameters[0].altered and parameters[2].value) or (parameters[2].altered and parameters[2].value): 
            try:
                indexvalue = parameters[0].ValueAsText
                print("taxmap zoom!!", indexvalue)
                self.zoom(indexvalue)
            except Exception as e:
                pass

        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        indexvalue = parameters[0].value
        print("zoom!!", indexvalue)
        self.zoom(indexvalue)
        return

    def zoom(self, indexvalue):
        # Do I need to convert a scale to a zoom level?

        try:
            view = self.aprx.activeView
            viewtype = str(type(view))
        except:
            # Possibly we're running a unit test
            # or there is just no active view right now
            arcpy.AddMessage("There is no current view.")
            return

        if 'Layout' in viewtype:
        # This is a Layout
            # Note that this fails if the mapSeries is bookmark based.
            try:
                ms = view.mapSeries
                new_page = ms.getPageNumberFromName(indexvalue)
                print("New page in map series is", new_page)
                ms.currentPageNumber = new_page
                ms.refresh()
            except Exception as e:
                arcpy.AddError("Layout zoom failed with \"%s\"" % e)                
            
            return

        # Assume this is a MapView
        query = "%s='%s'" % (self.indexfield, indexvalue)
        try:
            row = arcpy.da.SearchCursor(self.mapindex_path, ['mapscale', 'SHAPE@'], query).next()
            arcpy.AddMessage("Features selected by \"%s\": %s" % (query, row))
        except Exception as e:
            arcpy.AddMessage("Can't find feature. \"%s\" Error: \"%s\"" % (query, e))
            return

        mapscale = row[0]
        extent   = row[1].extent

        view.camera.setExtent(extent)
        return
    
    def findtaxmap(self, maptaxlot):
        query = "%s='%s'" % ("MapTaxlot", maptaxlot)
        mapnumber = None
        try:
            row = arcpy.da.SearchCursor(self.mapindex_path, ['MapNumber'], query).next()
            arcpy.AddMessage("Features selected by \"%s\": %s" % (query, row))
            mapnumber = row[0]
        except Exception as e:
            arcpy.AddMessage("Can't find that taxmap \"%s\". %s" % (self.mapindex_path, e))

        return mapnumber

# =============================================================================

if __name__ == "__main__":
    
    class Messenger(object):
        def addMessage(self, message):
            print(message)

    egdb = "C:\\Users\\bwilson\\source\\ORMAP\\ORMAP-ParcelFabric\\ClatsopCounty_NO_PF\\cc-gis.sde"
    assert arcpy.Exists(egdb)
    arcpy.env['workspace'] = egdb
    fc = "Clatsop.DBO.mapindex"

    # Get an instance of the tool.
    zoom = Zoom()

    # Read its default parameters.
    params = zoom.getParameterInfo()

    # Set some test values into the instance
    #arcpy.env.workspace = '.\\test_pro\\test_pro.gdb'

    zoom.updateParameters(params)

    # Run it.
    zoom.execute(params, Messenger())

# That's all
