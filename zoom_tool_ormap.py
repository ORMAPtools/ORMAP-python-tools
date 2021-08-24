"""
Zoom of current map to a taxmap extent

This tool uses to layers called MapIndex and Taxlot if your layers 
do not match this then you should change the names using the variables on 
lines below

Parameters:
  0 Map_Number           String  Required Input   Value List
  1 Tax_Lot              String  Optional Input
  2 Zoom_to_Map_Number   Boolean Optional Input
  3 Zoom_to_Tax_Lot      Boolean Optional Input
  4 Apply_Map_Filter     Boolean Optional Input
  5 Filter_Status        String  Derived  Output  EMPTY
  6 Filter_Layers       [String] Optional Input   Value List
  7 Map_Index            String  Optional Output  Mapindex
  8 Taxlots              String  Optional Output  Taxlot
"""
import arcpy

MapIndex = "MapIndex" 
Taxlot = "Taxlot" 
    
class ToolValidator(object):
    """Class for validating a tool's parameter values and controlling
    the behavior of the tool's dialog."""
    
    def __init__(self):
        """Setup arcpy and the list of tool parameters."""
        import arcpy
        self.params = arcpy.GetParameterInfo()

    def initializeParameters(self):
        """Refine the properties of a tool's parameters.
        This method is called when the tool is opened."""

        mapNumberList = []
        aprx= arcpy.mp.ArcGISProject("CURRENT")
        Map = aprx.activeMap
        """mapIndexLayer = Map.listLayers(self.params[4].value)[0]"""
        mapIndexLayer = Map.listLayers(MapIndex)[0]
        mapIndexLayerDS = mapIndexLayer.dataSource
        with arcpy.da.SearchCursor(mapIndexLayerDS, "mapnumber") as cursor:
            for row in cursor:
                if row[0] not in mapNumberList:
                    mapNumberList.append(row[0])
        mapNumberList.sort()
        self.params[0].filter.list = mapNumberList
        
        return
    
    def updateParameters(self):
        """Modify the values and properties of parameters before internal
        validation is performed. This method is called whenever a parameter
        has been changed."""

        aprx = arcpy.mp.ArcGISProject("CURRENT")
        Map = aprx.activeMap
        taxlotLyr= Map.listLayers(Taxlot)[1]
        taxlotLyrDS = taxlotLyr.dataSource
        
        def zoomToFeature(featureClass, whereExpression, aprx):
            aprx = arcpy.mp.ArcGISProject("CURRENT")
            with arcpy.da.SearchCursor(featureClass, ["shape@"], where_clause=whereExpression) as cursor:
                    for row in cursor:
                            theNewExtent =  row[0].extent
                            theActiveView = aprx.activeView
                            if theActiveView != None: 
                                theActiveView.camera.setExtent(theNewExtent)
                    del cursor

        ## If the Map Number parameter is alter this code is executed to provide the values list for parameter 2.
        if self.params[0].altered: 
            taxlotList = [" "]
            whereClause = "mapnumber ='" + self.params[0].value + "'"
            with arcpy.da.SearchCursor(taxlotLyrDS, ["mapnumber","taxlot"], where_clause=whereClause) as cursor:
                for row in cursor:
                    if row[1] not in taxlotList:
                        taxlotList.append(row[1])
                del cursor,row
            taxlotList.sort()
            self.params[1].filter.list = taxlotList           
            if self.params[1].value not in taxlotList:
                self.params[1].value = " " 
            if self.params[0].altered and self.params[2].value:
               """ mapIndexLayer = Map.listLayers(self.params[4].value)[0]"""
               mapIndexLayer = Map.listLayers(MapIndex)[0]
               mapIndexLayerDS = mapIndexLayer.dataSource
               whereClause = "mapnumber ='" + self.params[0].value + "'"
               zoomToFeature(mapIndexLayerDS, whereClause, aprx)
            if self.params[4].value: 
                filterTable = self.params[5].value
                filterList = filterTable.exportToString()
                filterList = filterList.split(";")
                for layerName in filterList:
                    LayerList = Map.listLayers(layerName)
                    TableList = Map.listTables(layerName)
                    for filterlayer in LayerList: 
                        if filterlayer.isFeatureLayer:
                            filterlayer.definitionQuery = whereClause        
                            break
                    for filtertable in TableList: 
                        filtertable.definitionQuery = whereClause        
                        break 
        if  self.params[6].altered and self.params[6].value:
            filterTable = self.params[5].value
            filterList = filterTable.exportToString()
            filterList = filterList.split(";")
            for layerName in filterList:
                LayerList = Map.listLayers(layerName)
                TableList = Map.listTables(layerName)
                for filterlayer in LayerList: 
                    if filterlayer.isFeatureLayer:
                        filterlayer.definitionQuery = None        
                        break
                for filtertable in TableList: 
                    filtertable.definitionQuery = None        
                    break
            self.params[5].value = None
            self.params[4].value = False
            self.params[6].value = False          
				
        if self.params[1].altered and self.params[3].value and self.params[1].value:
            TaxwhereClause = "mapnumber ='" + self.params[0].value + "' and taxlot ='" + self.params[1].value + "'" 
            zoomToFeature(taxlotLyrDS, TaxwhereClause, aprx)
            
            
        return
    
    def updateMessages(self):
        """Modify the messages created by internal validation for each tool
        parameter. This method is called after internal validation."""

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True