import vanilla
from mojo.events import postEvent, addObserver, removeObserver


class GlyphMarkDemo:
    
    def __init__(self):
        
        self.ledName = "Status Light"
        self.glyph = None
        
        self.w = vanilla.Window((200, 100), "Mark Color")
        self.w.bind("close", self.windowClosed)
        self.w.open()
        
        addObserver(self, "updateMark", "drawInactive")
        addObserver(self, "glyphChanged", "currentGlyphChanged")
        
    def updateMark(self, sender=None):
        if self.glyph:
            if self.glyph.mark:
                postEvent("ControlBoardOutput", name=self.ledName, state="on", value=self.glyph.mark[0:3])
            else:
                postEvent("ControlBoardOutput", name=self.ledName, state="off")
                
    def glyphChanged(self, info):
        self.glyph = info["glyph"]
        self.updateMark()
        
    def windowClosed(self, sender):
        removeObserver(self, "currentGlyphChanged")
        removeObserver(self, "drawInactive")
        postEvent("ControlBoardOutput", name=self.ledName, state="off")
        
        
GlyphMarkDemo()