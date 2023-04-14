import os
import subprocess

# Use the below lists to index into specific configuration parameters
LQEntries_List = [32, 64]
SQEntries_List = [32, 64]
l1d_size_List = ["32kB", "64kB"]
l1i_size_List = ["8kB", "16kB"]
l2_size_List = ["256kB", "512kB"]
bp_type_List = ["TournamentBP", "BiModeBP"]
ROBEntries_List = [128, 192]
numIQEntries_List = [16, 64]

for i in range(250, 256):
	# Get the binary of the index to index into the lists
    bin_i = [int(j) for j in list(format(i, '08b'))]
    
    # Get the specific configuration parameters
    LQEntries = LQEntries_List[bin_i[0]]
    SQEntries = SQEntries_List[bin_i[1]]
    l1d_size = l1d_size_List[bin_i[2]]
    l1i_size = l1i_size_List[bin_i[3]]
    l2_size = l2_size_List[bin_i[4]]
    bp_type = bp_type_List[bin_i[5]]
    ROBEntries = ROBEntries_List[bin_i[6]]
    numIQEntries = numIQEntries_List[bin_i[7]]
    
    # Create a new output folder for each new type of configuration
    output_folder = f"~/gem5/configs/source_code/outputs/output_LQEntries_{LQEntries}_SQEntries_{SQEntries}_l1d_size_{l1d_size}_l1i_size_{l1i_size}_l2_size_{l2_size}_bp_type_{bp_type}_ROBEntries_{ROBEntries}_numIQEntries_{numIQEntries}"
    
    if not os.path.exists(os.path.expanduser("~/gem5/configs/source_code/outputs")):
        os.makedirs(os.path.expanduser("~/gem5/configs/source_code/outputs"))
        
    if not os.path.exists(os.path.expanduser(output_folder)):
        os.makedirs(os.path.expanduser(f"{output_folder}"))
    
    # Command to simluate a system with the specified configurations as paased via command line arguments and parsed using argparse
    command = [
                os.path.expanduser("~/gem5/build/X86/gem5.opt"), 
                "-d", os.path.expanduser(output_folder), 
                os.path.expanduser("~/gem5/configs/source_code/config.py"), 
                "-c", os.path.expanduser("~/gem5/configs/source_code/sieve"),
                f"--LQEntries={LQEntries}",
                f"--SQEntries={SQEntries}",
                f"--l1d_size={l1d_size}",
                f"--l1i_size={l1i_size}",
                f"--l2_size={l2_size}",
                f"--bp_type={bp_type}",
                f"--ROBEntries={ROBEntries}",
                f"--numIQEntries={numIQEntries}"
            ]
    
    print("\n\n****************************************************************\n\n")
    print("Index : ", i)
    print("Starting simulation with command", " ".join(command), flush=True)
    
    command_output = subprocess.run(command, capture_output=True)
    
    with open(os.path.expanduser(f"{output_folder}/command_output.txt"), "w") as f:
        print(command_output.stdout, file=f)
            
    print("Simulation finished with return code", command_output.returncode, flush=True)
    print("\n\n****************************************************************\n\n")
    if command_output.returncode!=0:
        break

