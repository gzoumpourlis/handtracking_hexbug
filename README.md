# Controlling a HexBug robot with hand-tracking (Leap Motion + Arduino + HexBug)

In this project, we control a HexBug robot through hand-tracking, i.e. by translating hand movements to robot movement commands. The required equipment consists of:<br />
-  a **HexBug robot** <br />
-  a **Leap Motion controller** <br />
-  an **Arduino Uno Rev3** <br />
-  an **infrared LED emitter (940nm)** <br />

<p>
  <img src="https://raw.githubusercontent.com/gzoumpourlis/handtracking_hexbug/main/pics/demo.gif" width="600" title="Example: live demo of our project">
</p>

## Overview

The  overview of our project is shown in the following figure:

<p>
  <img src="https://raw.githubusercontent.com/gzoumpourlis/handtracking_hexbug/main/pics/HexBug_Arduino_LeapMotion.png" width="600" title="Overview of the project">
</p>

## Demo

To run the demo, you can execute the following command

```bash
$ python demo_hexbug_leapmotion.py
```

## Credits

The current GitHub repo contains code parts from the following repository.
Credits go to their owners/developers.

Code in `hexbug_spider.h`: https://github.com/xiam/arduino_hexbug_spider <br />
