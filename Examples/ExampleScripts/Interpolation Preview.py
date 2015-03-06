from mojo.events import addObserver, removeObserver
from defconAppKit.controls.glyphView import GlyphView
import vanilla


class InterpolationWindow:
    
    def __init__(self):
        
        self.w = vanilla.Window((800, 500), "Interpolation Preview", minSize=(800, 500))
        
        self.fontList = AllFonts()
        self.fontNameList = [font.info.fullName for font in self.fontList]
        self.tempFont = RFont(showUI=False)
        
        self.w.fontChoice0 = vanilla.PopUpButton((20, 20, 160, 25), self.fontNameList, callback=self.interpolate)
        self.w.fontChoice1 = vanilla.PopUpButton((20, 50, 160, 25), self.fontNameList, callback=self.interpolate)
        self.w.interpSlider = vanilla.Slider((20, 90, 160, 25), maxValue=1, callback=self.interpolate)
        self.w.interpValue = vanilla.TextBox((20, 115, 160, 20), "0.95", sizeStyle="small")
        self.w.showOutlinesBox = vanilla.CheckBox((20, 140, 160, 25), "Show Outlines", callback=self.viewChange)
        self.w.preview = GlyphView((200, 0, -0, -0))
        self.w.glyphNameBox = vanilla.EditText((20, 180, 160, 25), "a", callback=self.interpolate)
        self.viewChange(None)
        self.w.bind("close", self.windowClosed)
        self.w.open()
        
        addObserver(self, "controlChanged", "ControlBoardInput")
        
    def controlChanged(self, info):
        if info["name"] == "Interp Value":
            self.w.interpSlider.set(info["value"])
            self.w.interpValue.set(info["value"])
            self.interpolate(None)
        elif info["name"] == "Switch":
            if info["state"] == "down":
                self.w.showOutlinesBox.set(True)
                self.viewChange(None)
            elif info["state"] == "up":
                self.w.showOutlinesBox.set(False)
                self.viewChange(None)
        
        
    def viewChange(self, sender):
        # Change the view options
        p = self.w.preview
        if self.w.showOutlinesBox.get():
            p.setShowFill(False)
            p.setShowStroke(True)
            p.setShowMetrics(True)
            p.setShowMetricsTitles(False)
            p.setShowOnCurvePoints(True)
            p.setShowOffCurvePoints(True)
        else:
            p.setShowFill(True)
            p.setShowStroke(False)
            p.setShowMetrics(False)
            p.setShowMetricsTitles(False)
            p.setShowOnCurvePoints(False)
            p.setShowOffCurvePoints(False)
        self.interpolate(None)
        
    def interpolate(self, sender):
        value = self.w.interpSlider.get()
        self.w.interpValue.set(value)
        name = self.w.glyphNameBox.get()
        if len(self.fontList) > 0:
            font0 = self.fontList[self.w.fontChoice0.get()]
            font1 = self.fontList[self.w.fontChoice1.get()]
            if not False in [name in font0, name in font1]:
                g0 = font0[name]
                g1 = font1[name]
                self.tempFont.newGlyph(name)
                gInterp = self.tempFont[name]
                gInterp.interpolate(value, g0, g1)
                self.w.preview.set(gInterp.naked())

    def windowClosed(self, sender):
        removeObserver(self, "CurrentGlyphChanged")
        removeObserver(self, "ControlBoardInput")


InterpolationWindow()