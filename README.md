# chknodes
# Overview

This repository contains Python scripts to interact with [SLURM]([url](https://slurm.schedmd.com/quickstart.html)) clusters, specifically for querying partition and node information.

# Files
chknodes.py: The main script to run the program from the command line. It allows users to specify a SLURM partition name and retrieves detailed node information.
slurm_functions.py: Contains modular functions for querying SLURM partitions and nodes using subprocess calls to scontrol commands. Functions include:
    get_available_partitions(): Retrieves a list of available SLURM partitions.
    get_partition_info(partition_name): Retrieves detailed information about a specific SLURM partition.
    get_node_info(node_list): Retrieves information about nodes in a given SLURM partition.

# Usage
Running the Program

To use chknodes, execute main.py from the bash command line with a SLURM partition name:

    ./chknodes.py {partition_name}

Replace {partition_name} with the name of the SLURM partition you want to inspect.

# Functionality

Partition Information: Retrieves and displays details about the selected SLURM partition, including node names and their current status (e.g., CPU allocation, efficiency, and load).

Interactive Selection: If no partition name is provided as an argument, the program interactively lists available partitions and prompts the user to select one.

# Requirements

Python 3
SLURM cluster with scontrol command accessible from the environment where the script is executed.

# License

This project is licensed under the GPL 3.0 License.

Feel free to adjust the sections and details according to your specific project structure and preferences. This description provides a clear overview of what the repository contains, how to use it, and the functionality it offers.

Sandeep Dash
