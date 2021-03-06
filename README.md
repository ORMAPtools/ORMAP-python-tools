# ORMAP-python-tools
ArcGIS Python Toolbox for ORMAP

Tested with ArcGIS Pro 2.8.2 / Python 3.7.10

## To do

Currently there are a bunch of hardcodes tying the zoom tool
to Clatsop County and me (bwilson). These obviously need to be 
removed.

## Files

**ormap_toolbox.pyt** - This is the Python toolbox; it will show up in ArcGIS as a toolbox.

**print_tool.py** - Exports a taxmap as a PDF.

**zoom_tool.py** - Changes the extent in the current map to a taxmap.

**hello_toolbox.pyt** - Demo python toolbox

There are currently some other files in the repo that got pulled
along from earlier work done by other people including zoom_script_tool.py and zoom_tool_ormap.py.

### Zoom

Taxmap page index -- zoom current map to taxmap

There is an option set by default, "Zoom now". When it's set,
you select a page and the map should immediately zoom.

If you turn off "Zoom now" then the map zoom won't happen until you click on the "Run" button.

Taxlot number -- This is not working yet.

#### Debugging

Currently the zoom tool is set up to redirect "print" output to a file C:\TEMP\zoom.txt and I normally run "tail -f zoom.out" in a bash shell to watch it as the tool executes. arcpy.AddMessage
does not help because the messages are only visible when the tool
completes, and since you don't have to Run the tool it will never
generate a message log...

## Unit Tests

There is a unit test in each python file. This means you can develop the code in that file independently, running it in a debugger and confirming it does what you expect before putting together all the pieces.

So for example, you can start by testing zoom_tool.py,
and then run ormap_toolbox.pyt as a standalone script.

Of course, you could run each from a command line, but you can run it in Visual Studio Code and watch its operation in the debugger, executing one line at a time.

## Visual Studio Code

I use Visual Studio Code to develop and test Python. It's free and has excellent code completion ("Intellisense") and debugging. Therefore I have added the associated launch.json file in .vscode to this repository.

### ArcGIS Pro set up

I followed some suggestions found [here, in GIS Stackexchange.](https://gis.stackexchange.com/questions/203380/setting-up-python-arcpy-with-arcgis-pro-and-visual-studio/356487#356487)
In ArcGIS Pro, clone the default Python environment. I renamed the clone arcgispro-py3-vscode. Then make the clone the default in ArcGIS Pro.
Use the cloned environment in Visual Studio Code, adding any additional packages
to the clone.

### Editing and testing PYT files in VSCODE

ArcGIS recognizes PYT files as Python Toolboxes. Add the .pyt extension to VS Code so that it treats them as python code instead of text.

Under File->Preferences->Settings->Files->Associations
I add *.pyt: python.

### Selecting Python version

Set the version using Ctl-Shift-P Python: Select interpreter.
When you want to test with a different version of Python you will have to do
this again.

### Customizing the Quick Access ribbon

https://pro.arcgis.com/en/pro-app/latest/help/analysis/geoprocessing/basics/customize-arcgis-pro-with-geoprocessing-tools.htm

## Resources

*I need to update this section, send suggestions.*

### Esri

May 2018 video: [Buillding Geoprocessing Tools With Python: Getting Started](https://www.youtube.com/watch?v=iTZytnBcagQ)

[Defining parameter data types in a python toolbox](https://desktop.arcgis.com/en/arcmap/latest/analyze/creating-tools/defining-parameter-data-types-in-a-python-toolbox.htm)

[Controlling the progress dialog box](https://desktop.arcgis.com/en/arcmap/latest/analyze/creating-tools/controlling-the-progress-dialog-box.htm)

