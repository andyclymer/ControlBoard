
import os
from mojo.extensions import ExtensionBundle


basePath = os.path.dirname(__file__)
extensionPath = os.path.join(basePath, "ControlBoard.roboFontExt")
libPath = os.path.join(basePath, "lib")
htmlPath = os.path.join(basePath, "html")
resourcesPath = os.path.join(basePath, "resources")

B = ExtensionBundle()

B.name = "ControlBoard"
B.version = "0.2b"
B.mainScript = "ControlBoard.py"

B.developer = "Andy Clymer"
B.developerURL = 'http://www.andyclymer.com/'

B.launchAtStartUp = False
B.addToMenu = [{"path" : "ControlBoard.py", "preferredName" : "ControlBoard", "shortKey" : ""}]
B.requiresVersionMajor = '1'
B.requiresVersionMinor = '5'
B.infoDictionary["html"] = True

B.save(extensionPath, libPath=libPath, htmlPath=htmlPath, resourcesPath=resourcesPath, pycOnly=False)

print "Done"