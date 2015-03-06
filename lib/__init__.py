import os
import site

# Add all of the directories in ./modules as site package directories
extensionPath = os.path.dirname(__file__)
modulesPath = os.path.join(extensionPath, "modules")
for item in os.listdir(modulesPath):
    itemPath = os.path.join(modulesPath, item)
    if os.path.isdir(itemPath):
        site.addsitedir(itemPath)