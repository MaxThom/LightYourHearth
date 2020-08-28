import led_animation_util as LedUtil
import utilities as Util
import threading
import time
from rpi_ws281x import Color, PixelStrip, ws
import pprint
import constants
from PIL import ImageColor

class Ledstrip:
    def __init__(self):
        self.onGoingTask = None
        self.cancelTask = False
        self.brightness = constants.LED_BRIGHTNESS
        self.pixels = PixelStrip(constants.LED_COUNT, constants.LED_PIN, constants.LED_FREQ_HZ, constants.LED_DMA, constants.LED_INVERT, constants.LED_BRIGHTNESS, constants.LED_CHANNEL, constants.LED_STRIP)
        self.pixels.begin()
        LedUtil.clear(self.pixels)
        self.pixels.setPixelColor(0, Color(255, 255, 255, 255))
        self.pixels.show()
        
        print("Controlling ledstrip on pin ", constants.LED_PIN)

    def pixel_rainbow_colors(self, args):
        wait, isFloat = Util.floatTryParse(args["wait"])
        if (isFloat):
            self.__execute_task(LedUtil.rainbow_colors, (self.pixels, lambda: self.cancelTask, wait))

    def pixel_rainbow_cycle(self, args):
        loop_forever, isBool = Util.boolTryParse(args["loop_forever"])
        wait, isFloat = Util.floatTryParse(args["wait"])
        loop, isInt = Util.intTryParse(args["loop"])
        if (isBool and isFloat and isInt):
            self.__execute_task(LedUtil.rainbow_cycle, (self.pixels, lambda: self.cancelTask, wait, loop, loop_forever))

    def pixel_rainbow_cycle_successive(self, args):
        wait, isFloat = Util.floatTryParse(args["wait"])
        if (isFloat):
            self.__execute_task(LedUtil.rainbow_cycle_successive, (self.pixels, lambda: self.cancelTask, wait))

    def pixel_brightness_decrease(self, args):
        wait, isFloat = Util.floatTryParse(args["wait"])
        step, isInt = Util.intTryParse(args["step"])
        if (isFloat and isInt):
            self.__execute_task(LedUtil.brightness_decrease, (self.pixels, lambda: self.cancelTask, wait, step))

    def pixel_blink_color(self, args):
        color, isColor = Util.colorTryParse(args["color"])
        wait, isFloat = Util.floatTryParse(args["wait"])
        blink_time, isInt = Util.intTryParse(args["blink_time"])
        if (isColor and isFloat and isInt):
            self.__execute_task(LedUtil.blink_color, (self.pixels, lambda: self.cancelTask, blink_time, wait, color))

    def pixel_appear_from_back(self, args):
        color, isColor = Util.colorTryParse(args["color"])
        if (isColor):
            self.__execute_task(LedUtil.appear_from_back, (self.pixels, lambda: self.cancelTask, color))
        
    def pixel_color_wipe(self, args):
        color, isColor = Util.colorTryParse(args["color"])
        wait, isFloat = Util.floatTryParse(args["wait"])
        if (isColor and isFloat):
            self.__execute_task(LedUtil.color_wipe, (self.pixels, lambda: self.cancelTask, wait, color))        

    def set_brightness(self, args):
        brightness, isInt = Util.intTryParse(args["brightness"])
        if (isInt):
            self.brightness = brightness
            self.pixels.setBrightness(brightness)
            self.pixels.show()

    def set_settings(self, args):
        self.__cancel_task()
        self.led_type = args["led_type"]
        self.led_count = int(args["led_pixel_count"])
        ledType = constants.LED_STRIP
        if (self.led_type == constants.LED_STRIP_SK6812):
            ledType = ws.SK6812_STRIP_RGBW
        elif (self.led_type == constants.LED_STRIP_WS2811):
            ledType = ws.WS2811_STRIP_RGB
        elif (self.led_type == constants.LED_STRIP_WS2812B):
            ledType = ws.WS2811_STRIP_RGB

        self.pixels = PixelStrip(self.led_count, constants.LED_PIN, constants.LED_FREQ_HZ, constants.LED_DMA, constants.LED_INVERT, self.brightness, constants.LED_CHANNEL, ledType)
        self.pixels.begin()

    def pixel_off(self, args):
        self.__cancel_task()
        LedUtil.clear(self.pixels)
        self.pixels.show()

    def __execute_task(self, task, args):
        self.__cancel_task()
        self.onGoingTask = threading.Thread(target=task, args=args)
        self.onGoingTask.start()

    def __cancel_task(self):
        if (self.onGoingTask != None):
            self.cancelTask = True
            self.onGoingTask.join()
            self.cancelTask = False
            

        