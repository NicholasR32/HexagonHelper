import pyautogui as pag
from PIL import Image
import time

DEBUG = True

# Magic numbers
last_x_percent = 0.555
last_y_percent = 0.33
last_width_percent = 0.1
last_height_percent = 0.07

# Dimensions for a single digit in any seconds place
seconds_digit_width_percent = 0.045
seconds_digit_height_percent = 0.1

thousands_x_percent = 0.6695
thousands_y_percent = 0.33

# Dimensions for a single digit in any frames place
frames_digit_width_percent = 0.022
frames_digit_height_percent = 0.045

frames_x_percent = 0.857
frames_y_percent = 0.374

def screenshot_region(x, y, width, height):
    # Get display dimensions
    screen_width, screen_height = pag.size()

    # Calculate the absolute coordinates based on relative proportions
    abs_x = int(x * screen_width)
    abs_y = int(y * screen_height)
    abs_width = int(width * screen_width)
    abs_height = int(height * screen_height)

    # Take the screenshot of the specified region
    screenshot = pag.screenshot(region=(abs_x, abs_y, abs_width, abs_height))

    return screenshot

def scan_for_last():
    while True:
        # Delay screenshot calls to save resources
        time.sleep(0.1)
        print("Scanning for LAST...\n" if DEBUG else "", end="")

        # Screenshot the region where the "LAST" text should be
        screenshot_last = screenshot_region(last_x_percent, last_y_percent, last_width_percent, last_height_percent)
        screenshot_last.save("last.png")

        # Check if the text is there
        try:
            found = pag.locate(needleImage="last_text.png", haystackImage=screenshot_last)
        # Not there.
        except pag.ImageNotFoundException:
            print("LAST text not found.\n" if DEBUG else "", end="")
        # Text is there, grab the timer!
        else:
            print("LAST text found!\n" if DEBUG else "", end="")
            # print(found)
            scan_timer()
            time.sleep(1)

def scan_timer():
    time = ""
    # Scan each seconds digit in the timer from L to R, starting with the thousands place.
    # 0=thousands, 1=hundreds, 2=tens, 3=ones
    # (If the thousands  digit ever gets used, I will be very impressed)
    for place in range(0,4):
        # Screenshot region where this digit should be.
        screenshot_digit = screenshot_region(place * seconds_digit_width_percent + thousands_x_percent,
                                             thousands_y_percent,
                                             seconds_digit_width_percent,
                                             seconds_digit_height_percent)

        digit_val = locate_digit(screenshot_digit, True)

        if digit_val == -1:
            print(f"seconds place {place} has no digit.")
        else:
            time += str(digit_val)

    time += ":"

    # Scan each frames digit in the timer. Easier, since there's always 2 of them.
    for place in range(0,2):
        # Screenshot region where this digit should be.
        screenshot_digit = screenshot_region(place * frames_digit_width_percent + frames_x_percent,
                                             frames_y_percent,
                                             frames_digit_width_percent,
                                             frames_digit_height_percent)

        digit_val = locate_digit(screenshot_digit, False)

        # This should never happen.
        if digit_val == -1:
            print(f"frames place {place} has no digit!?!?!?!?")
        else:
            time += str(digit_val)
    print(f"Time survived: {time}")

# Searches the given screenshot for any digit.
def locate_digit(screenshot_digit, seconds_or_frames):
    # Search for every possible digit from 0-9.
    for digit in range(0,10):
        try:
            # Compare with the digit templates in either seconds or frames places.
            if seconds_or_frames:
                found = pag.locate(needleImage=f"secondsdigits/{digit}_seconds.png",
                                   haystackImage=screenshot_digit,
                                   confidence=0.95)
            else:
                found = pag.locate(needleImage=f"framesdigits/{digit}_frames.png",
                                    haystackImage=screenshot_digit,
                                    confidence=0.95)
        # This is not the digit.
        except pag.ImageNotFoundException:
            pass
            # print(f"{digit} not in place {place}.")
        # This digit is here, return it!
        else:
            return digit

    # There is no digit in this spot. Should only happen for the tens, hundreds, and thousands of seconds.
    return -1

scan_for_last()



############# testing stuff

# screenshot_last = screenshot_region(last_x_percent, last_y_percent, last_width_percent, last_height_percent)
# screenshot_last.save("last.png")

# img = Image.open("timer.png")
# img.show()

# Goes up to thousandths place
timer_x_percent = 0.67
timer_y_percent = 0.33
timer_width_percent = 0.25
timer_height_percent = 0.1

last_x_percent = 0.555
last_y_percent = 0.33
last_width_percent = 0.1
last_height_percent = 0.07

# Dimensions for a single digit in any seconds place
seconds_digit_width_percent = 0.045
seconds_digit_height_percent = 0.1

thousands_x_percent = 0.6695
thousands_y_percent = 0.33

hundreds_x_percent = thousands_x_percent + seconds_digit_width_percent
tens_x_percent = thousands_x_percent + 2*seconds_digit_width_percent
ones_x_percent = thousands_x_percent + 3*seconds_digit_width_percent

screenshot = screenshot_region(hundreds_x_percent, thousands_y_percent, seconds_digit_width_percent, seconds_digit_height_percent)
screenshot.save("hundreds.png")
screenshot = screenshot_region(tens_x_percent, thousands_y_percent, seconds_digit_width_percent, seconds_digit_height_percent)
screenshot.save("tens.png")
screenshot = screenshot_region(ones_x_percent, thousands_y_percent, seconds_digit_width_percent, seconds_digit_height_percent)
screenshot.save("ones.png")

# Dimensions for a single digit in any frames place
frames_digit_width_percent = 0.022
frames_digit_height_percent = 0.045

frames_x_percent = 0.857
frames_y_percent = 0.374

screenshot = screenshot_region(frames_x_percent, frames_y_percent, frames_digit_width_percent, frames_digit_height_percent)
screenshot.save("frame_tens.png")
screenshot = screenshot_region(frames_x_percent+frames_digit_width_percent, frames_y_percent, frames_digit_width_percent, frames_digit_height_percent)
screenshot.save("frame_ones.png")