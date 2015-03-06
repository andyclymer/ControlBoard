from mojo.events import postEvent

"""
ControlBoard
    "RGB LED" component demo
"""

# Send "ControlBoardOutput" notifications to board components to change their state.
# The "name" of the RGB LED is the name that's set in the Control Board window.

# To turn a RGB LED on, change its state to "on". It will turn on as a fully bright white:
postEvent("ControlBoardOutput", name="My RGB LED", state="on")

# Turn the RGB LED off
postEvent("ControlBoardOutput", name="My RGB LED", state="off")

# If the legs of the RGB LED are attached to pins that are capable of "Pulse Width Modulation",
# which is sometimes noted with the letters "PWM" or a "~" next to the pin number on the board,
# you can also set the color when you turn the LED on.
# Set the color to a (R, G, B) value:
postEvent("ControlBoardOutput", name="My RGB LED", state="on", value=(1, 0, 0.5))
# Set the color of the LED to a color name:
postEvent("ControlBoardOutput", name="My RGB LED", state="on", value="red")
postEvent("ControlBoardOutput", name="My RGB LED", state="on", value="turquoise")
postEvent("ControlBoardOutput", name="My RGB LED", state="on", value="dark green")
postEvent("ControlBoardOutput", name="My RGB LED", state="on", value="white")
# ...etc.

# A LRGB ED can also "toggle" between states, where it will switch between being on or off.
# Note: Currently, it will only turn the LED completely on to white and off.
postEvent("ControlBoardOutput", name="My RGB LED", state="toggle")

# Or, a LED can blink. This time the "value" is the blinking frequency in milliseconds (1000 = 1 sec)
# Note: Currently, it will only turn the LED completely on to white and off.
postEvent("ControlBoardOutput", name="My RGB LED", state="blink", value="500")

