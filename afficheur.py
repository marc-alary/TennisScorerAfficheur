from machine import Pin
from neopixel import NeoPixel
from time import sleep, sleep_ms

class Afficheur7Segments:
    def __init__(self, segment_pins, segment_leds=8):
        self.segment_labels = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
        self.segments = {
            label: NeoPixel(Pin(pin, Pin.OUT), segment_leds)
            for label, pin in zip(self.segment_labels, segment_pins)
        }
        self.segment_leds = segment_leds
        self.total_leds = segment_leds * len(self.segment_labels)

        self.char_map = {
            '0': [1,1,1,1,1,1,0], '1': [0,1,1,0,0,0,0], '2': [1,1,0,1,1,0,1],
            '3': [1,1,1,1,0,0,1], '4': [0,1,1,0,0,1,1], '5': [1,0,1,1,0,1,1],
            '6': [1,0,1,1,1,1,1], '7': [1,1,1,0,0,0,0], '8': [1,1,1,1,1,1,1],
            '9': [1,1,1,1,0,1,1], 'o': [0,0,1,1,1,0,1], 'c': [0,0,0,1,1,0,1],
            'u': [0,0,1,1,1,0,0], '-': [0,0,0,0,0,0,1], 'n': [0,0,1,0,1,0,1],
            'U': [0,1,1,1,1,1,0]
        }

        self.couleurs_rgb = {
            "red": (255, 0, 0), "green": (0, 255, 0), "blue": (0, 0, 255),
            "pink": (255, 0, 255), "yellow": (255, 120, 0), "cyan": (0, 255, 255),
            "purple": (160, 32, 240), "orange": (255, 165, 0), "black": (0,0,0),
            "default": (255, 0, 0)
        }

    def _get_segment_and_index(self, number):
        number -= 1
        if number < 0 or number >= self.total_leds:
            return None, None
        segment_index = number // self.segment_leds
        led_index = number % self.segment_leds
        label = self.segment_labels[segment_index]
        return label, led_index

    def led_on(self, number, color, luminosity):
        color = self.couleurs_rgb.get(color, self.couleurs_rgb["default"])
        luminosity = max(0, min(luminosity, 100))
        scaled_color = tuple(int(c * luminosity / 100) for c in color)

        seg, idx = self._get_segment_and_index(number)
        if seg:
            self.segments[seg][idx] = scaled_color
            self.segments[seg].write()

    def led_off(self, number):
        seg, idx = self._get_segment_and_index(number)
        if seg:
            self.segments[seg][idx] = (0, 0, 0)
            self.segments[seg].write()

    def segment_on(self, number, color, luminosity):
        start = (number - 1) * self.segment_leds + 1
        for i in range(start, start + self.segment_leds):
            self.led_on(i, color, luminosity)

    def segment_off(self, number):
        start = (number - 1) * self.segment_leds + 1
        for i in range(start, start + self.segment_leds):
            self.led_off(i)

    def afficheur_off(self):
        for i in range(1, len(self.segment_labels) + 1):
            self.segment_off(i)

    def afficheur_set(self, symbol, color, luminosity):
        pattern = self.char_map.get(symbol.lower(), [0] * 7)
        for i, val in enumerate(pattern):
            if val:
                self.segment_on(i + 1, color, luminosity)
            else:
                self.segment_off(i + 1)

    # -------- Méthodes supplémentaires --------
    def raw_on(self, y, color, luminosity):
        if y == 1:
            self.segment_on(1, color, luminosity)
        elif 1 < y < 10:
            self.led_on(y + 7, color, luminosity)
            self.led_on(50 - y, color, luminosity)
        elif y == 10:
            self.segment_on(7, color, luminosity)
        elif 10 < y < 19:
            self.led_on(y + 6, color, luminosity)
            self.led_on(51 - y, color, luminosity)
        elif y == 19:
            self.segment_on(4, color, luminosity)

    def raw_off(self, y):
        if y == 1:
            self.segment_off(1)
        elif 1 < y < 10:
            self.led_off(y + 7)
            self.led_off(50 - y)
        elif y == 10:
            self.segment_off(7)
        elif 10 < y < 19:
            self.led_off(y + 6)
            self.led_off(51 - y)
        elif y == 19:
            self.segment_off(4)

    def column_on(self, x, color, luminosity):
        if x == 1:
            self.segment_on(5, color, luminosity)
            self.segment_on(6, color, luminosity)
        elif 1 < x < 10:
            self.led_on(x - 1, color, luminosity)
            self.led_on(47 + x, color, luminosity)
            self.led_on(34 - x, color, luminosity)
        elif x == 10:
            self.segment_on(2, color, luminosity)
            self.segment_on(3, color, luminosity)

    def column_off(self, x):
        if x == 1:
            self.segment_off(5)
            self.segment_off(6)
        elif 1 < x < 10:
            self.led_off(x - 1)
            self.led_off(47 + x)
            self.led_off(34 - x)
        elif x == 10:
            self.segment_off(2)
            self.segment_off(3)

    def diag45_on(self, number, color, luminosity):
        if 1 <= number <= 8:
            self.led_on(number, color, luminosity)
            self.led_on(49 - number, color, luminosity)
        elif 8 < number < 17:
            self.led_on(number, color, luminosity)
            self.led_on(40 + number, color, luminosity)
            self.led_on(49 - number, color, luminosity)
        elif 17 <= number <= 24:
            self.led_on(number, color, luminosity)
            self.led_on(49 - number, color, luminosity)

    def diag45_off(self, number):
        if 1 <= number <= 8:
            self.led_off(number)
            self.led_off(49 - number)
        elif 8 < number < 17:
            self.led_off(number)
            self.led_off(40 + number)
            self.led_off(49 - number)
        elif 17 <= number <= 24:
            self.led_off(number)
            self.led_off(49 - number)

    def diag270_on(self, number, color, luminosity):
        if 1 <= number <= 8:
            self.led_on(number, color, luminosity)
            self.led_on(49 - number, color, luminosity)
        elif 8 < number < 17:
            self.led_on(number, color, luminosity)
            self.led_on(40 + number, color, luminosity)
            self.led_on(49 - number, color, luminosity)
        elif 17 <= number <= 24:
            self.led_on(number, color, luminosity)
            self.led_on(49 - number, color, luminosity)


    def diag270_off(self, number):
        if 1 <= number <= 8:
            self.led_off(number)
            self.led_off(49 - number)
        elif 8 < number < 17:
            self.led_off(number)
            self.led_off(40 + number)
            self.led_off(49 - number)
        elif 17 <= number <= 24:
            self.led_off(number)
            self.led_off(49 - number)
           
    def wavesymbol(self, symbol, color, luminosity=80):
        change = 10
        while change <= luminosity:
            self.afficheur_set(symbol, color, change)
            change += 5
        change = luminosity
        while change >= 10:
            self.afficheur_set(symbol, color, change)
            change -= 5

    def falldown(self, color, luminosity):
        from time import sleep
        tempo = 0.3
        for raw in range(1, 20):
            self.raw_on(raw, color, luminosity)
            sleep(tempo)
            self.raw_off(raw)
            if raw in [2, 4]:
                tempo -= 0.1
            elif raw in [6]:
                tempo -= 0.05
            elif raw in [8, 10]:
                tempo -= 0.01

    def riseup(self, color, luminosity):
        from time import sleep
        tempo = 0.3
        for raw in range(19, 0, -1):
            self.raw_on(raw, color, luminosity)
            sleep(tempo)
            self.raw_off(raw)
            if raw in [18, 16]:
                tempo -= 0.1
            elif raw in [14]:
                tempo -= 0.05
            elif raw in [11, 10]:
                tempo -= 0.01             
            
    def diagdown(self, color="green", luminosity=80):
        tempo = 0.3
        for d in range(1, 25):  # De la diagonale 1 à 24
            self.diag45_on(d, color, luminosity)
            sleep(tempo)
            self.diag45_off(d)
            if d in [2, 4]:
                tempo -= 0.1
            elif d == 6:
                tempo -= 0.05
            elif d in [8, 10]:
                tempo -= 0.01

    def diagup(self, color="green", luminosity=80):
        from time import sleep
        tempo = 0.3
        for d in range(24, 0, -1):  # De la diagonale 24 à 1
            self.diag270_on(d, color, luminosity)
            sleep(tempo)
            self.diag270_off(d)
            if d in [23, 21]:
                tempo -= 0.1
            elif d == 19:
                tempo -= 0.05
            elif d in [16, 14]:
                tempo -= 0.01