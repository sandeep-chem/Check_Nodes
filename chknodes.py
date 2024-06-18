#!/usr/bin/env python3

import sys
import subprocess

def get_available_partitions():
    """
    Retrieves a list of available SLURM partitions from scontrol.

    Returns:
        A list of dictionaries, each containing partition information.
    """
    command = 'scontrol show partitions'
    output = subprocess.run(command, shell=True, capture_output=True, text=True)

    if output.returncode != 0:
        print("Failed to retrieve available partitions.")
        print(f"Command: {command}")
        print(output.stderr)
        return []

    partition_info = []
    current_partition = {}
    output_lines = output.stdout.splitlines()
    for line in output_lines:
        if line.startswith("PartitionName="):
            if current_partition:
                partition_info.append(current_partition)
                current_partition = {}

        segments = line.split()
        for segment in segments:
            if '=' in segment:
                key, value = segment.split('=', 1)
                current_partition[key.strip()] = value.strip()

    if current_partition:
        partition_info.append(current_partition)

    return partition_info

def get_partition_info(partition_name):
    """
    Retrieves SLURM partition information for a given partition name.

    Args:
        partition_name (str): Name of the SLURM partition.

    Returns:
        A dictionary containing partition information.
    """
    command = f'scontrol show partition {partition_name}'
    output = subprocess.run(command, shell=True, capture_output=True, text=True)
    
    if output.returncode != 0:
        print(f"Failed to get partition information for partition '{partition_name}'.")
        print(f"Command: {command}")
        print(output.stderr)
        return None

    partition_info = {}
    output_lines = output.stdout.splitlines()
    for line in output_lines:
        segments = line.split()
        for segment in segments:
            if '=' in segment:
                key, value = segment.split('=', 1)
                partition_info[key.strip()] = value.strip()

    return partition_info

def get_node_info(node_list):
    """
    Retrieves SLURM node information for a given node list.

    Args:
        node_list (str): Comma-separated list of node names.

    Returns:
        A list of dictionaries, each containing node information.
    """
    command = f'scontrol show node {node_list}'
    output = subprocess.run(command, shell=True, capture_output=True, text=True)

    if output.returncode != 0:
        print("Failed to get node information.")
        print(f"Command: {command}")
        print(output.stderr)
        return None

    node_info = []
    current_node = {}
    output_lines = output.stdout.splitlines()
    for line in output_lines:
        if line.startswith("NodeName="):
            if current_node:
                node_info.append(current_node)
                current_node = {}

        segments = line.split()
        for segment in segments:
            if '=' in segment:
                key, value = segment.split('=', 1)
                current_node[key.strip()] = value.strip()

    if current_node:
        node_info.append(current_node)

    return node_info    

if __name__ == "__main__":
    # Get available partition names
    partition_names = get_available_partitions()

    if not partition_names:
        print("No partitions available.")
        sys.exit(1)

    selected_partition = None

    if len(sys.argv) > 1:
        selected_partition_arg = sys.argv[1]
        if selected_partition_arg in [partition['PartitionName'] for partition in partition_names]:
            selected_partition = selected_partition_arg
        else:
            print("Wrong partition name chosen. Available partitions are:")
            for i, partition in enumerate(partition_names, start=1):
                print(f"{i}. {partition['PartitionName']}")
            while True:
                try:
                    choice = int(input("\nEnter the number of the partition you want to retrieve information for: "))
                    if 1 <= choice <= len(partition_names):
                        selected_partition = partition_names[choice - 1]['PartitionName']
                        break
                    else:
                        print("Invalid choice. Please enter a number within the range.")
                except ValueError:
                    print("Invalid input. Please enter a valid number.")

    if not selected_partition:
        print("Available Partitions:")
        for i, partition in enumerate(partition_names, start=1):
            print(f"{i}. {partition['PartitionName']}")

        while True:
            try:
                choice = int(input("\nEnter the number of the partition you want to retrieve information for: "))
                if 1 <= choice <= len(partition_names):
                    selected_partition = partition_names[choice - 1]['PartitionName']
                    break
                else:
                    print("Invalid choice. Please enter a number within the range.")
            except ValueError:
                print("Invalid input. Please enter a valid number.")

    selected_partition_info = get_partition_info(selected_partition)

    if selected_partition_info:
        print(f"\nNode status for '{selected_partition}':")

        node_list = selected_partition_info.get("Nodes", "")
        
        if node_list:
            node_info = get_node_info(node_list)
            if node_info:
                keys = ["NodeName", "CPUAlloc", "CPUEfctv", "CPUTot", "CPULoad"]
                for node in node_info:
                    node_info_str = " | ".join(f"{key} = {node.get(key, '')}" for key in keys)
                    print(node_info_str)
