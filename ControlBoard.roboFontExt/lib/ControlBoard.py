import os
import site

# Add all of the directories in ./modules as site package directories
extensionPath = os.path.dirname(__file__)
modulesPath = os.path.join(extensionPath, "modules")
for item in os.listdir(modulesPath):
    itemPath = os.path.join(modulesPath, item)
    if os.path.isdir(itemPath):
        site.addsitedir(itemPath)

from components import *
import BreakfastSerial as BSer

from mojo.events import addObserver, removeObserver, postEvent
import vanilla
import string



# Board layouts, taken from pyFirata and extended to a few others:



"""

TO DO:

    OVERALL:
        
        "Buzzer" component is just using a LED object for now,
            It turns on and off in the same way, but it would be nice in the future
            to have its own object with some more buzzer-specific methods
        
        Rewrite with the view separate so that it can run without the window open
        
        Import/Export board presets
        
    
    INTERFACE:

        When you choose a different board, have pin lists update? Or must do this on your own?
        
        "Remove" only shows up when item is selected
        
        Add a little console output
            Show all input/outputs rolling by
            Limit to a certain number of lines?
                Or only show the last status for each component?
                If this: then why not just update the list live?


"""
        
        

class ControlBoard:
    
    
    def __init__(self):
        
        # The BreakfastSerial Arudino board object
        self.board = None
        # self.board = BSer.Arduino(port, layout=layoutDict)
        
        # Board layouts, taken from pyFirata and extended to add a few others:
        self.boardLayouts = {
            "Arduino (Standard)": {
                "digital": tuple(x for x in range(14)),
                "analog": tuple(x for x in range(6)),
                "pwm": (3, 5, 6, 9, 10, 11),
                "use_ports": True,
                "disabled": (0, 1)  # Rx, Tx, Crystal
            },
            "Arduino Mega": {
                "digital": tuple(x for x in range(54)),
                "analog": tuple(x for x in range(16)),
                "pwm": tuple(x for x in range(2, 14)),
                "use_ports": True,
                "disabled": (0, 1)  # Rx, Tx, Crystal
            },
            "Arduino Due": {
                "digital": tuple(x for x in range(54)),
                "analog": tuple(x for x in range(12)),
                "pwm": tuple(x for x in range(2, 14)),
                "use_ports": True,
                "disabled": (0, 1)  # Rx, Tx, Crystal
            },
            "Teensy 3.1": {
                "digital": tuple(x for x in range(24)),
                "analog": tuple(x for x in range(15)),
                "pwm": (3, 4, 5, 6, 9, 10, 20, 21, 22, 23),
                "use_ports": True,
                "disabled": (0, 1)  # Rx, Tx, Crystal
            }
        }
        self._boardLayoutNames = self.boardLayouts.keys()
        self._boardLayoutNames.sort()
        
        # Board component types. Name, object, number of pins, pin type
        self.componentTypes = {
            "Output: LED": {"object": ComponentLED, "pinCount": 1, "pinType": "digital"}, 
            "Output: RGB LED": {"object": ComponentRGBLED, "pinCount": 3, "pinType": "digital"},
            "Output: Buzzer": {"object": ComponentLED, "pinCount": 1, "pinType": "digital"},
            "Output: DC Motor": {"object": ComponentMotor, "pinCount": 1, "pinType": "pwm"}, 
            "Output: Servo Motor": {"object": ComponentServo, "pinCount": 1, "pinType": "pwm"}, 
            "Input: Button/Switch": {"object": ComponentButton, "pinCount": 1, "pinType": "digital"}, 
            "Input: Analog Sensor": {"object": ComponentSensor, "pinCount": 1, "pinType": "analog"},
            "Input: Rotary Encoder": {"object": ComponentRotaryEncoder, "pinCount": 2, "pinType": "digital"}}
        self._componentTypeNames = self.componentTypes.keys()
        self._componentTypeNames.sort()
        
        # Board components are configured as a list of dictionaries.
        # The component objects aren't built and initilized with the Arduino until "Apply" is clicked
        self.components = []
        
        
        # ---------- Window ----------
        
        self.w = vanilla.Window((300, 400), 
                "ControlBoard 0.15b", minSize=(300, 350), maxSize=(300, 1000), autosaveName="ControlBoardWindow")
        self.w.bind("close", self._closingWindowCallback)
        
        yPos = 10
        self.w.boardLayoutTitle = vanilla.TextBox((0, yPos+3, 75, 15), 
                "Board Type:", sizeStyle="small", alignment="right")
        self.w.boardLayoutChoice = vanilla.PopUpButton((80, yPos, -10, 20),
                self._boardLayoutNames, sizeStyle="small")
                
        yPos += 25
        self.w.statusTitle = vanilla.TextBox((0, yPos+3, 75, 15), 
                "Status:", sizeStyle="small", alignment="right")
        self.w.statusText = vanilla.TextBox((80, yPos+3, -10, 35),
                "Connecting...", sizeStyle="small")
        self.w.spinner = vanilla.ProgressSpinner((80, yPos+3, 20, 20),
                displayWhenStopped=False)
        self.w.reconnectButton = vanilla.SquareButton((-80, yPos, -10, 25), "Reconnect", sizeStyle="small", callback=self._tryConnecting)
        self.w.reconnectButton.enable(False)
        
        yPos += 40
        self.w.horizLineTop = vanilla.HorizontalLine((5, yPos, -5, 1))
        
        yPos += 10
        self.w.componentTitle = vanilla.TextBox((10, yPos, -100, 25), 
                "Board Components:", sizeStyle="small")
        yPos += 20
        ySplit = -160
        self.w.componentList = vanilla.List((10, yPos, -10, ySplit), 
                [], selectionCallback=self.componentSelected, allowsMultipleSelection=False)

        yPos = ySplit + 10
        self.w.compBox = vanilla.Box((10, yPos, -10, 105))
        self.w.compBox.typeTitle = vanilla.TextBox((5, 10, 40, 25), 
                "Type:", sizeStyle="small", alignment="right")
        self.w.compBox.typeChoice = vanilla.PopUpButton((50, 5, -10, 25), 
                [], sizeStyle="small", callback=self.componentEdited)
        self.w.compBox.typeChoice.enable(False)
        self.w.compBox.nameTitle = vanilla.TextBox((5, 40, 40, 25), 
                "Name:", sizeStyle="small", alignment="right")
        self.w.compBox.componentName = vanilla.EditText((50, 38, 130, 20), 
                "", sizeStyle="small", callback=self.componentEdited, continuous=False)
        self.w.compBox.componentName.enable(False)
        self.w.compBox.pinTitle = vanilla.TextBox((5, 70, 40, 25), 
                "Pin:", sizeStyle="small", alignment="right")
        self.w.compBox.pin1Choice = vanilla.PopUpButton((50, 67, 50, 20), 
                [], sizeStyle="small", callback=self.componentEdited)
        self.w.compBox.pin2Choice = vanilla.PopUpButton((105, 67, 50, 20), 
                [], sizeStyle="small", callback=self.componentEdited)
        self.w.compBox.pin3Choice = vanilla.PopUpButton((160, 67, 50, 20), 
                [], sizeStyle="small", callback=self.componentEdited)
        self.w.compBox.pin1Choice.enable(False)
        self.w.compBox.pin2Choice.enable(False)
        self.w.compBox.pin2Choice.show(False)
        self.w.compBox.pin3Choice.enable(False)
        self.w.compBox.pin3Choice.show(False)
        # @@@ A button to open a help doc about this kind of component?
        #self.w.compBox.infoButton = vanilla.SquareButton((190, 38, -10, 20), "More info", sizeStyle="small")
        #self.w.compBox.infoButton.enable(False)
        
        yPos += 115
        self.w.addButton = vanilla.SquareButton((10, yPos, 120, 25), 
                unichr(0x271a) + " New Component", sizeStyle="small", callback=self.newComponent)
        self.w.addButton.enable(False)
        self.w.removeButton = vanilla.SquareButton((140, yPos, 80, 25), 
                unichr(0x25ac) + " Remove", sizeStyle="small", callback=self.removeComponent)
        self.w.removeButton.enable(False)
        self.w.applyButton = vanilla.SquareButton((230, yPos, -10, 25),
                "Apply", sizeStyle="small", callback=self.applyChanges)
        self.w.applyButton.enable(False)
                
        self.w.open()
        self._tryConnecting(None)
        
        
    
    def updateListContents(self):
        # Rebuild the list of display contents in the Board Components list\
        currentSelection = self.w.componentList.getSelection()
        newList = []
        for component in self.components:
            componentDescription = component["type"] + " " + unichr(0x201c) + component["name"] + unichr(0x201d)
            if component["problem"]:
                componentDescription = "(" + componentDescription + ")"
            newList.append(componentDescription)
        self.w.componentList.set(newList)
        self.w.componentList.setSelection([])
        self.w.componentList.setSelection(currentSelection)
            
    
    def componentSelected(self, sender):
        # An item was selected in the list
        selection = sender.getSelection()
        if selection == []:
            self.setComponentInfo(None)
            self.w.removeButton.enable(False)
        else:
            self.w.removeButton.enable(True)
            idx = sender.getSelection()[0]
            component = self.components[idx]
            self.setComponentInfo(component)
            
    
    def componentEdited(self, sender):
        # An item changed, just update all of the info back to the dict
        idx = self.w.componentList.getSelection()[0]
        # Collect all the info for this component
        thisType = self.w.compBox.typeChoice.getItems()[self.w.compBox.typeChoice.get()]
        thisName = self.w.compBox.componentName.get()
        # Only save the entries for the total number of pins that this component needs
        thisPins = []
        if self.w.compBox.pin1Choice.get() >= 0:
            thisPins.append(self.w.compBox.pin1Choice.getItems()[self.w.compBox.pin1Choice.get()])
        if self.w.compBox.pin2Choice.get() >= 0:
            thisPins.append(self.w.compBox.pin2Choice.getItems()[self.w.compBox.pin2Choice.get()])
        if self.w.compBox.pin3Choice.get() >= 0:
            thisPins.append(self.w.compBox.pin3Choice.getItems()[self.w.compBox.pin3Choice.get()])
        pinCount = self.componentTypes[thisType]["pinCount"]
        thisPins = thisPins[0:pinCount]
        self.components[idx]["type"] = thisType
        self.components[idx]["name"] = thisName
        self.components[idx]["pins"] = thisPins
        self.updateListContents()
        # ALlow for updating:
        self.w.applyButton.enable(True)
        

    def setComponentInfo(self, component=None):
        # Set the Component Info box
        if component == None:
            self.w.compBox.pinTitle.set("Pin:")
            self.w.compBox.typeChoice.enable(False)
            self.w.compBox.componentName.enable(False)
            self.w.compBox.pin1Choice.enable(False)
            self.w.compBox.pin2Choice.enable(False)
            self.w.compBox.pin2Choice.show(False)
            self.w.compBox.pin3Choice.enable(False)
            self.w.compBox.pin3Choice.show(False)
            #self.w.compBox.infoButton.enable(False)
            self.w.compBox.typeChoice.setItems([])
            self.w.compBox.componentName.set("")
            self.w.compBox.pin1Choice.setItems([])
            self.w.compBox.pin2Choice.setItems([])
            self.w.compBox.pin3Choice.setItems([])
        else:
            self.w.compBox.pinTitle.set("Pin:")
            self.w.compBox.typeChoice.enable(True)
            self.w.compBox.componentName.enable(True)
            #self.w.compBox.infoButton.enable(True)
            self.w.compBox.typeChoice.setItems(self._componentTypeNames)
            self.w.compBox.typeChoice.set(self._componentTypeNames.index(component["type"]))
            self.w.compBox.componentName.set(component["name"])
            # Start without any pins filled in, and only enable as many as needed
            self.w.compBox.pin1Choice.enable(False)
            self.w.compBox.pin2Choice.enable(False)
            self.w.compBox.pin2Choice.show(False)
            self.w.compBox.pin3Choice.enable(False)
            self.w.compBox.pin3Choice.show(False)
            self.w.compBox.pin1Choice.setItems([])
            self.w.compBox.pin2Choice.setItems([])
            self.w.compBox.pin3Choice.setItems([])
            totalPins = self.componentTypes[component["type"]]["pinCount"]
            # Set the pins in the interface
            # Pull all of the pins out to a list
            pinList = ["", "", ""]
            for i, pin in enumerate(component["pins"]):
                pinList[i] = pin
            # Find a list of pins that match this component type
            availablePinList = self.getPinList(component["type"])
            if totalPins >= 1:
                self.w.compBox.pin1Choice.setItems(availablePinList)
                self.w.compBox.pin1Choice.enable(True)
                self.w.compBox.pin1Choice.show(True)
                thisPin = pinList[0]
                if thisPin in availablePinList:
                    self.w.compBox.pin1Choice.set(availablePinList.index(thisPin))
            if totalPins >= 2:
                self.w.compBox.pinTitle.set("Pins:")
                self.w.compBox.pin2Choice.setItems(availablePinList)
                self.w.compBox.pin2Choice.enable(True)
                self.w.compBox.pin2Choice.show(True)
                thisPin = pinList[1]
                if thisPin in availablePinList:
                    self.w.compBox.pin2Choice.set(availablePinList.index(thisPin))
            if totalPins >= 3:
                self.w.compBox.pin3Choice.setItems(availablePinList)
                self.w.compBox.pin3Choice.enable(True)
                self.w.compBox.pin3Choice.show(True)
                thisPin = pinList[2]
                if thisPin in availablePinList:
                    self.w.compBox.pin3Choice.set(availablePinList.index(thisPin))
                
    
    def getPinList(self, componentType):
        # Get a pin list, and turn the list to string
        pinList = [""]
        boardLayout = self.boardLayouts[self._boardLayoutNames[self.w.boardLayoutChoice.get()]]
        pinType = self.componentTypes[componentType]["pinType"]
        pinsByType = boardLayout[pinType]
        for pin in pinsByType:
            pinName = str(pin)
            if pinType == "analog":
                pinName = "A" + pinName
            # @@@ Removing this for now:
            #elif pin in boardLayout["pwm"]:
            #    pinName += " ~"
            pinList.append(pinName)
        return pinList
            
        
    def newComponent(self, sender):
        # Add a new component
        self.components.append(
            {"type": self._componentTypeNames[0], 
            "name": 
            "My Component", 
            "pins": ["", "", ""], 
            "object": None,
            "problem": True})
        self.updateListContents()
        
        
    def removeComponent(self, sender):
        # Remove a component
        selection = self.w.componentList.getSelection()
        if not selection == []:
            idx = selection[0]
            del(self.components[idx])
            self.updateListContents()
        self.w.applyButton.enable(True)
            
    
    def applyChanges(self, sender):
        # Apply any changes to board components
        # @@@ This is still a bit of a hack,
        # @@@ ...only creating component objects if it's using unused pins
        usedPins = [""]
        for component in self.components:
            # Stop the component
            if component["object"]:
                component["object"].stop()
            # Initialize a new object for this component
            objectClass = self.componentTypes[component["type"]]["object"]
            pinCount = self.componentTypes[component["type"]]["pinCount"]
            component["problem"] = False
            for pinIdx in range(pinCount):
                if component["pins"][pinIdx] in usedPins:
                    component["pins"][pinIdx] = ""
                    component["problem"] = True
                    component["object"] = None
            if not component["problem"]:
                usedPins += component["pins"][0:pinCount]
                component["object"] = objectClass(self.board, component["pins"], component["name"])
        # Finished applying changes...
        self.w.applyButton.enable(False)
        self.updateListContents()
                 
    
    def _closingWindowCallback(self, sender):
        self.w.unbind("close", self._closingWindowCallback)
        # Stop all component objects from observing notifications
        for component in self.components:
            if component["object"]:
                component["object"].stop()
        # Stop monitoring the board
        if self.board:
            self._stopBoard(None)
    
    
    
    # ---------- Board Callbacks ----------
    
    def _tryConnecting(self, sender):
        
        
        # Stop the current board, if one was already connected
        self._stopBoard()
        
        # Try connecting to a board
        self.w.statusText.show(False)
        self.w.addButton.enable(False)
        #self.w.spinner.start()
        self.board = None
        layoutName = self._boardLayoutNames[self.w.boardLayoutChoice.get()]
        layoutDict = self.boardLayouts[layoutName]

        try:
            self.board = BSer.Arduino(layout=layoutDict)
            if self.board:
                self.w.statusText.set("Connected!\n" + self.board.name) 
                self.w.addButton.enable(True)
                # If there were components alrady set up, enable the "Apply" button
                if self.components:
                    self.w.applyButton.enable(True)
            else:
                self.w.statusText.set("Couldn't find board...")
            
        except BSer.FirmataNotOnBoardException:
            self.w.statusText.set("Firmata not found.\nReset Arduino and try again.")
            
        except BSer.ArduinoNotFoundException:
            self.w.statusText.set("Board not found!\nIs it plugged in?")

        #self.w.spinner.stop()
        self.w.statusText.show(True)
        self.w.reconnectButton.enable(True)
        
        
            
    
    def _stopBoard(self, sender=None):
        # Stop monitoring the board
        if self.board:
            self.board._monitor.stop()
            # ...and kill the serial connection
            self.board.exit()
        
    
        
        

ControlBoard()

