#!/usr/bin/env python3

import sys
from slurm_functions import get_available_partitions, get_partition_info, get_node_info

def select_partition(partition_names):
    """
    Prompts user to select a SLURM partition.

    Args:
        partition_names (list): List of dictionaries containing partition information.

    Returns:
        The name of the selected partition (str).
    """
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

    return selected_partition

def main():
    # Get available partition names
    partition_names = get_available_partitions()

    if not partition_names:
        print("No partitions available.")
        sys.exit(1)

    # Select a partition
    selected_partition = select_partition(partition_names)

    # Get information for the selected partition
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

if __name__ == "__main__":
    main()