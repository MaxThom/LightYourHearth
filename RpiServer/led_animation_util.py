import time
import time
from rpi_ws281x import Color, PixelStrip, ws
 
def clear(pixels, must_show=True):
    for i in range(pixels.numPixels()):
        pixels.setPixelColor(i, Color(0, 0, 0))
    if (must_show): pixels.show()
    
# Define the wheel function to interpolate between different hues.
def wheel(pos):
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)

# WRGB 
def color_wipe(pixels, isCancelled, wait=0.0, color=(255,255,255, 255), should_clear=False):
    if (should_clear):
        print("TEST")
        clear(pixels)
    for i in range(pixels.numPixels()):
        pixels.setPixelColor(i, Color(color[2], color[1], color[3],  color[0]))
        if (wait != 0.0):
            if (isCancelled()):
                break
            time.sleep(wait)
            pixels.show()
    pixels.show()

# Define rainbow cycle function to do a cycle of all hues.
def rainbow_cycle_successive(pixels, isCancelled, wait=0.1):
    clear(pixels)    
    for i in range(pixels.numPixels()):
        # tricky math! we use each pixel as a fraction of the full 96-color wheel
        # (thats the i / strip.numPixels() part)
        # Then add in j which makes the colors go around per pixel
        # the % 96 is to make the wheel cycle around
        pixels.setPixelColor(i, wheel(((i * 256 // pixels.numPixels())) % 256) )
        if (isCancelled()):
            return
        pixels.show()
        if wait > 0:
            time.sleep(wait)
        if (isCancelled()):
            return
 
def rainbow_cycle(pixels, isCancelled, wait=0.005, loop=0, loop_forever=True):
    clear(pixels)
    if (loop == 0 or loop_forever):
        loop_forever = True

    while (loop_forever):
        for j in range(256): # one cycle of all 256 colors in the wheel
            for i in range(pixels.numPixels()):
                pixels.setPixelColor(i, wheel(((i * 256 // pixels.numPixels()) + j) % 256) )
            if (isCancelled()):
                return
            pixels.show()
            if wait > 0:
                time.sleep(wait)
            if (isCancelled()):
                return
 
def rainbow_colors(pixels, isCancelled, wait=0.05, loop_forever=True):
    clear(pixels)
    while (loop_forever):
        for j in range(256): # one cycle of all 256 colors in the wheel
            for i in range(pixels.numPixels()):
                pixels.setPixelColor(i, wheel(((256 // pixels.numPixels() + j)) % 256) )
            if (isCancelled()):
                return
            pixels.show()
            if wait > 0:
                time.sleep(wait)
            if (isCancelled()):
                    return
 
def brightness_decrease(pixels, isCancelled, wait=0.01, step=1):
    for j in range(int(256 // step)):
        for i in range(pixels.numPixels()):
            c = pixels.getPixelColorRGB(i)
            r = int(max(0, c.r - step))
            g = int(max(0, c.g - step))
            b = int(max(0, c.b - step))
            pixels.setPixelColor(i, Color(r, g, b))
        if (isCancelled()):
            return
        pixels.show()
        if wait > 0:
            time.sleep(wait)
        if (isCancelled()):
            return
 
def blink_color(pixels, isCancelled, blink_time=5, wait=0.5, color=(255,0,0)):
    clear(pixels)
    for i in range(blink_time):
        # blink two times, then wit
        clear(pixels)
        for j in range(2):
            for k in range(pixels.numPixels()):
                # LedStrip is bgr and not rgb  
                pixels.setPixelColor(k, Color(color[2], color[1], color[3],  color[0]))
            if (isCancelled()):
                return
            pixels.show()
            time.sleep(0.08)
            clear(pixels)
            if (isCancelled()):
                return
            time.sleep(0.08)
            if (isCancelled()):
                return
        time.sleep(wait)
        if (isCancelled()):
            return
 
def appear_from_back(pixels, isCancelled, color=(255, 0, 0)):
    clear(pixels)
    for i in range(pixels.numPixels()):
        for j in reversed(range(i, pixels.numPixels())):
            clear(pixels, False)
            # first set all pixels at the begin
            for k in range(i):
                pixels.setPixelColor(k, Color(color[2], color[1], color[3],  color[0]))
            # set then the pixel at position j
            pixels.setPixelColor(j, Color(color[2], color[1], color[3],  color[0]))            
            if (isCancelled()):
                return
            pixels.show()
            time.sleep(0.02)
            if (isCancelled()):
                return
