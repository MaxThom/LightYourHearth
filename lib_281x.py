import time
import math
from random import *
from dataclasses import dataclass


from rpi_ws281x import Color, PixelStrip, ws


# LED strip configuration:
LED_COUNT = 144         # Number of LED pixels.
LED_PIN = 18           # GPIO pin connected to the pixels (must support PWM!).
LED_FREQ_HZ = 800000   # LED signal frequency in hertz (usually 800khz)
LED_DMA = 10           # DMA channel to use for generating signal (try 10)
LED_BRIGHTNESS = 255   # Set to 0 for darkest and 255 for brightest
LED_INVERT = False     # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL = 0
#LED_STRIP = ws.SK6812_STRIP_BRGW
LED_STRIP = ws.SK6812W_STRIP

def clear(pixels, must_show=True):
    for i in range(pixels.numPixels()):
        pixels.setPixelColor(i, Color(0, 0, 0))
    if (must_show): pixels.show()

# Define functions which animate LEDs in various ways.
def colorStraight(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
    strip.show()

# Define functions which animate LEDs in various ways.
def colorWipe(strip, color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)


def theaterChase(strip, color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, color)
            strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, 0)


def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
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


def rainbow(strip, wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)


def rainbowCycle(strip, wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel(((i * 256 // strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)


def theaterChaseRainbow(strip, wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, wheel((i + j) % 255))
            strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, 0)

def color_wipe_cycle(pixels, wait=0.01, color=(255,255,255, 255), fade_step=50):
    count = pixels.numPixels()
    step = count * max(abs(100 - fade_step), 1) / 50
    print(step)
    step_r = color[0] / step
    step_g = color[1] / step
    step_b = color[2] / step
    print(step_r, step_g, step_b)
    for i in range(pixels.numPixels()):
        for j in range(i):
            if (j < i-1):                
                r = int(max(0, color[0] - (i-j) * step_r))
                g = int(max(0, color[1] - (i-j) * step_g))
                b = int(max(0, color[2] - (i-j) * step_b))
                pixels.setPixelColor(j, Color(r, g, b))
            else:
                pixels.setPixelColor(j, Color(color[0],color[1], color[2], color[3]))
        pixels.show()
        time.sleep(wait)

def color_wipe_rainbow(pixels, wait=0.01, fade_step=1, color_step=30):
    count = pixels.numPixels()
    step = count / fade_step
    for k in range(256):
        cycle_color = wheelRGB(((256 // pixels.numPixels() + k*color_step)) % 256) 
        step_r = cycle_color[0] / step
        step_g = cycle_color[1] / step
        step_b = cycle_color[2] / step
        for i in range(pixels.numPixels()):
            for j in range(i):
                if (j < i-1):
                    r = int(max(0, cycle_color[0] - (i-j) * step_r))
                    g = int(max(0, cycle_color[1] - (i-j) * step_g))
                    b = int(max(0, cycle_color[2] - (i-j) * step_b))
                    pixels.setPixelColor(j, Color(r, g, b))
                else:
                    pixels.setPixelColor(j, Color(cycle_color[0], cycle_color[1], cycle_color[2]))
            pixels.show()
            time.sleep(wait)

def color_breathing(pixels, color=(255,0,0,0)):    
    mov_max = 100
    mov_factor = 0.5
    #while (True):
    mov = 0
    while (mov < mov_max):
        time.sleep(0.01)
        print(mov)
        factor = get_mouvement_factor(mov)
        r = int(color[0]*factor)
        g = int(color[1]*factor)
        b = int(color[2]*factor)
        w = int(color[3]*factor)
        print("color ", r, g, b, w)
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, Color(r, g, b, w))
        strip.show()
        mov += mov_factor

def color_breathing_lerp(pixels, color_from=(255,0,0,0), color_to=(0,255,0,0)):    
    mov_max = 100
    mov_factor = 0.25
    while (True):
        mov = 0
        while (mov < mov_max):
            time.sleep(0.01)
            print(mov)
            factor = get_mouvement_factor(mov)
            r = int((color_to[0]-color_from[0])*factor) + color_from[0]
            g = int((color_to[1]-color_from[1])*factor) + color_from[1]
            b = int((color_to[2]-color_from[2])*factor) + color_from[2]
            w = int((color_to[3]-color_from[3])*factor) + color_from[3]
            print("color ", r, g, b, w)
            for i in range(strip.numPixels()):
                strip.setPixelColor(i, Color(r, g, b, w))
            strip.show()
            mov += mov_factor
    
def color_breathing_lerp_rainbow(pixels, color_step=70):    
    mov_max = 125
    mov_factor = 0.2
    while (True):
        last_color = wheelRGB(((256 // pixels.numPixels() + 0*color_step)) % 256) 
        for k in range(1, 256):
            mov = -25
            next_color = wheelRGB(((256 // pixels.numPixels() + k*color_step)) % 256) 
            while (mov < mov_max):
                time.sleep(0.01)
                print(mov)
                factor = get_mouvement_factor(mov)
                r = int((next_color[0]-last_color[0])*factor) + last_color[0]
                g = int((next_color[1]-last_color[1])*factor) + last_color[1]
                b = int((next_color[2]-last_color[2])*factor) + last_color[2]
                print("color ", r, g, b)
                for i in range(strip.numPixels()):
                    strip.setPixelColor(i, Color(r, g, b))
                strip.show()
                mov += mov_factor
            temp = strip.getPixelColorRGB(0)
            last_color = (temp.r, temp.g, temp.b)
            last_color = next_color

def get_mouvement_factor(x):
    print("----------------")
    period = 100 # The higher the slower
    cycles = x / period
    print("cycles ", cycles)
    tau = math.pi * 2
    print("tau ", tau)
    raw_sin_wave = math.sin(cycles*tau)
    print("raw_sin_wave ", raw_sin_wave)
    mouvement_factor = raw_sin_wave / 2 + 0.5
    print("mouvement_factor ", mouvement_factor)
    return mouvement_factor

def appear_from_back(pixels, color=(0, 255, 0, 255), size=3):
    clear(pixels)
    for i in range(int(pixels.numPixels()/size)):
        for j in reversed(range(i*size, pixels.numPixels()-size)):
            clear(pixels, False)
            # first set all pixels at the begin
            for k in range(i*size):
                pixels.setPixelColor(k, Color(color[1], color[2], color[3],  color[0]))
            # set then the pixel at position j
            for l in range(size):
                pixels.setPixelColor(j+l, Color(color[1], color[2], color[3],  color[0]))
            pixels.show()
            time.sleep(0.02)

def fireworks(pixels, size=7, color=(0, 0, 0, 255), is_rainbow=True, number_of_fireworks=5, chance_of_explosion=5, fade_step=20, firework_fade=40):
    color = (color[1], color[2], color[3], color[0])
    if (size % 2 == 0):
        size += 1
    while (True):
        for i in range(pixels.numPixels()):
            c = pixels.getPixelColorRGB(i)
            r = int(max(0, c.r - (c.r / 255 * fade_step)))
            g = int(max(0, c.g - (c.g / 255 * fade_step)))
            b = int(max(0, c.b - (c.b / 255 * fade_step)))
            pixels.setPixelColor(i, Color(r, g, b))
        for i in range(number_of_fireworks):
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
        time.sleep(0.005)

def labyrinth(pixels, wait=0.05, count=5, color=(0,0,255,0), contact_color=(127, 127, 127, 0), turn_chance=2):
    points = []
    points_location = {}
    points_contact = {}
    for i in range(count):
        start = randint(0, pixels.numPixels())
        velocity = randint(0, 1)
        if (velocity == 0):
            velocity = -1
        points.append(Point(start, velocity))

    while (True):
        for i in range(len(points)):
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
            if (points[i].x+points[i].x_v) in points_location:
                points_location[points[i].x+points[i].x_v] += 1
            else:
                points_location[points[i].x+points[i].x_v] = 1
            # Show            
            pixels.setPixelColor(points[i].x, Color(color[0], color[1], color[2], color[3]))
        for key, value in points_location.items():
            if (value > 1):
                points_contact[key] = 1
        for key in list(points_contact.keys()):
            value = points_contact[key]
            pixels.setPixelColor(key, Color(int(contact_color[0]*value), int(contact_color[1]*value), int(contact_color[2]*value), int(contact_color[3]*value)))
            points_contact[key] = round(points_contact[key]-0.05, 2)
            if (points_contact[key]  < 0):
                points_contact.pop(key)

        pixels.show()
        points_location.clear()
        time.sleep(wait)

@dataclass
class Point:
    x: int
    x_v: int
    y: int = 0    
    y_v: int = 0




# Main program logic follows:
if __name__ == '__main__':
    strip = PixelStrip(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL, LED_STRIP)
    # Intialize the library (must be called once before other functions).
    strip.begin()
    colorWipe(strip, Color(0, 0, 0), wait_ms=0)
    print('Press Ctrl-C to quit.')
    while True:
        # Color wipe animations.
        #colorWipe(strip, Color(255, 0, 0))  # Red wipe
        #colorWipe(strip, Color(0, 255, 0))  # Blue wipe
        #colorWipe(strip, Color(0, 0, 255))  # Green wipe
        #colorWipe(strip, Color(0, 0, 0, 255))  # White wipe
        #colorWipe(strip, Color(255, 255, 255))  # Composite White wipe
        #colorWipe(strip, Color(255, 255, 255, 255))  # Composite White + White LED wipe
        # Theater chase animations.
        #theaterChase(strip, Color(127, 0, 0))  # Red theater chase
        #theaterChase(strip, Color(0, 127, 0))  # Green theater chase
        #theaterChase(strip, Color(0, 0, 127))  # Blue theater chase
        #theaterChase(strip, Color(0, 0, 0, 127))  # White theater chase
        #theaterChase(strip, Color(127, 127, 127, 0))  # Composite White theater chase
        #theaterChase(strip, Color(127, 127, 127, 127))  # Composite White + White theater chase
        # Rainbow animations.
        #rainbow(strip)
        #rainbowCycle(strip)
        #theaterChaseRainbow(strip) 
        
        #color_wipe_cycle(strip, 0.01, (60,121,120,0), 50)
        #color_wipe_rainbow(strip, 0.01, 1, 30)
        #color_breathing(strip)
        #color_breathing_lerp(strip)
        #color_breathing_lerp_rainbow(strip)
        #appear_from_back(strip, size=7)
        #fireworks(strip)
        labyrinth(strip)

        