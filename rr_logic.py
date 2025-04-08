from copy import deepcopy, copy
#Function to find the current available proccessor
def find_next_core(Core):
    min_key = -1
    min_core = float('inf')

    for c in Core:
        if Core[c][-1][2] < min_core:
            min_core = Core[c][-1][2]
            min_key = c

    return min_key

#Function to find the completion time of each procces by checking each proccess run block and finding which one has the largest exit time
def find_completion_time(p_key, core):
    completion_time = float('inf')*-1
    for block in core.values():
        for c in block:
            if c[0] == p_key and c[2] > completion_time:
                completion_time = c[2] 
    return completion_time

def init_process_data_structure(proccess_data):
   return {i+1:[p[0], p[1], p[1], 0, p[2]] for i, p in enumerate(proccess_data)}

def init_core_data_structure(core_no):
    return {c:[[-1,0,0],] for c in range(1, core_no + 1)}


#Function to schedule the procceses in the cores
def schedule_single_quantum(Proccess, Core, quantum):
    while max([Proccess[p][2] for p in Proccess]) > 0:
        for p in Proccess:
            current_proccess = Proccess[p]
            if current_proccess[2] > 0: #Check if the procces has any burst time left
                core_number = find_next_core(Core) 
                current_core = Core[core_number]

                #Calculate the time when the process begins execution
                if current_proccess[1] == current_proccess[2] and len(list(Core.values())[-1]) == 1:
                    begin_time = current_proccess[0] #begin at arrival time
                else:
                    begin_time = current_core[-1][2] #begin at the end of the last procces on that core

                #Calculate at what time the process ends this block
                if current_proccess[2] - quantum < 0: #set remaining burst time to 0
                    end_time = begin_time + current_proccess[2]
                    current_proccess[2] = 0 
                else:
                    end_time = begin_time + quantum
                    current_proccess[2] -= quantum
                
                current_core.append([p, begin_time , end_time, current_proccess[4]]) #add process block to core [process number, begin time, end time]

    for p in Proccess:
        Proccess[p][3] = find_completion_time(p, Core) #add the completion time to each proccess

    waiting_time = {p:Proccess[p][3] - Proccess[p][1] - Proccess[p][0] if Proccess[p][3] - Proccess[p][1] - Proccess[p][0] > 0 else 0 for p in Proccess}
    turn_around_time = {p:(Proccess[p][1] + waiting_time[p]) for p in Proccess}

    avarage_waiting_time  = sum(waiting_time.values())/len(waiting_time.values())
    total_turn_around_time = sum(turn_around_time.values())
    return {"schema": Core, "AWT": avarage_waiting_time, "TTAT":total_turn_around_time}

def rr_result(proccess_data, core_no):
    proccess_data.sort(key=lambda x: x[0]) #sort the proccesses by arrival time
    Proccess = init_process_data_structure(proccess_data) #Initialize the process full data structure
    Core = init_core_data_structure(core_no) #INITIALIZE THE CORES

    max_quantum = max([p[2] for p in Proccess.values()])

    best_awt = float('inf')
    best_ttat = 0
    best_q_schema = []
    AWT_Bar = []
    TTAT_Bar = []

    #Find best posible quantum
    for q in range(1, max_quantum + 1):
        result = schedule_single_quantum(deepcopy(Proccess), deepcopy(Core), q) #pass a copy of the dataset because it gets mutated
        #Find the schema with the best waiting time
        if result["AWT"] < best_awt:
            best_awt = result["AWT"]
            best_q_schema = [result["schema"], q]
            best_ttat = result["TTAT"]
        result = 0

    step = max_quantum/35
    step = int(step)

    quantum_range = range(step,max_quantum + 1,step)
    quantum_range = list(quantum_range)

    #find the awt and ttat for the best quantum and add that quantum to the range
    for i,q in enumerate(copy(quantum_range)):
        result = schedule_single_quantum(deepcopy(Proccess), deepcopy(Core), q) #pass a copy of the dataset because it gets mutated
        AWT_Bar.append(result["AWT"])
        TTAT_Bar.append(result["TTAT"])
        if q < best_q_schema[1] and (len(quantum_range) == i + 1 or quantum_range[i+1] > best_q_schema[1]):
            AWT_Bar.insert(i+1, best_awt)
            TTAT_Bar.insert(i+1,best_ttat)
            quantum_range.insert(i+1, best_q_schema[1])
    
    if not (max_quantum in quantum_range): #add the last quantum to the range
        last_result = schedule_single_quantum(deepcopy(Proccess), deepcopy(Core), max_quantum)
        AWT_Bar.append(last_result["AWT"])
        TTAT_Bar.append(last_result["TTAT"])
        quantum_range.append(max_quantum)
    
    return { #to be passed to the gantt chart
        "max_quantum" : max_quantum,
        "quantum_range" : quantum_range,
        "AWT_Bar": AWT_Bar,
        "TTAT_Bar": TTAT_Bar,
        "best_q_schema": best_q_schema,
    }
