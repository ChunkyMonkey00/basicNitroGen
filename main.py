import threading
import requests
import random
import string
import time
import signal

CONFIRM_URL = "https://discord.com/api/v8/entitlements/gift-codes/"
working_codes = []
should_sleep = False  # Global flag to indicate if all threads should sleep

num_threads =  20
total_responses =  0

def signal_handler(signal, frame):
    global total_responses, start_time
    elapsed_time = time.time() - start_time
    print("Average CPS of session: "+str(total_responses/elapsed_time))
    raise SystemExit(0)

signal.signal(signal.SIGINT, signal_handler)

def generate_random_code(length=18):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))

def check_code(code):
    global should_sleep, num_responses, total_responses  # Declare should_sleep and num_responses as global
    response = requests.post(CONFIRM_URL + code, headers = {'User-agent': 'dcng   0.1'})
    if response.status_code ==   200:
        print(f"Code {code} is working")
        working_codes.append(code)

        raise SystemExit(0)
    elif response.status_code ==   429:
        if not should_sleep:
            should_sleep = True
    else:
        total_responses +=  1

def code_checker(num_threads):
    global should_sleep
    while True:
        if should_sleep:  # If the flag is True, sleep and then reset the flag
            time.sleep(1)
            should_sleep = False
        code = generate_random_code()
        check_code(code)
        time.sleep(0.1)  # Add a small delay between checks to avoid overloading the computer

# Get user input for the number of threads
while True:
    try:
        num_threads = int(input("Enter the number of threads to use: "))
        break
    except ValueError:
        print("Please enter a valid integer.")

# Record the start time
start_time = time.time()

# Start code checking threads
checker_threads = []
for _ in range(num_threads):
    checker_thread = threading.Thread(target=code_checker, args=(num_threads,))
    checker_threads.append(checker_thread)
    checker_thread.start()

# Start the CPS printing thread
cps_thread = threading.Thread()
cps_thread.start()

# Stop the code checking threads
for checker_thread in checker_threads:
    checker_thread.join()

# Stop the CPS printing thread
cps_thread.join()
