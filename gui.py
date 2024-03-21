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

def draw_shapes(root):
    # Wait for window to update, then get dimensions
    root.update_idletasks()
    window_width = root.winfo_width()
    window_height = root.winfo_height()

    # Draw black rectangle spanning top of screen
    canvas = tk.Canvas(root, width=window_width, height=window_height, highlightbackground='black', highlightthickness=6)
    canvas.create_rectangle(0, window_height * 0.1, window_width, window_height*0.2, fill='black', outline='black')

    canvas.create_text(window_width // 2, window_height * 0.1, text='Hexagon', anchor='n', font=('Bump IT UP', 25), fill='white')
    canvas.pack()

    return canvas

def cycle_background_color(canvas, color1, color2, step, direction):
    MIN_STEPS = 0
    MAX_STEPS = 100

    new_color = [0,0,0]

    # Find difference in RGB vals between the two colors
    color_diff = [c2-c1 for c1, c2 in zip(color1, color2)]

    # Calculate offset in color based on step count
    for i in range(0,3):
        new_color[i] = color1[i] + int((step / MAX_STEPS) * color_diff[i])

    # Set new color
    canvas.configure(bg=rgb_to_hex(new_color))
    # print(f"background is now {new_color}")

    # Change direction once color hits one end
    if step == MAX_STEPS:
        direction = -1
    elif step == MIN_STEPS:
        direction = 1
    step += direction

    # Next color call
    root.after(20, cycle_background_color, canvas, color1, color2, step+direction, direction)

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

def draw_grid(canvas, table):
    for i, pair in enumerate(table):
        timer_raw = pair[0]
        timer = f"{timer_raw[0]}:{timer_raw[1]}"
        date = pair[1]

        timer_label = tk.Label(canvas, text=timer, anchor='n', font=('Bump IT UP', 12), bg='black', fg='white')
        date_label = tk.Label(canvas, text=date, anchor='n', font=('Bump IT UP', 12), bg='black', fg='white')

        timer_label.grid(row=i, column=0)
        date_label.grid(row=i, column=1)
        print(f"adding {timer} {date}")

# Using treeview
def draw_grid_2(canvas, table):
    global window_width
    global window_height

    # Put Treeview inside frame
    tree_frame = tk.Frame(canvas, bg='white')
    # tree_frame.pack()
    tree_frame.lift()

    tree = ttk.Treeview(canvas)
    tree['columns'] = ('time', 'date')
    # Get rid of phantom column
    tree.column('#0', width=0, stretch='no')
    tree.column('time', width=int(window_width*0.95)//2, anchor='center')
    tree.column('date', width=int(window_width*0.95)//2, anchor='center')
    # Style headings
    style = ttk.Style()
    # background won't change for some reason
    style.configure('Treeview.Heading', font=('Bump IT UP', 12), background='black')

    tree.heading('#0', text='phantom col')
    tree.heading('time', text='time')
    tree.heading('date', text='date')
    
    tree.tag_configure('custom', font=('Bump IT UP', 12), background='black', foreground='white')
    for item in enumerate(table):
        index = str(item[0])
        entry = item[1]
        
        # print(f'adding {item}')
        # Root of Treeview table is represented by empty string
        tree.insert(parent='', index='end', iid=index, text="0", values=entry)
        # Add style to row entry
        tree.item(index, tags=('custom'))
    tree.pack(side=tk.BOTTOM, expand=False, fill=tk.BOTH, pady=window_height*0.2)


if __name__ == '__main__':
    # Get font
    pyglet.options['win32_gdi_font'] = True
    pyglet.font.add_file('fonts/bump-it-up.ttf')

    root = tk.Tk()
    # root.resizable(False, False)
    # MyLabel = tk.Label(root, text="EXAMPLE TEXT", font=('Bump IT UP', 25))
    # MyLabel.pack()

    # Get display dimensions
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    resize_window(root, 0.5, 0.5, 0.5, 0.5)
    canvas = draw_shapes(root)

    window_width = canvas.winfo_reqwidth()
    window_height = canvas.winfo_reqheight()
    print(str(window_width) + " " + str(window_height))


    hexagon_color1 = hex_to_rgb("#7A0B12")
    hexagon_color2 = hex_to_rgb("#89790A")

    cycle_background_color(canvas, hexagon_color1, hexagon_color2, 0, 1)

    table = [[['10', '30'], '02/29/24 07:47:18 PM'],
             [['70', ''], '02/29/24 07:48:35 PM'],
             [['6', '41'], '02/29/24 07:48:47 PM'],
             [['89', '38'], '02/29/24 07:50:19 PM'],
             [['5', '49'], '02/29/24 07:50:34 PM'],
             [['2', '13'], '02/29/24 07:50:50 PM'],
             [['', ''], '02/29/24 07:50:57 PM'],
             [['6', '39'], '02/29/24 07:51:05 PM'],
             [['3', '19'], '02/29/24 07:51:15 PM'],
             [['5', ''], '02/29/24 07:51:22 PM'],
             [['', ''], '02/29/24 07:51:27 PM'],
             [['35', '59'], '02/29/24 07:52:19 PM']]
    
    draw_grid_2(canvas, table)
    # canvas.grid_rowconfigure(0, weight=1)
    # canvas.grid_columnconfigure(0, weight=1)
    root.mainloop()
