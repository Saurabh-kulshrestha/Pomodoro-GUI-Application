from tkinter import *

# ---------------------------- CONSTANTS ------------------------------- #
PINK = "#e2979c"            # Color for short breaks
RED = "#e7305b"             # Color for long breaks
GREEN = "#9bdeac"           # Color for work sessions
YELLOW = "#f7f5dd"          # Background color
FONT_NAME = "Courier"       # Font style used throughout the UI

WORK_MIN = 25               # Work session time in minutes
SHORT_BREAK_MIN = 5         # Short break time in minutes
LONG_BREAK_MIN = 20         # Long break time in minutes

reps = 0                    # Keeps track of total repetitions (sessions)
timer = None                # To store the timer object (for after_cancel)

# ---------------------------- TIMER RESET ------------------------------- #
def reset_timer():
    global reps
    reps = 0  # Reset session counter to 0

    # Cancel the running timer using its ID
    window.after_cancel(timer)

    # Reset the session label back to 'Timer'
    status.config(text="Timer", fg=GREEN)

    # Reset the time displayed on the canvas to "00:00"
    canvas.itemconfig(timer_text, text="00:00")

    # Clear the check marks that show completed work sessions
    check_marks.config(text="")

# ---------------------------- TIMER MECHANISM ------------------------------- #
def start_timer():
    global reps
    reps += 1  # Increase session count each time timer is started

    # Convert durations from minutes to seconds
    work_sec = WORK_MIN * 60
    short_break_sec = SHORT_BREAK_MIN * 60
    long_break_sec = LONG_BREAK_MIN * 60

    # Every 8th session is a long break
    if reps % 8 == 0:
        status.config(text="Break", fg=RED)
        count_down(long_break_sec)
    # Every 2nd, 4th, 6th session is a short break
    elif reps % 2 == 0:
        status.config(text="Break", fg=PINK)
        count_down(short_break_sec)
    # Every 1st, 3rd, 5th, 7th session is a work session
    else:
        status.config(text="Work", fg=GREEN)
        count_down(work_sec)

# ---------------------------- COUNTDOWN MECHANISM ------------------------------- #
def count_down(count):
    # Calculate minutes and seconds from total seconds
    count_min = count // 60
    count_sec = count % 60

    # Format seconds to always be two digits (e.g., 0 => 00)
    if count_sec < 10:
        count_sec = f"0{count_sec}"

    # Update the timer display on canvas
    canvas.itemconfig(timer_text, text = f"{count_min}:{count_sec}")

    # If time is remaining, call count_down again after 100ms (for testing; use 1000 for real)
    if count > 0:
        global timer
        timer = window.after(100, count_down, count - 1)
    else:
        # When a session finishes, display check marks for each completed work session
        mark = ""
        work_session = reps // 2
        for _ in range(work_session):
            mark += "✔"
        check_marks.config(text=mark)

        # Automatically start the next session
        start_timer()

# ---------------------------- UI SETUP ------------------------------- #
window = Tk()
window.title("Pomodoro")
window.config(padx=100, pady=50, bg=YELLOW)  # Add padding and background color

# Canvas for tomato image and timer display
canvas = Canvas(width=220, height=224, bg=YELLOW, highlightthickness=0)
tomato_image = PhotoImage(file="tomato.png")  # Load image
canvas.create_image(110, 112, image=tomato_image)  # Place image at center
timer_text = canvas.create_text(110, 130, text="00:00", fill="white", font=(FONT_NAME, 28, "bold"))  # Timer text
canvas.grid(row=1, column=1)

# Label for status: "Work", "Break", etc.
status = Label(text="Timer", fg=GREEN, font=(FONT_NAME, 50, "bold"), bg=YELLOW)
status.grid(row=0, column=1)

# Button to start the timer
start_button = Button(text="Start", font=(FONT_NAME, 15, "bold"), command=start_timer)
start_button.grid(row=2, column=0)

# Button to reset the timer
reset_button = Button(text="Reset", font=(FONT_NAME, 15, "bold"), command=reset_timer)
reset_button.grid(row=2, column=2)

# Label to show ✔ marks after each completed work session
check_marks = Label(font=(FONT_NAME, 15, "bold"), fg=GREEN, bg=YELLOW)
check_marks.grid(row=3, column=1)

# Run the application loop
window.mainloop()
