import arcpy

#This tool uses to layers called MapIndex and Taxlot if your layers 
#do not match this then you should change the names.  They are not 
#variables because that will really slow the application down. (I tried)

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
        mapIndexLayer = Map.listLayers("MapIndex")[0]
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

        def zoomToFeature(featureClass, whereExpression, aprx):
            with arcpy.da.SearchCursor(featureClass, ["shape@"], where_clause=whereExpression) as cursor:
                    for row in cursor:
                            theNewExtent =  row[0].extent
                            theActiveView = aprx.activeView
                            theActiveView.camera.setExtent(theNewExtent)
                    del cursor

        aprx = arcpy.mp.ArcGISProject("CURRENT")
        Map = aprx.activeMap
        taxlotLyr= Map.listLayers("taxlot")[1]
        taxlotLyrDS = taxlotLyr.dataSource


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
               mapIndexLayer = Map.listLayers("MapIndex")[0]
               mapIndexLayerDS = mapIndexLayer.dataSource
               whereClause = "mapnumber ='" + self.params[0].value + "'"
               zoomToFeature(mapIndexLayerDS, whereClause, aprx)
				
        if self.params[1].altered and self.params[3].value and self.params[1].value:
            whereClause = "mapnumber ='" + self.params[0].value + "' and taxlot ='" + self.params[1].value + "'" 
            zoomToFeature(taxlotLyrDS, whereClause, aprx)
            
            
        return
    
    def updateMessages(self):
        """Modify the messages created by internal validation for each tool
        parameter. This method is called after internal validation."""

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True