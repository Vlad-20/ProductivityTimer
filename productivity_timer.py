import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import datetime
import time

class TimerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Productivity Timer")
        self.root.geometry("400x250")
        self.root.resizable(False, False)
        
        # App state variables
        self.timer_id = None
        self.timer_running = False
        self.paused = False
        
        self.initial_seconds = 0
        self.time_remaining = 0
        self.pause_time = 0
        
        self.log_filepath = ""

        # Style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure("TLabel", font=("Inter", 11))
        self.style.configure("TButton", font=("Inter", 11, "bold"))
        self.style.configure("Header.TLabel", font=("Inter", 16, "bold"))
        self.style.configure("Timer.TLabel", font=("Inter", 48, "bold"))
        self.style.configure("Pause.TLabel", font=("Inter", 12))

        # Timer window
        self.timer_window = None
        self.timer_label = None
        self.pause_label = None
        self.pause_button = None

        self.create_main_window()

    def create_main_window(self):
        #Creates the widgets for the main setup window
        main_frame = ttk.Frame(self.root, padding="20 20 20 20")
        main_frame.pack(expand=True, fill="both")

        ttk.Label(main_frame, text="Set Your Time", style="Header.TLabel").pack(pady=(0, 10))

        # Time entry frame
        time_frame = ttk.Frame(main_frame)
        time_frame.pack()

        ttk.Label(time_frame, text="HH:").pack(side="left", padx=5)
        self.hh_entry = ttk.Entry(time_frame, width=3, font=("Inter", 12))
        self.hh_entry.pack(side="left")
        self.hh_entry.insert(0, "00")

        ttk.Label(time_frame, text="MM:").pack(side="left", padx=5)
        self.mm_entry = ttk.Entry(time_frame, width=3, font=("Inter", 12))
        self.mm_entry.pack(side="left")
        self.mm_entry.insert(0, "25")

        ttk.Label(time_frame, text="SS:").pack(side="left", padx=5)
        self.ss_entry = ttk.Entry(time_frame, width=3, font=("Inter", 12))
        self.ss_entry.pack(side="left")
        self.ss_entry.insert(0, "00")

        # Log file frame
        log_frame = ttk.Frame(main_frame)
        log_frame.pack(fill="x", pady=20)

        ttk.Button(log_frame, text="Browse Log File", command=self.browse_file).pack(side="left")
        self.log_label = ttk.Label(log_frame, text="No file selected", font=("Inter", 9), relief="sunken", padding=5)
        self.log_label.pack(side="left", fill="x", expand=True, padx=(10, 0))

        # Start button
        self.start_button = ttk.Button(main_frame, text="Start Timer", command=self.start_timer)
        self.start_button.pack(pady=(10, 0), fill="x")

    def browse_file(self):
        #Opens a file dialog to select/create a log file
        filepath = filedialog.asksaveasfilename(
            title="Select or Create Log File",
            initialfile="productivity_log.txt", # predefined filename
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if filepath:
            self.log_filepath = filepath
            #Show a truncated path if it's too long
            display_path = self.log_filepath
            if len(display_path) > 35:
                display_path = "..." + display_path[-32:]
            self.log_label.config(text=display_path)
        else:
            self.log_filepath = ""
            self.log_label.config(text="No file selected")

    def start_timer(self):
        # Validates input and starts the timer window
        # 1. Validate log path
        if not self.log_filepath:
            messagebox.showerror("Error", "Please select a log file location before starting.")
            return

        # 2. Validate time
        try:
            h_str = self.hh_entry.get()
            m_str = self.mm_entry.get()
            s_str = self.ss_entry.get()

            #Check length
            if (len(h_str) > 2) or (len(m_str) > 2) or (len(s_str) > 2):
                 messagebox.showerror("Error", "Time values must be 2 digits maximum (HH, MM, SS).")
                 return

            h = int(h_str)
            m = int(m_str)
            s = int(s_str)
            
            #Check ranges
            if not (0 <= h <= 99):
                messagebox.showerror("Error", "Hours (HH) must be between 00 and 99.")
                return
            
            if not (0 <= m <= 59):
                messagebox.showerror("Error", "Minutes (MM) must be between 00 and 59.")
                return

            if not (0 <= s <= 59):
                messagebox.showerror("Error", "Seconds (SS) must be between 00 and 59.")
                return
            
            self.initial_seconds = (h * 3600) + (m * 60) + s
            
            if self.initial_seconds <= 0:
                messagebox.showerror("Error", "Please enter a time greater than zero.")
                return

        except ValueError:
            messagebox.showerror("Error", "Please enter valid numbers for time (HH, MM, SS).")
            return

        # 3. Reset state and start
        self.time_remaining = self.initial_seconds
        self.pause_time = 0
        self.timer_running = True
        self.paused = False

        self.root.withdraw()  #Hide main window
        self.create_timer_window()
        self.update_timer()  #Start the timer loop

    def create_timer_window(self):
        #Creates the second window for the active countdown
        self.timer_window = tk.Toplevel(self.root)
        self.timer_window.title("Timer Running")
        self.timer_window.geometry("400x250")
        self.timer_window.resizable(False, False)
        
        # Protocol for window close
        # If user clicks the 'X', treat it as a 'Stop'
        self.timer_window.protocol("WM_DELETE_WINDOW", self.stop_timer)

        timer_frame = ttk.Frame(self.timer_window, padding="20 20 20 20")
        timer_frame.pack(expand=True, fill="both")

        self.timer_label = ttk.Label(timer_frame, text=self.format_time(self.time_remaining), style="Timer.TLabel")
        self.timer_label.pack(pady=(10, 0))

        self.pause_label = ttk.Label(timer_frame, text="Paused: 00:00:00", style="Pause.TLabel")
        self.pause_label.pack(pady=(0, 20))

        # Button frame
        button_frame = ttk.Frame(timer_frame)
        button_frame.pack(fill="x")

        self.pause_button = ttk.Button(button_frame, text="Pause", command=self.toggle_pause)
        self.pause_button.pack(side="left", fill="x", expand=True, padx=(0, 5))

        self.stop_button = ttk.Button(button_frame, text="Stop", command=self.stop_timer)
        self.stop_button.pack(side="left", fill="x", expand=True, padx=(5, 0))

    def update_timer(self):
        #The main 1-second loop that updates the timer and pause count
        if not self.timer_running:
            return

        if self.paused:
            #If paused, increment pause time
            self.pause_time += 1
            self.pause_label.config(text=f"Paused: {self.format_time(self.pause_time)}")
        else:
            #If running, decrement countdown time
            if self.time_remaining > 0:
                self.time_remaining -= 1
                self.timer_label.config(text=self.format_time(self.time_remaining))
            else:
                #Timer finished
                self.timer_running = False
                messagebox.showinfo("Time's Up!", "Your timer has finished.")
                self.write_log() #Write log
                self.cleanup_and_return() #Close and go back to main
                return #Stop the loop

        #Schedule the next update
        self.timer_id = self.root.after(1000, self.update_timer)

    def toggle_pause(self):
        #Toggles the paused state of the timer
        self.paused = not self.paused
        if self.paused:
            self.pause_button.config(text="Resume")
        else:
            self.pause_button.config(text="Pause")

    def stop_timer(self):
        #Stops the timer, logs the time and returns to the main window
        self.timer_running = False
        if self.timer_id:
            self.root.after_cancel(self.timer_id)
            self.timer_id = None
        
        self.write_log()
        self.cleanup_and_return()

    def write_log(self):
        #Calculates effective time and writes to the log file
        try:
            #It's the time that actually passed on the countdown
            effective_time_passed = self.initial_seconds - self.time_remaining
            
            #Total session time = time spent running + time spent paused
            total_session_time = effective_time_passed + self.pause_time
            
            with open(self.log_filepath, 'a') as f: #append mode
                f.write("="*30 + "\n")
                f.write(f"Session Logged: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Initial Time Set:   {self.format_time(self.initial_seconds)}\n")
                f.write(f"Effective Time Run: {self.format_time(effective_time_passed)}\n")
                f.write(f"Total Time Paused:  {self.format_time(self.pause_time)}\n")
                f.write(f"Total Session Time: {self.format_time(total_session_time)}\n")
                f.write("="*30 + "\n\n")

        except Exception as e:
            messagebox.showerror("Log Error", f"Failed to write to log file:\n{e}")

    def cleanup_and_return(self):
        #Destroys the timer window and shows the main window
        if self.timer_window:
            self.timer_window.destroy()
            self.timer_window = None
        
        #Reset main window entries
        self.hh_entry.delete(0, 'end')
        self.hh_entry.insert(0, '00')
        self.mm_entry.delete(0, 'end')
        self.mm_entry.insert(0, '25')
        self.ss_entry.delete(0, 'end')
        self.ss_entry.insert(0, '00')
        
        self.root.deiconify() #Show the main window again

    def format_time(self, total_seconds):
        #Converts seconds into HH:MM:SS string format
        total_seconds = int(total_seconds)
        hours, remainder = divmod(total_seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{hours:02}:{minutes:02}:{seconds:02}"

if __name__ == "__main__":
    root = tk.Tk()
    app = TimerApp(root)
    root.mainloop()