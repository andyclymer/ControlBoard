from mojo.events import postEvent

"""
ControlBoard
    "LED" component demo
"""

# Send "ControlBoardOutput" notifications to board components to change their state.
# The "name" of the LED is the name that's set in the Control Board window.

# To turn an LED on, change its state to "on".
postEvent("ControlBoardOutput", name="My LED", state="on")

# Turn the LED off
postEvent("ControlBoardOutput", name="My LED", state="off")

# If the LED is attached to a pin that's capable of "Pulse Width Modulation",
# which is sometimes noted with the letters "PWM" or a "~" next to the pin number on the board,
# you can also set the brightness when you turn the LED on. Use a "value" between 0 and 1.
postEvent("ControlBoardOutput", name="My LED", state="on", value=0.5)

# A LED can also "toggle" between states, where it will switch between being on or off
postEvent("ControlBoardOutput", name="My LED", state="toggle")

# Or, a LED can blink. This time the "value" is the blinking frequency in milliseconds (1000 = 1 sec)
postEvent("ControlBoardOutput", name="My LED", state="blink", value="500")

