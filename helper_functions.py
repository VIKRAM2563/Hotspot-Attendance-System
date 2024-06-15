import subprocess
# Import subprocess for Wi-Fi network scanning

# Create a dictionary to keep track of the number of times each bench has been occupied
benches = {}
total_rows = 9
total_columns = 5


def scan_wifi_networks():

    """Scans for available Wi-Fi networks and returns a list of their names."""

    devices = subprocess.check_output(['netsh', 'wlan', 'show', 'network'])
    devices = devices.decode('ascii','ignore') # Ignore needed to not crash program in cases of emoji SSIDs
    devices = devices.replace("\r", "") 
    return devices


def print_bench_matrix(benches):
    """Prints a matrix of the students present at each bench.

    Args:
        benches: A dictionary that maps benches to the number of students present at each bench.

    Returns:
        None.
    """
    matrix = []
    for i in range(total_rows):
        row = []
        for j in range(total_columns):
            bench = (i+1, j+1)
            if bench in benches:
                count = benches[bench]['count']
                if count == 1:
                    row.append("?")
                elif count == 2:
                    row.append("✓")

            else:
                row.append("X")
                

        matrix.append(row)

    # Print the matrix
    print("\n".join([" ".join(row) for row in matrix]))




def process_network_list(network_list):
    """Processes a list of Wi-Fi networks and returns a dictionary that maps each network to a tuple of its coordinates.

    Args:
        network_list: A list of Wi-Fi networks.

    Returns:
        A dictionary that maps Wi-Fi networks to their coordinates.
    """
    benches = {}
    filtered_network_list = []
    
    network_list = network_list.split("\n")
    
    for network in network_list:
        if network.startswith("SSID"):
            ssid = network.split(":")[1].strip()
            
            if ssid.startswith("1BY") and len(ssid) >= 6:
                try:
                    num_str = ssid[3:6]
                    num_int = int(num_str)
                    
                    if num_int >= 0:
                        if ssid.startswith("1BY") and ssid not in filtered_network_list:
                            filtered_network_list.append(ssid)
                            
                            bench_coordinate = int(ssid[-2:])
                            x = bench_coordinate // 10
                            y = bench_coordinate % 10
                            bench = (x, y)
                            
                            if bench in benches:
                                benches[bench]['count'] += 1
                                benches[bench]['ssids'].append(ssid)
                                
                                if benches[bench]['count'] > 2:
                                    print(f"Possible attendance issue at bench {bench}. SSIDs: {benches[bench]['ssids']}")
                                    for ssid in benches[bench]['ssids']:
                                        if ssid in filtered_network_list:
                                            filtered_network_list.remove(ssid)
                            else:
                                benches[bench] = {'count': 1, 'ssids': [ssid]}
                
                except ValueError:
                    print(f"Warning: '{num_str}' is not a convertible integer, skipping...")

    return benches, filtered_network_list

def count_empty_benches(benches, total_rows, total_columns):
    """Counts the number of empty benches in a dictionary that maps benches to the number of students present at each bench.

    Args:
        benches: A dictionary that maps benches to the number of students present at each bench.
        total_rows: The total number of rows in the bench matrix.
        total_columns: The total number of columns in the bench matrix.

    Returns:
        The number of empty benches.
    """

    empty_benches = 0
    
    for i in range(total_rows):
        for j in range(total_columns):
            bench = (i + 1, j + 1)
            if bench in benches:
                count = benches[bench]['count']
                if count == 1 or count == 2:
                    continue
            else:
                empty_benches += 1
    
    return empty_benches

def get_present_students(filtered_network_list):
    """Returns a list of the students present in a list of Wi-Fi networks.

    Args:
        filtered_network_list: A list of Wi-Fi networks.

    Returns:
        A list of students present.
    """
    three_char_list = [network[3:6] for network in filtered_network_list]
    return three_char_list

def get_absent_students(three_char_list):
    """Returns a list of the students absent in a list of Wi-Fi networks.

    Args:
        three_char_list: A list of Wi-Fi networks.

    Returns:
        A list of students absent.
    """   
    three_char_int_list = [int(network) for network in three_char_list]
    
    absent_numbers = []
    
    for i in range(133, 200):
        if i not in three_char_int_list:
            absent_numbers.append(i)
    
    return absent_numbers