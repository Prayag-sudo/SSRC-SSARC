import tkinter as tk
from tkinter import scrolledtext
import serial
import threading

# -------------------------
# SERIAL CONFIG
# -------------------------
PORT = "/dev/cu.usbserial-140"
BAUD = 115200

ser = serial.Serial(PORT, BAUD, timeout=0.1)

# -------------------------
# GLOBAL MODE
# -------------------------
global_mode = True

# -------------------------
# SERIAL READER
# -------------------------
def read_serial():
    while True:
        if ser.in_waiting:
            line = ser.readline().decode(errors="ignore")
            if line:
                output_box.insert(tk.END, line)
                output_box.see(tk.END)

# -------------------------
# ROUTING BUTTON CLASS
# -------------------------
class SSRCButton:
    def __init__(self, master, text, on_command, off_command, row, col, width, height):
        self.on_command = on_command
        self.off_command = off_command

        self.button = tk.Button(
            master,
            text=text,
            width=width,
            height=height,
            command=self.activate
        )
        self.button.grid(row=row, column=col, padx=5, pady=5)

    def activate(self):
        global global_mode
        if global_mode:
            ser.write(self.on_command.encode())
        else:
            ser.write(self.off_command.encode())

# -------------------------
# MAIN WINDOW
# -------------------------
root = tk.Tk()
root.title("SSRC Routing Interface")

# -------------------------
# NODE ACCESS BUTTONS (Larger)
# -------------------------

# Row 0
N1 = SSRCButton(root, "M1", "ooG111", "ooG011", 0, 0, 6, 3)
N2 = SSRCButton(root, "M3", "ooG113", "ooG013", 0, 2, 6, 3)
N3 = SSRCButton(root, "M5", "ooG115", "ooG015", 0, 4, 6, 3)

# Row 2
N4 = SSRCButton(root, "M7", "ooG117", "ooG017", 2, 0, 6, 3)
N5 = SSRCButton(root, "M9", "ooG119", "ooG019", 2, 2, 6, 3)
N6 = SSRCButton(root, "M11", "oG1111", "oG0113", 2, 4, 6, 3)

# Row 4
N7 = SSRCButton(root, "M13", "oG1113", "oG0113", 4, 0, 6, 3)
N8 = SSRCButton(root, "M15", "oG1115", "oG0115", 4, 2, 6, 3)
N9 = SSRCButton(root, "M17", "oG1117", "oG0117", 4, 4, 6, 3)

# -------------------------
# INTERMEDIATE BUTTONS (Smaller)
# -------------------------

# Horizontal intermediates
I1  = SSRCButton(root, "M19",  "oG1119",  "oG0119",  0, 1, 4, 2)
I2  = SSRCButton(root, "M21",  "oG1121",  "oG0121",  0, 3, 4, 2)

I6  = SSRCButton(root, "M29",  "oG1129",  "oG0129",  2, 1, 4, 2)
I7  = SSRCButton(root, "M31",  "oG1131",  "oG0131",  2, 3, 4, 2)

I11 = SSRCButton(root, "M39", "oG1139",  "oG0139",  4, 1, 4, 2)
I12 = SSRCButton(root, "M41", "oG1141",  "oG0141",  4, 3, 4, 2)

# Vertical intermediates
I3  = SSRCButton(root, "M23",  "oG1123",  "oG0123",  1, 0, 4, 2)
I4  = SSRCButton(root, "M25",  "oG1125",  "oG0125",  1, 2, 4, 2)
I5  = SSRCButton(root, "M27",  "oG1127",  "oG0127",  1, 4, 4, 2)

I8  = SSRCButton(root, "M33",  "oG1133",  "oG0133",  3, 0, 4, 2)
I9  = SSRCButton(root, "M35",  "oG1135",  "oG0135",  3, 2, 4, 2)
I10 = SSRCButton(root, "M37",  "oG1137",  "oG0137",  3, 4, 4, 2)

# -------------------------
# GLOBAL MODE BUTTON
# -------------------------
def toggle_global():
    global global_mode
    global_mode = not global_mode
    if global_mode:
        global_toggle.config(text="MODE: ON")
    else:
        global_toggle.config(text="MODE: OFF")

global_toggle = tk.Button(
    root,
    text="MODE: ON",
    width=12,
    height=2,
    command=toggle_global
)
global_toggle.grid(row=0, column=6, rowspan=3, padx=10)

# -------------------------
# LATCH & RESET
# -------------------------
def latch():
    ser.write("oooooR".encode())

def reset():
    ser.write("oooooM".encode())
def status():
    ser.write("oooooS".encode())

latch_button = tk.Button(root, text="LATCH", width=12, command=latch)
latch_button.grid(row=5, column=0, columnspan=2, pady=10)

reset_button = tk.Button(root, text="MASTER RESET", width=12, command=reset)
reset_button.grid(row=5, column=4, columnspan=2, pady=10)

status_button = tk.Button(root, text="Status", width=12, command=status)
status_button.grid(row=5, column=2, columnspan=2, pady=10)

# -------------------------
# OUTPUT WINDOW
# -------------------------
output_box = scrolledtext.ScrolledText(root, width=80, height=10)
output_box.grid(row=6, column=0, columnspan=7, padx=10, pady=5)

# -------------------------
# RAW COMMAND INPUT
# -------------------------
def send_raw(event=None):
    cmd = raw_entry.get()
    if cmd:
        ser.write(cmd.encode())
        raw_entry.delete(0, tk.END)

raw_entry = tk.Entry(root, width=60)
raw_entry.grid(row=7, column=0, columnspan=5, padx=10, pady=5)
raw_entry.bind("<Return>", send_raw)

send_button = tk.Button(root, text="SEND", command=send_raw)
send_button.grid(row=7, column=5)

# -------------------------
# START SERIAL THREAD
# -------------------------
thread = threading.Thread(target=read_serial, daemon=True)
thread.start()

root.mainloop()