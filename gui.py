import tkinter as tk
from tkinter import ttk
import pyglet

def resize_window(root, x_percent, y_percent, width_percent, height_percent):
    global screen_width
    global screen_height
    # Set window dimensions relative to display, and center in screen
    abs_x = int(x_percent * screen_width // 2)
    abs_y = int(y_percent * screen_height // 2)
    abs_width = int(width_percent * screen_width)
    abs_height = int(height_percent * screen_height)

    root.geometry(f'{abs_width}x{abs_height}+{abs_x}+{abs_y}')
    print(root.geometry())
    print(f'{screen_width} {screen_height}')

def get_canvas(root):
    # Wait for window to update, then get dimensions
    root.update_idletasks()
    global window_width
    global window_height

    canvas = tk.Canvas(root, width=window_width, height=window_height, highlightbackground='black', highlightthickness=6)
    # Draw black rectangle spanning top of screen
    # canvas.create_rectangle(0, window_height * 0.1, window_width, window_height*0.2, fill='black', outline='black')

    # canvas.create_text(window_width // 2, window_height * 0.1, text='Hexagon', anchor='n', font=('Bump IT UP', 25), fill='white')
    canvas.pack()

    return canvas

# Wrapper for the color changing function below.
def cycle_color(root, color1, color2):
    cycle_color_rec(root, color1, color2, step=0, direction=1)

# Cycles the background of the given container between the two colors smoothly.
def cycle_color_rec(root, color1, color2, step, direction):
    MIN_STEPS = 0
    MAX_STEPS = 100

    # Text color changes faster.
    if isinstance(root, tk.Label):
        MAX_STEPS = 50

    new_color = [0,0,0]

    # Find difference in RGB vals between the two colors
    color_diff = [c2-c1 for c1, c2 in zip(color1, color2)]

    # Calculate offset in color based on step count
    for i in range(0,3):
        new_color[i] = color1[i] + int((step / MAX_STEPS) * color_diff[i])

    # Set new color. If it is a frame, change the background.
    # If it's a label, change the foreground (text color).
    if isinstance(root, tk.Frame):
        root.configure(bg=rgb_to_hex(new_color))
    elif isinstance(root, tk.Label):
        root.configure(fg=rgb_to_hex(new_color))
    # print(f"background is now {new_color}")

    # Change direction once color hits one end
    if step == MAX_STEPS:
        direction = -1
    elif step == MIN_STEPS:
        direction = 1
    step += direction

    # Next color call
    root.after(20, cycle_color_rec, root, color1, color2, step+direction, direction)

# Helper functions from chat
def hex_to_rgb(hex_color):
    # Remove the '#' character if present
    hex_color = hex_color.lstrip('#')

    # Convert the hex color code to integers for R, G, B
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)

    return (r, g, b)

def rgb_to_hex(rgb):
    # Ensure that each RGB value is within the valid range
    r = max(0, min(255, rgb[0]))
    g = max(0, min(255, rgb[1]))
    b = max(0, min(255, rgb[2]))
    # Convert RGB tuple to hexadecimal color code
    return '#{:02x}{:02x}{:02x}'.format(r, g, b)

def draw_text(root, level_name, data):
    global level_bg_colors
    global level_name_colors
    global current_level

    # Draw level name
    levelname_label = tk.Label(root, text=level_name, anchor='n', font=('Bump IT UP', 12), background='black', foreground='white', pady=17)
    levelname_label.grid(row=0, column=1, sticky='ew')
    root.rowconfigure(0, weight=1)
    root.columnconfigure(1, weight=1)

    # Make it color changing
    cycle_color(levelname_label, level_name_colors[current_level][0], level_name_colors[current_level][1])

    global button_image_left
    global button_image_right

    # Must use lambdas so function is called when button is clicked, not when button is built
    prev_button = tk.Button(root, activebackground='black', text='prev', bg='black', borderwidth=0, command=lambda: switch_level(-1), image=button_image_left)
    prev_button.grid(row=0, column=0, sticky='ew')

    prev_button = tk.Button(root, activebackground='black', text='next', bg='black', borderwidth=0, command=lambda: switch_level(1), image=button_image_right)
    prev_button.grid(row=0, column=2, sticky='ew')


    # Draw stats for best time, avg time, total number of attempts
    stats = calc_stats(data)
    num_attempts_label = tk.Label(root, text=stats[0], padx=40, anchor='center', font=('Bump IT UP', 12), background='black', foreground='white')
    best_attempt_label = tk.Label(root, text=stats[1], padx=40, anchor='center', font=('Bump IT UP', 12), background='black', foreground='white')
    avg_attempt_label = tk.Label(root, text=stats[2], padx=40, anchor='center', font=('Bump IT UP', 12), background='black', foreground='white')

    num_attempts_label.grid(row=1, column=0, sticky='ew')
    best_attempt_label.grid(row=1, column=1, sticky='ew')
    avg_attempt_label.grid(row=1, column=2, sticky='ew')

    # Add space between stats and table
    root.rowconfigure(2, minsize=40)

def calc_stats(data):
    stats = ['','','']

    # Calculate number of attempts
    num_attempts = len(data)
    stats[0] = f'Attempts: {num_attempts}'

    # Calculate best and avg attempt
    max_seconds = -1
    max_frames = -1

    total_frames = 0
    for attempt in data:
        att_seconds = int(attempt[0][0])
        att_frames = int(attempt[0][1])

        # Add to total
        total_frames += (att_seconds * 60 + att_frames)

        # This attempt is higher in seconds
        if (att_seconds > max_seconds):
            max_seconds = att_seconds
            max_frames = att_frames
        # This attempt has the same number of seconds, but a few more frames
        elif (att_seconds == max_seconds and att_frames > max_frames):
            max_frames = att_frames

    avg_seconds = int(round((total_frames / num_attempts) // 60))
    avg_frames = int(round((total_frames / num_attempts) % 60))

    stats[1] = f'Best: {max_seconds}:{max_frames}'
    stats[2] = f'Average: {avg_seconds}:{avg_frames}'
    print(stats)

    return stats

def switch_level(next):
    global root
    global current_level
    current_level += next
    # Wrap around current level index
    if current_level == 6:
        current_level = 0
    elif current_level == -1:
        current_level = 5
    print(f'current level: {current_level}')
    draw_all(root, current_level)

# Using treeview
def draw_table(root, data):
    global window_width
    global window_height

    # Put Treeview inside frame
    tree_frame = tk.Frame(root, bg='white')
    tree_frame.grid(row=3, column=0, columnspan=3)

    # Draw scrollbar
    scrollbar = tk.Scrollbar(tree_frame)
    scrollbar.pack(side=tk.RIGHT, fill='y')

    # Create tree
    tree = ttk.Treeview(tree_frame, yscrollcommand=scrollbar.set, selectmode='none')

    # Configure scrollbar
    scrollbar.config(command=tree.yview)

    # Define columns for treeview
    tree['columns'] = ('time', 'date')
    # Get rid of phantom column
    tree.column('#0', width=0, stretch='no')
    tree.column('time', width=int(window_width*0.95)//2, anchor='center')
    tree.column('date', width=int(window_width*0.95)//2, anchor='center')
    # Style headings (background won't change for some reason)
    style = ttk.Style()
    style.configure('Treeview.Heading', font=('Bump IT UP', 12), background='black')

    tree.heading('#0', text='phantom col')
    tree.heading('time', text='time')
    tree.heading('date', text='date')

    tree.tag_configure('custom', font=('Bump IT UP', 12), background='black', foreground='white')
    for temp in enumerate(data):
        item = temp
        index = str(item[0])
        entry = item[1]


        # Reformat the time part of the entry
        entry[0] = str(entry[0][0] + ":" + entry[0][1])
        # print(f'adding {entry}')

        # Root of Treeview table is represented by empty string
        tree.insert(parent='', index='end', iid=index, text="0", values=entry)
        # Add style to row entry
        tree.item(index, tags=('custom'))
    tree.pack(side=tk.BOTTOM)

def draw_all(root, current_level):
    global level_bg_colors
    global level_name_colors
    global level_names
    global table

    for widget in root.winfo_children():
        widget.destroy()

    app_frame = tk.Frame(root, highlightbackground='black', highlightthickness=6)
    app_frame.grid(row=0, column=0, sticky='nsew')

    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    cycle_color(app_frame, level_bg_colors[current_level][0], level_bg_colors[current_level][1])

    draw_text(app_frame, level_names[current_level], table)
    draw_table(app_frame, table)

    root.mainloop()

if __name__ == '__main__':
    # Get font
    pyglet.options['win32_gdi_font'] = True
    pyglet.font.add_file('fonts/bump-it-up.ttf')

    level_names = ['Hexagon', 'Hexagoner', 'Hexagonest', 'Hyper Hexagon', 'Hyper Hexagoner', 'Hyper Hexagonest']
    level_bg_colors = [[hex_to_rgb("#7A0B12"), hex_to_rgb("#89790A")],
                       [hex_to_rgb("#2CE969"), hex_to_rgb("#DF8F10")],
                       [hex_to_rgb("#116300"), hex_to_rgb("#116300")],
                       [hex_to_rgb("#081469"), hex_to_rgb("#015566")],
                       [hex_to_rgb("#E70C8C"), hex_to_rgb("#2070EF")],
                       [hex_to_rgb("#696969"), hex_to_rgb("#BDBDBD")]]
    level_name_colors = [[hex_to_rgb("#CB9040"), hex_to_rgb("#E5AA40")],
                         [hex_to_rgb("#86C140"), hex_to_rgb("#BAF540")],
                         [hex_to_rgb("#116300"), hex_to_rgb("#116300")],
                         [hex_to_rgb("#404CE5"), hex_to_rgb("#406CF5")],
                         [hex_to_rgb("#5B52D2"), hex_to_rgb("#F80483")],
                         [hex_to_rgb("#F9F9F9"), hex_to_rgb("#F9F9F9")]]

    table = [[['10', '30'], '02/29/24 07:47:18 PM'],
             [['70', '01'], '02/29/24 07:48:35 PM'],
             [['6', '41'], '02/29/24 07:48:47 PM'],
             [['90', '38'], '02/29/24 07:50:19 PM'],
             [['5', '49'], '02/29/24 07:50:34 PM'],
             [['2', '13'], '02/29/24 07:50:50 PM'],
             [['6', '39'], '02/29/24 07:51:05 PM'],
             [['3', '19'], '02/29/24 07:51:15 PM'],
             [['35', '59'], '02/29/24 07:52:19 PM'],
             [['10', '30'], '02/29/24 07:47:18 PM'],
             [['70', '02'], '02/29/24 07:48:35 PM'],
             [['6', '41'], '02/29/24 07:48:47 PM'],
             [['89', '39'], '02/29/24 07:50:19 PM'],
             [['5', '49'], '02/29/24 07:50:34 PM'],
             [['2', '13'], '02/29/24 07:50:50 PM'],
             [['6', '39'], '02/29/24 07:51:05 PM'],
             [['3', '19'], '02/29/24 07:51:15 PM'],
             [['5', '15'], '02/29/24 07:51:22 PM'],
             [['35', '59'], '02/29/24 07:52:19 PM']]

    current_level = 0
    root = tk.Tk()

    # Get display dimensions
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    # Resize window
    scale_x = 0.5
    scale_y = 0.5
    window_width = int(screen_width * scale_x)
    window_height = int(screen_height * scale_y)
    window_pos_x = int(scale_x * screen_width // 2)
    window_pos_y = int(scale_y * screen_height // 2)

    root.geometry(f'{window_width}x{window_height}+{window_pos_x}+{window_pos_y}')


    button_image_left = tk.PhotoImage(file='arrowleft.png')
    button_image_right = tk.PhotoImage(file='arrowright.png')

    draw_all(root, current_level)
