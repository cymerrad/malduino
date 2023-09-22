import click
import colorsys
from consts import BLINK, BLUE, CYAN, GREEN, LED_OFF, MAGENTA, RED, YELLOW
from itertools import cycle

PREAMBLE = """LOCALE US
LED 255 0 255
DELAY 3000
DEFAULTDELAY 1000
LED 255 0 0
LED 255 255 0
LED 0 255 0

"""

DEFAULT_MESSAGE="All work and no play makes Jack a dull boy. "

@click.command()
@click.argument('filename', type=click.Path())
@click.option('--text', default=DEFAULT_MESSAGE, help='Text to be repeated.')
# @click.option('--duration', default=DEFAULT_DURATION_MS, help='Duration of LED blink in milliseconds (default: 5000).')
# @click.option('--speed', default=DEFAULT_SPEED_MS, help='Speed of LED blink in milliseconds (default: 500).')
@click.option('--hours', default=8, help='Number of hours to repeat the sequence (default: 1).')
@click.option('--tao', default=False, help='Print Tao?')
def dump_text(filename, text, hours, tao):
    """
    Dumps text into the specified file.
    """

    malduino_script = ""
    if tao:
        malduino_script = generate_tao()
    else:
        malduino_script = generate_jack(text, hours)

    try:
        with open(filename, 'w') as file:
            file.write(malduino_script)
        click.echo(f"Text has been successfully dumped into {filename}")
    except Exception as e:
        click.echo(f"An error occurred: {e}")

def generate_jack(message, hours):
    """
    Generate a MalduinoW script with specified actions.

    Args:
        hours (int): The number of hours to repeat the actions.

    Returns:
        str: MalduinoW script.
    """
    script = ""

    script += PREAMBLE

    # Function to add LED blink commands
    def add_led_blink(duration_ms, speed_ms, LED_ON=MAGENTA):
        nonlocal script
        num_blinks = duration_ms // (2 * speed_ms)
        script += f"DEFAULTDELAY {speed_ms}\n"
        for _ in range(num_blinks):
            script += LED_ON  # Turn the LED on
            script += LED_OFF  # Turn the LED off

    def blink_once(LED_COLOR=MAGENTA):
        nonlocal script
        script += LED_OFF
        script += LED_COLOR

    def loop(line_no, LED_COLOR=MAGENTA):
        nonlocal script
        add_led_blink(3000, 200, GREEN)
        add_led_blink(2000, 100, YELLOW)
        add_led_blink(1000, 50, RED)

        script += "DEFAULTDELAY 1000\n"
        blink_once()
        # Type out a message and go to the next line
        script += f"STRING {line_no}: {message}\n"
        blink_once()
        script += "SHIFT ENTER\n"
        blink_once()

        script += LED_COLOR
        # Wait for 50 seconds
        script += "DELAY 50000\n"

    # Calculate the number of times to repeat the entire sequence
    repeats = hours * 60  # Convert hours to minutes

    largest_width = len(str(repeats))
    for i in range(1, repeats+1):
        padded_line_no = str(i).zfill(largest_width)
        loop(padded_line_no)

    return script

def enumerate_rainbow_colors(num_colors) -> str:
    # Initialize variables for hue, saturation, and value
    hue = 0.0
    saturation = 1.0
    value = 1.0

    # Calculate the hue increment based on the number of colors
    hue_increment = 1.0 / num_colors

    # Enumerate and print the RGB values for each color
    for _ in range(num_colors):
        # Convert HSV to RGB
        r, g, b = colorsys.hsv_to_rgb(hue, saturation, value)

        # Convert RGB values to integers in the range [0, 255]
        r = int(r * 255)
        g = int(g * 255)
        b = int(b * 255)

        # Yield the RGB values for Malduino
        yield f"LED {r} {g} {b}"

        # Increment the hue for the next color
        hue += hue_increment

def generate_tao():
    tao_book = open("tao.txt", "r").readlines()
    script = PREAMBLE

    for line, color in zip(tao_book, cycle(enumerate_rainbow_colors(16 ** 3))):
        pass

if __name__ == '__main__':
    dump_text()