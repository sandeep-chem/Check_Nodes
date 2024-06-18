#!/usr/bin/env python3

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