import matplotlib.pyplot as plt
import numpy as np
from random import random as r
import rr_logic
from copy import copy

def generate_gantt_figure(core_no, proccess_data, mode, m_quantum):
    # Generated from user input
    proccesor_labels = ["proccesor "+str(i) for i in range(1, core_no+1)]
    result = rr_logic.rr_result(proccess_data, core_no)

    # Map the returned variables to local ones
    quantum_range = result["quantum_range"]
    AWT_Bar = result["AWT_Bar"]
    TTAT_Bar = result["TTAT_Bar"]
    best_q_schema = result["best_q_schema"]

    #In case of manual quantum
    m_p_data = rr_logic.init_process_data_structure(proccess_data)
    m_c_no = rr_logic.init_core_data_structure(core_no)
    m_result = rr_logic.schedule_single_quantum(m_p_data, m_c_no ,m_quantum)

    if mode != "auto":
        best_q_schema[0] = m_result["schema"]

        for i, q in enumerate(copy(quantum_range)):
            if q < m_quantum and (len(quantum_range) == i + 1 or quantum_range[i+1] > m_quantum):
                AWT_Bar.insert(i+1, m_result["AWT"])
                TTAT_Bar.insert(i+1, m_result["TTAT"])
                quantum_range.insert(i+1, m_quantum)

    x_axis = np.arange(len(quantum_range))

    # Create the figure
    if core_no == 1:
        layout = [
        ["A", "B"],
        ["0", "B"],
        ["0", "C"],
        ["0", "C"]
    ]
    elif core_no == 2:
        layout = [
        ["A", "B"],
        ["0", "C"],
    ]
    elif core_no == 3:
        layout = [
        ["A", "B"],
        ["A", "B"],
        ["A", "C"],
        ["0", "C"]
    ]
    else:
        layout = [
            ["A", "B"],
            ["A", "C"]
        ]
    fig, axs = plt.subplot_mosaic(layout, figsize=(14, 7), dpi=110)
    
    if "0" in axs:
        axs['0'].axis('off')

    gantt_plot = axs["A"]
    awt_plot = axs["B"]
    ttat_plot = axs["C"]

    # Gantt Chart
    gantt_plot.set_title(f"Gantt Chart for the schedule with the best quantum\nQ={best_q_schema[1]}" if mode == "auto" else f"Gantt Chart for the schedule with the given quantum\nQ={m_quantum}")
    gantt_plot.set_xlabel("Time(ms)")

    for key in dict(reversed(list(best_q_schema[0].items()))): 
        cores = best_q_schema[0][key]
        for block in cores[1:]: 
            block_proccesor_category = proccesor_labels[key-1]
            block_total_width = block[2] - block[1] 
            block_x_start = block[1] 
            col = (r(), r(), r(), 0.5)  # Random RGB color
            hbar_plot = gantt_plot.barh(block_proccesor_category, block_total_width, left=block_x_start, color=col, edgecolor="black") 
            gantt_plot.bar_label(hbar_plot, [f"{block[1]}\n{block[3]}\n{block[2]}"], label_type="center")

    # Average Waiting Time plot
    awt_plot.set_title("Average Waiting Time")
    awt_plot.set_xticks(ticks=x_axis, labels=quantum_range, rotation=90)

    for i,b in enumerate(AWT_Bar):
        if b == min(AWT_Bar):
            bar_plot1 = awt_plot.bar(x_axis[i], b, width=0.5, color='#63993D')
            awt_plot.bar_label(bar_plot1, [round(b,2)], label_type="edge", rotation=90, padding=5)
            awt_plot.get_xticklabels()[i].set_color('#87BB62')
            awt_plot.get_xticklabels()[i].set_fontweight('bold')
        elif b == m_result["AWT"] and awt_plot.get_xticklabels()[i].get_text() == str(m_quantum) and mode !='auto':
            bar_plot1 = awt_plot.bar(x_axis[i], b, width=0.5, color='#F5921B')
            awt_plot.bar_label(bar_plot1, [round(b,2)], label_type="edge", rotation=90, padding=5)
            awt_plot.get_xticklabels()[i].set_color('#CA6C0F')
            awt_plot.get_xticklabels()[i].set_fontweight('bold')
        else:
            bar_plot1 = awt_plot.bar(x_axis[i], b, width=0.5, color='#0066CC')

    awt_plot.set_ylabel("Time(ms)")
    awt_plot.set_xlabel("Quantum")

    # Total Turn-Around Time plot
    ttat_plot.set_title("Total Turn Around Time")
    ttat_plot.set_xticks(ticks=x_axis, labels=quantum_range, rotation=90)
    ttat_plot.set_ylabel("Time(ms)")
    ttat_plot.set_xlabel("Quantum")
    
    for l,h in enumerate(TTAT_Bar):
        if h == min(TTAT_Bar):
            bar_plot2 = ttat_plot.bar(x_axis[l], h, width=0.5, color='#63993D')
            ttat_plot.bar_label(bar_plot2, [h], label_type="edge", rotation=90, padding=5)
            ttat_plot.get_xticklabels()[l].set_color('#63993D')
            ttat_plot.get_xticklabels()[l].set_fontweight('bold')
        elif h == m_result["TTAT"] and ttat_plot.get_xticklabels()[l].get_text() == str(m_quantum) and  mode !='auto':
            bar_plot1 = ttat_plot.bar(x_axis[l], h, width=0.5, color='#F5921B')
            ttat_plot.bar_label(bar_plot1, [round(h,2)], label_type="edge", rotation=90, padding=5)
            ttat_plot.get_xticklabels()[l].set_color('#CA6C0F')
            ttat_plot.get_xticklabels()[l].set_fontweight('bold')
        else:
            bar_plot2 = ttat_plot.bar(x_axis[l], h, width=0.5, color='#0066CC')

    # Set y-axis ranges
    awt_plot.set_ylim([min(AWT_Bar) - 50 if min(AWT_Bar) - 50 > 0 else 0, max(AWT_Bar) + 50])
    ttat_plot.set_ylim([min(TTAT_Bar) - 50, max(TTAT_Bar) + 50])

    fig.tight_layout(pad=1.0)