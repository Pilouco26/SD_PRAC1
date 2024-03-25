import subprocess
import os

def run_nameserver():
    # Run nameserver.py
    try:
        subprocess.Popen(['python3', 'nameserver.py'])
        print("nameserver.py started successfully.")
    except Exception as e:
        print(f"Error starting nameserver.py: {e}")

def run_receive_rmq():
    # Run receiveRMQ.py
    try:
        subprocess.Popen(['python3', 'receiveRMQ.py'])
        print("receiveRMQ.py started successfully.")
    except Exception as e:
        print(f"Error starting receiveRMQ.py: {e}")

if __name__ == "__main__":
    # Change directory to where the scripts are located
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    # Run both scripts concurrently
    run_nameserver()
    run_receive_rmq()
    # Infinite loop to keep the window open (use with caution)
    while True:
        pass
