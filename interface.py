import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import gantt 

def add_process_row():
    # Add a new row with three entries (at, bt, name) and a plus button
    row = len(process_rows) + 2  # Keep track of rows and ensure it's added below the last row
    w = 17
    # Arrival Time entry
    at_entry = ttk.Entry(input_frame, width=w)
    at_entry.grid(row=row, column=0, pady=5)
    
    # Burst Time entry
    bt_entry = ttk.Entry(input_frame, width=w)
    bt_entry.grid(row=row, column=1, pady=5)
    
    # Process Name entry
    name_entry = ttk.Entry(input_frame, width=w)
    name_entry.grid(row=row, column=2, pady=5)
    
    process_rows.append((at_entry, bt_entry, name_entry))

def update_quantum_selection():
    if quantum_mode.get() == "manual":
        manual_quantum_entry.config(state="normal")
    else:
        manual_quantum_entry.config(state="disabled")

def delete_last_row():
    # Remove the last process row except for if there is only one
    if len(process_rows)>1:
        at_entry, bt_entry, name_entry = process_rows.pop()
        at_entry.destroy()
        bt_entry.destroy()
        name_entry.destroy()

def display_gantt_chart():
    try:
        # Get Core Number
        core_no = int(cores_entry.get())
        
        # Get Process Data
        proccess_data = []
        for at_entry, bt_entry, name_entry in process_rows:
            try:
                # Get values from each entry and form the process data
                arrival_time = int(at_entry.get())
                burst_time = int(bt_entry.get())
                name = name_entry.get()
                proccess_data.append([arrival_time, burst_time, name])
            except ValueError:
                raise ValueError("Invalid input. Ensure all fields are filled correctly.")
        
        # Get Algorithm Choice
        algorithm = algorithms_combobox.get()
        if not algorithm:
            raise ValueError("Please select an algorithm.")
        
        print(f"Selected Algorithm: {algorithm}")
        # Generate Gantt chart (you can adjust the logic based on the selected algorithm)
        m_quantum = int(manual_quantum_entry.get()) if quantum_mode.get() == "manual" else 999
        gantt.generate_gantt_figure(core_no, proccess_data, quantum_mode.get(), m_quantum)
        plt.show()  # Display the figure
    
    except ValueError as e:
        show_error_popup(str(e))
    except Exception as e:
        show_error_popup(f"An error occurred: {str(e)}")

def show_error_popup(message):
    # Create a new top-level window to display the error message
    error_window = tk.Toplevel(root)
    error_window.title("Error")
    error_window.geometry("300x100") 
    error_label = ttk.Label(error_window, text=message, wraplength=250)
    error_label.pack(padx=10, pady=10)
    close_button = ttk.Button(error_window, text="Close", command=error_window.destroy)
    close_button.pack(pady=5)

#------------------------------
# Create GUI Structure
#------------------------------
root = tk.Tk()
root.title("OS Scheduling")
root.geometry("750x700") 

#Get third party ttk theme from local directory
root.tk.call('source', 'forest-light.tcl')
ttk.Style().theme_use('forest-light')

# Create a variable to store quantum selection mode
quantum_mode = tk.StringVar(value="auto")

# Create the frame
input_frame = tk.Frame(root, padx=20, pady=20)
input_frame.pack(anchor='n')  # Center the frame in the window

process_rows = []

# "Process Data" label
ttk.Label(input_frame, text="Process Data", font=("Helvatica", 13,'bold')).grid(row=0, column=0, pady=5, sticky="w")
ttk.Label(input_frame, text="Arrival Time", font=("Helvatica", 10,'bold')).grid(row=1, column=0, pady=5, sticky="w")
ttk.Label(input_frame, text="Burst Time", font=("Helvatica", 10,'bold')).grid(row=1, column=1, pady=5, sticky="w")
ttk.Label(input_frame, text="Name", font=("Helvatica", 10,'bold')).grid(row=1, column=2, pady=5, sticky="w")

# Plus button
plus_button = ttk.Button(input_frame, text="add row", command=add_process_row, style="Accent.TButton")
plus_button.grid(row=0, column=1, pady=5)

# Minus button
minus_button = ttk.Button(input_frame, text="remove row", command=delete_last_row)
minus_button.grid(row=0, column=2, pady=5)

# Add initial row
add_process_row()

# "Core No" label and entry
ttk.Label(input_frame, text="Number of Processors", font=("Helvatica", 10,'bold') ).grid(row=0, column=4, pady=5, padx=50, sticky="w")
cores_entry = ttk.Entry(input_frame, width=22)
cores_entry.grid(row=1, column=4, pady=5, padx=50, sticky="w")

#Quantum Selection
ttk.Label(input_frame, text="Quantum Selection", font=("Helvatica", 10, 'bold')).grid(row=2, column=4, pady=5, padx=50, sticky="w")

auto_quantum_radio = ttk.Radiobutton(input_frame, text="Automatic", value="auto", variable=quantum_mode, command=update_quantum_selection)
auto_quantum_radio.grid(row=3, column=4, pady=5, padx=50, sticky="w")

manual_quantum_radio = ttk.Radiobutton(input_frame, text="Manual", value="manual", variable=quantum_mode, command=update_quantum_selection)
manual_quantum_radio.grid(row=4, column=4, pady=5, padx=50, sticky="w")

# Entry field for manual quantum input
manual_quantum_entry = ttk.Entry(input_frame, width=22, state="disabled")
manual_quantum_entry.grid(row=5, column=4, pady=5, padx=50, sticky="w")


# Combobox for selecting algorithm
ttk.Label(input_frame, text="Select Algorithm", font=("Helvatica", 10,'bold')).grid(row=6, column=4, pady=5, padx=50, sticky="w")
algorithms = ["Round Robin", "FCFS", "SJF"]  # Add more algorithms as needed
algorithms_combobox = ttk.Combobox(input_frame, values=algorithms, state="readonly", width=20)
algorithms_combobox.grid(row=7, column=4, pady=5, padx=50, sticky="w")

# Submit button
submit_button = ttk.Button(input_frame, text="Submit", command=display_gantt_chart, style="Accent.TButton")
submit_button.grid(row=8, column=4, pady=10)

# Initialize the GUI
root.mainloop()
