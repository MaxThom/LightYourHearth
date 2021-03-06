import time
import math
import utilities as Util
from rpi_ws281x import Color, PixelStrip, ws
from random import *

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

def wheelRGB(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return (pos * 3, 255 - pos * 3, 0, 0)
    elif pos < 170:
        pos -= 85
        return (255 - pos * 3, 0, pos * 3, 0)
    else:
        pos -= 170
        return (0, pos * 3, 255 - pos * 3, 0)        

def get_mouvement_factor(x):
    period = 100 # The higher the slower
    cycles = x / period
    tau = math.pi * 2
    raw_sin_wave = math.sin(cycles*tau)
    mouvement_factor = raw_sin_wave / 2 + 0.5
    return mouvement_factor

# WRGB 
def color_wipe(pixels, isCancelled, wait=0.0, color=(255,255,255, 255), should_clear=False):
    if (should_clear):
        clear(pixels)
    for i in range(pixels.numPixels()):
        pixels.setPixelColor(i, Color(color[1], color[2], color[3],  color[0]))
        if (wait != 0.0):
            if (isCancelled()):
                break
            time.sleep(wait)
            pixels.show()
    pixels.show()

def color_pair(pixels, isCancelled, wait=0.0, color1=(255,255,255, 255), color2=(255,255,255, 255), size1=3, size2=3, with_animation=False, fade_step=50):
    clear(pixels)
        
    i = 0
    while i < pixels.numPixels():
        for j in range(i, i+size1):
            pixels.setPixelColor(j, Color(color1[1], color1[2], color1[3],  color1[0]))
        i += size1

        for j in range(i, i+size2):
            pixels.setPixelColor(j, Color(color2[1], color2[2], color2[3],  color2[0]))
        i += size2

        if (isCancelled()):
            return        
    pixels.show()

    if (with_animation):
        step_tuple = (fade_step, fade_step, fade_step, fade_step)
        color1 = tuple(map(lambda i, j: i-j if i - j > 0 else 0, color1, step_tuple)) 
        color2 = tuple(map(lambda i, j: i-j if i - j > 0 else 0, color2, step_tuple))

        while (True):            
            for l in range(pixels.numPixels()):
                i = 0
                while i < pixels.numPixels():
                    for j in range(i, i+size1):
                        pixels.setPixelColor(j, Color(color1[1], color1[2], color1[3]))
                    i += size1

                    for j in range(i, i+size2):
                        pixels.setPixelColor(j, Color(color2[1], color2[2], color2[3]))
                    i += size2

                    if (isCancelled()):
                        return        
            
                c = pixels.getPixelColorRGB(l)
                r = c.r
                if (r > 0): r = int(max(0, c.r + fade_step))
                g = c.g
                if (g > 0): g = int(max(0, c.g + fade_step))
                b = c.b
                if (b > 0): b = int(max(0, c.b + fade_step))                
                
                pixels.setPixelColor(l, Color(r, g, b))
                k = 5
                for j in range(l+1, l+5):
                    if (j < pixels.numPixels()):
                        c = pixels.getPixelColorRGB(j)
                        r = c.r
                        if (r > 0): r = int(max(0, c.r + (fade_step/5 * k)))
                        g = c.g
                        if (g > 0): r = int(max(0, c.g + (fade_step/5 * k)))
                        b = c.b
                        if (b > 0): r = int(max(0, c.b + (fade_step/5 * k)))
                        pixels.setPixelColor(j, Color(r, g, b))
                    k -= 1
                k = 1
                for j in range(l-5, l-1):
                    if (j >= 0):
                        c = pixels.getPixelColorRGB(j)
                        r = c.r
                        if (r > 0): r = int(max(0, c.r + (fade_step/5 * k)))
                        g = c.g
                        if (g > 0): r = int(max(0, c.g + (fade_step/5 * k)))
                        b = c.b
                        if (b > 0): r = int(max(0, c.b + (fade_step/5 * k)))
                        pixels.setPixelColor(j, Color(r, g, b))
                    k += 1

                pixels.show()
                if (isCancelled()):
                    return
                time.sleep(wait)
                if (isCancelled()):
                    return

def color_wipe_cycle(pixels, isCancelled, wait=0.01, color=(255,255,255, 255), fade_step=50, loop_forever=True):
    step = pixels.numPixels() * max(abs(100 - fade_step), 1) / 50
    step_w = color[0] / step
    step_r = color[1] / step
    step_g = color[2] / step
    step_b = color[3] / step
    while (True):
        for i in range(pixels.numPixels()):
            for j in range(i+1):
                if (j < i-1):                
                    w = int(max(0, color[0] - (i-j) * step_w))
                    r = int(max(0, color[1] - (i-j) * step_r))
                    g = int(max(0, color[2] - (i-j) * step_g))
                    b = int(max(0, color[3] - (i-j) * step_b))
                    pixels.setPixelColor(j, Color(r, g, b, w))
                else:
                    pixels.setPixelColor(j, Color(color[1], color[2], color[3],  color[0]))
            pixels.show()
            if (isCancelled()):
                return
            time.sleep(wait)
            if (isCancelled()):
                return
        if (not loop_forever):
            return

def color_wipe_rainbow(pixels, isCancelled, wait=0.01, fade_step=50, color_step=30):
    step = pixels.numPixels() * max(abs(100 - fade_step), 1) / 50
    while (True):
        for k in range(256):
            cycle_color = wheelRGB(((256 // pixels.numPixels() + k*color_step)) % 256) 
            step_r = cycle_color[0] / step
            step_g = cycle_color[1] / step
            step_b = cycle_color[2] / step
            for i in range(pixels.numPixels()):
                for j in range(i+1):
                    if (j < i-1):
                        r = int(max(0, cycle_color[0] - (i-j) * step_r))
                        g = int(max(0, cycle_color[1] - (i-j) * step_g))
                        b = int(max(0, cycle_color[2] - (i-j) * step_b))
                        pixels.setPixelColor(j, Color(r, g, b))
                    else:
                        pixels.setPixelColor(j, Color(cycle_color[0], cycle_color[1], cycle_color[2]))
                pixels.show()
                if (isCancelled()):
                    return
                time.sleep(wait)
                if (isCancelled()):
                    return

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
                pixels.setPixelColor(k, Color(color[1], color[2], color[3],  color[0]))
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
 
def appear_from_back(pixels, isCancelled, color=(0, 255, 0, 255), wait=0.02, size=3):
    clear(pixels)
    while (not isCancelled()):
        for i in range(int(pixels.numPixels()/size)):
            for j in reversed(range(i*size, pixels.numPixels()-size)):
                if (isCancelled()):
                    return
                clear(pixels, False)
                # first set all pixels at the begin
                for k in range(i*size):
                    pixels.setPixelColor(k, Color(color[1], color[2], color[3],  color[0]))
                # set then the pixel at position j
                for l in range(size):
                    pixels.setPixelColor(j+l, Color(color[1], color[2], color[3],  color[0]))
                if (isCancelled()):
                    return
                pixels.show()
                time.sleep(wait)
                if (isCancelled()):
                    return

def theaterChase(pixels, isCancelled, color=(255, 0, 0, 0), wait=0.01, is_rainbow=True):
    if (is_rainbow):
        theaterChaseRainbow(pixels, isCancelled, wait)
        return

    while (True):
        for q in range(3):
            if (isCancelled()):
                return
            for i in range(0, pixels.numPixels(), 3):
                pixels.setPixelColor(i + q, Color(color[1], color[2], color[3],  color[0]))
            pixels.show()
            if (isCancelled()):
                return
            time.sleep(wait)
            if (isCancelled()):
                return
            for i in range(0, pixels.numPixels(), 3):
                pixels.setPixelColor(i + q, 0)

def theaterChaseRainbow(pixels, isCancelled, wait=0.01):
    while (True):
        for j in range(256):
            for q in range(3):
                if (isCancelled()):
                    return
                for i in range(0, pixels.numPixels(), 3):
                    pixels.setPixelColor(i + q, wheel((i + j) % 255))
                pixels.show()
                if (isCancelled()):
                    return
                time.sleep(wait)
                if (isCancelled()):
                    return
                for i in range(0, pixels.numPixels(), 3):
                    pixels.setPixelColor(i + q, 0)

def breathing(pixels, isCancelled, color=(255,0,0,0), move_factor=0.5):    
    mov_max = 100
    mov_factor = move_factor
    while (True):
        mov = 0
        while (mov < mov_max):
            if (isCancelled()):
                return
            time.sleep(0.01)
            if (isCancelled()):
                return
            factor = get_mouvement_factor(mov)
            r = int(color[1]*factor)
            g = int(color[2]*factor)
            b = int(color[3]*factor)
            w = int(color[0]*factor)            
            for i in range(pixels.numPixels()):
                pixels.setPixelColor(i, Color(r, g, b, w))
            pixels.show()
            mov += mov_factor
            if (isCancelled()):
                return

def breathing_lerp(pixels, isCancelled, color_from=(255,0,0,0), color_to=(0,255,0,0), move_factor=0.25):    
    mov_max = 100
    mov_factor = move_factor
    while (True):
        mov = 0
        while (mov < mov_max):
            if (isCancelled()):
                return
            time.sleep(0.01)
            if (isCancelled()):
                return
            factor = get_mouvement_factor(mov)
            r = int((color_to[1]-color_from[1])*factor) + color_from[1]
            g = int((color_to[2]-color_from[2])*factor) + color_from[2]
            b = int((color_to[3]-color_from[3])*factor) + color_from[3]
            w = int((color_to[0]-color_from[0])*factor) + color_from[0]
            for i in range(pixels.numPixels()):
                pixels.setPixelColor(i, Color(r, g, b, w))
            pixels.show()
            mov += mov_factor
            if (isCancelled()):
                return
    
def breathing_rainbow(pixels, isCancelled, color_step=30, move_factor=0.25):    
    mov_max = 125
    mov_factor = move_factor
    while (True):
        last_color = wheelRGB(((256 // pixels.numPixels() + 0*color_step)) % 256) 
        for k in range(1, 256):
            if (isCancelled()):
                return
            mov = -25
            next_color = wheelRGB(((256 // pixels.numPixels() + k*color_step)) % 256) 
            while (mov < mov_max):
                if (isCancelled()):
                    return
                time.sleep(0.01)
                if (isCancelled()):
                    return
                factor = get_mouvement_factor(mov)
                r = int((next_color[0]-last_color[0])*factor) + last_color[0]
                g = int((next_color[1]-last_color[1])*factor) + last_color[1]
                b = int((next_color[2]-last_color[2])*factor) + last_color[2]
                for i in range(pixels.numPixels()):
                    pixels.setPixelColor(i, Color(r, g, b))
                pixels.show()
                mov += mov_factor
                if (isCancelled()):
                    return
            temp = pixels.getPixelColorRGB(0)
            last_color = (temp.r, temp.g, temp.b)

def fireworks(pixels, isCancelled, size=7, color=(0, 0, 0, 255), is_rainbow=True, number_of_fireworks=5, chance_of_explosion=5, fade_step=20, firework_fade=40):
    color = (color[1], color[2], color[3], color[0])
    if (size % 2 == 0):
        size += 1
    while (not isCancelled()):
        for i in range(pixels.numPixels()):
            c = pixels.getPixelColorRGB(i)
            r = int(max(0, c.r - (c.r / 255 * fade_step)))
            g = int(max(0, c.g - (c.g / 255 * fade_step)))
            b = int(max(0, c.b - (c.b / 255 * fade_step)))
            pixels.setPixelColor(i, Color(r, g, b))
        for i in range(number_of_fireworks):
            if (isCancelled()):
                return
            chance = randint(0, 100)            
            if (chance <= chance_of_explosion):
                if (is_rainbow):
                    color = wheelRGB(randint(1, 255))
                where = randint(0, pixels.numPixels())
                pixels.setPixelColor(where, Color(color[1], color[2], color[3],  color[0]))
                for j in range(int(size/2)+1):
                    step = firework_fade * j
                    r = int(max(0, color[0] - (color[0] / 255 * step)))
                    g = int(max(0, color[1] - (color[1] / 255 * step)))
                    b = int(max(0, color[2] - (color[2] / 255 * step)))
                    w = int(max(0, color[3] - (color[3] / 255 * step)))
                    pixels.setPixelColor(where-j, Color(r, g, b, w))
                    pixels.setPixelColor(where+j, Color(r, g, b, w))
        pixels.show()
        if (isCancelled()):
                return
        time.sleep(0.005)
        if (isCancelled()):
                return

def labyrinth(pixels, isCancelled, wait=0.05, count=5, turn_chance=2, color=(0,0,0,255), contact_color=(0, 127, 127, 127)):
    clear(pixels, False)
    points = []
    points_location = {}
    points_contact = {}
    for i in range(count):
        start = randint(0, pixels.numPixels())
        velocity = randint(0, 1)
        if (velocity == 0):
            velocity = -1
        points.append(Util.Point(start, velocity))

    while (not isCancelled()):
        for i in range(len(points)):
            if (isCancelled()):
                return
            # Clear
            if (not points[i].x in points_contact):
                pixels.setPixelColor(points[i].x, Color(0, 0, 0, 0))
            # Next move
            velocity = randint(0, 100)
            if (velocity <= turn_chance):
                points[i].x_v *= -1
            points[i].x += points[i].x_v
            points[i].x %= pixels.numPixels()
            if points[i].x in points_location:
                points_location[points[i].x] += 1
            else:
                points_location[points[i].x] = 1
            if points[i].x+points[i].x_v in points_location:
                points_location[points[i].x+points[i].x_v] += 1
            else:
                points_location[points[i].x+points[i].x_v] = 1
            # Show            
            pixels.setPixelColor(points[i].x, Color(color[1], color[2], color[3], color[0]))
        for key, value in points_location.items():
            if (value > 1):
                points_contact[key] = 1
        for key in list(points_contact.keys()):
            value = points_contact[key]
            pixels.setPixelColor(key, Color(int(contact_color[1]*value), int(contact_color[2]*value), int(contact_color[3]*value), int(contact_color[0]*value)))
            points_contact[key] = round(points_contact[key]-0.05, 2)
            if (points_contact[key]  < 0):
                points_contact.pop(key)

        pixels.show()
        points_location.clear()
        if (isCancelled()):
                return
        time.sleep(wait)

