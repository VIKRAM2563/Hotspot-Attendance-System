import time
# Import the time module for time.sleep

from helper_functions import scan_wifi_networks, process_network_list, count_empty_benches, print_bench_matrix, get_present_students, get_absent_students
from helper_functions import total_columns, total_rows



while True:
  """
  Continuously scans for available Wi-Fi networks and prints information about the students present at each bench.

  Args:
    None.

  Returns:
    None.
  """

  benches = {}
  """
  Creates an empty dictionary to store the number of students present at each bench.
  """

  network_list = scan_wifi_networks()
  """
  Scans for available Wi-Fi networks and returns a list of their names.
  """

  if network_list is None:
    break
  """
  If the scan returns an empty list, the loop breaks.
  """

  benches, filtered_network_list = process_network_list(network_list)
  """
  Processes the list of Wi-Fi networks and returns a dictionary that maps each network to a tuple of its coordinates.
  """

  empty_benches = count_empty_benches(benches, total_rows, total_columns)
  """
  Counts the number of empty benches in the dictionary.
  """

  print("Empty benches:", empty_benches)
  """
  Prints the number of empty benches.
  """

  print_bench_matrix(benches)
  """
  Prints a matrix of the students present at each bench.
  """

  present_students = get_present_students(filtered_network_list)
  """
  Returns a list of the students present in a list of Wi-Fi networks.
  """

  print("Students present: ")
  print(present_students)
  """
  Prints a list of the students present.
  """

  absent_students = get_absent_students(present_students)
  """
  Returns a list of the students absent in a list of Wi-Fi networks.
  """

  print("Absent students: ")
  print(absent_students)
  """
  Prints a list of the students absent.
  """

  time.sleep(10)
  """
  Pauses the loop for 10 seconds.
  """
