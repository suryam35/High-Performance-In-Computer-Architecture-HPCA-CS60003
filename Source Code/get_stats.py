import matplotlib.pyplot as plt
import csv

LQEntries_List = [32, 64]
SQEntries_List = [32, 64]
l1d_size_List = ["32kB", "64kB"]
l1i_size_List = ["8kB", "16kB"]
l2_size_List = ["256kB", "512kB"]
bp_type_List = ["TournamentBP", "BiModeBP"]
ROBEntries_List = [128, 192]
numIQEntries_List = [16, 64]

def get_stats(file_path, stats_to_get):
    d = {}
    with open(file_path, 'r') as my_file:
        all_lines = my_file.readlines()[2:][:-2]
        for line in all_lines:
            line = line.split()
            if line[0] in stats_to_get:
                d[line[0]] = float(line[1])
    return d

def write_to_csv(name, cpi_values):
    with open(name, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["cpi", "LQ", "SQ", "l1d_size", "l1i_size", "l2_size", "bp", "ROB", "IQ"])
        for element in cpi_values:
            cpi = element[1]
            i = element[0]
            bin_i = [int(j) for j in list(format(i, '08b'))]
            LQEntries = LQEntries_List[bin_i[7]]
            SQEntries = SQEntries_List[bin_i[6]]
            l1d_size = l1d_size_List[bin_i[5]]
            l1i_size = l1i_size_List[bin_i[4]]
            l2_size = l2_size_List[bin_i[3]]
            bp_type = bp_type_List[bin_i[2]]
            ROBEntries = ROBEntries_List[bin_i[1]]
            numIQEntries = numIQEntries_List[bin_i[0]]
            writer.writerow([cpi, LQEntries, SQEntries, l1d_size, l1i_size, l2_size, bp_type, ROBEntries, numIQEntries])


def get_file_paths():
    file_paths = []
    for i in range(0, 256):

        bin_i = [int(j) for j in list(format(i, '08b'))]
        
        LQEntries = LQEntries_List[bin_i[7]]
        SQEntries = SQEntries_List[bin_i[6]]
        l1d_size = l1d_size_List[bin_i[5]]
        l1i_size = l1i_size_List[bin_i[4]]
        l2_size = l2_size_List[bin_i[3]]
        bp_type = bp_type_List[bin_i[2]]
        ROBEntries = ROBEntries_List[bin_i[1]]
        numIQEntries = numIQEntries_List[bin_i[0]]
    
        output_folder = f"outputs/output_LQEntries_{LQEntries}_SQEntries_{SQEntries}_l1d_size_{l1d_size}_l1i_size_{l1i_size}_l2_size_{l2_size}_bp_type_{bp_type}_ROBEntries_{ROBEntries}_numIQEntries_{numIQEntries}"
        file_paths.append((i, output_folder + "/stats.txt"))
    return file_paths

def get_complete(stats_to_get):
    all_list = []
    cpi_values = []
    file_paths = get_file_paths()
    for i in range(len(file_paths)):
        file_path = file_paths[i][1]
        d = get_stats(file_path, stats_to_get)
        all_list.append(d)
        cpi_values.append((file_paths[i][0], d['system.cpu.cpi']))
    
    return all_list, cpi_values

def make_plot(name, xaxis, req_list):
    fig, ax = plt.subplots()
    ax.plot(xaxis, req_list, marker="|")
    ax.set_xlabel('Configuration_number', fontsize = 14)
    ax.set_ylabel(name, fontsize = 14)
    ax.xaxis.set_ticks(xaxis)
    ax.xaxis.set_ticklabels(xaxis)
    fig.savefig(name, dpi=100, bbox_inches='tight')

def get_graphs(all_list, graph_names, stats_to_get):
    for i in range(len(graph_names)):
        name = graph_names[i]
        req_list = []
        for config in all_list:
            req_list.append(config[stats_to_get[i]])
        xaxis = [j for j in range(1, len(req_list)+1)]
        make_plot("graphs/" + name, xaxis, req_list)

def get_top(name, cpi_values):
    cpi_values.sort(key = lambda x: x[1])
    if len(cpi_values) > 10:
        cpi_values = cpi_values[:10]
    write_to_csv(name, cpi_values)

if __name__ == '__main__':
    stats_to_get = ['system.cpu.cpi', 'system.cpu.iew.branchMispredicts', 'system.cpu.iew.predictedNotTakenIncorrect', 'system.cpu.iew.predictedTakenIncorrect', 'system.cpu.ipc', 'system.cpu.branchPred.BTBHitRatio', 'system.cpu.dcache.overallMissLatency::cpu.data', 'system.cpu.dcache.overallMissRate::cpu.data', 'system.cpu.dcache.overallAvgMissLatency::cpu.data', 'system.cpu.icache.overallMissLatency::cpu.inst', 'system.cpu.icache.overallMissRate::cpu.inst', 'system.cpu.icache.overallAvgMissLatency::cpu.inst', 'system.cpu.rob.reads', 'system.cpu.rob.writes', 'system.cpu.iew.lsqFullEvents', 'system.cpu.lsq0.forwLoads', 'system.cpu.lsq0.blockedByCache']
    graph_names = ['cpi', 'mispred_branches_during_execution', 'Number of branches that were predicted not taken incorrectly', 'Number of branches that were predicted taken incorrectly', '– Instructions Per Cycle (IPC)', 'Number of BTB hit percentage', 'Number of overall miss cycles for d-cache', 'miss rate for d-cache', ' average overall miss latency for d-cache', 'Number of overall miss cycles for i-cache', 'miss rate for i-cache', ' average overall miss latency for i-cache','number of ROB accesses read', 'number of ROB accesses write', 'Number of times the LSQ has become full, causing a stall', 'Number of loads that had data forwarded from stores', 'Number of times access to memory failed due to the cache being blocked']
    all_list, cpi_values = get_complete(stats_to_get)
    all_list.sort(key = lambda x: x['system.cpu.cpi'])
    if len(all_list) > 10:
        all_list = all_list[:10]
    get_top('top_10.csv', cpi_values)
    get_graphs(all_list, graph_names, stats_to_get)


    
    