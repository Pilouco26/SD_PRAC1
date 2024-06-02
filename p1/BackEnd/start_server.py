import subprocess
import os

def start_servers():
    # Set the PYTHONPATH environment variable
    os.environ['PYTHONPATH'] = r"C:\Users\migue\PycharmProjects\sdpract\p1\BackEnd;" + os.environ.get('PYTHONPATH', '')

    # Path to the Python interpreter in the virtual environment
    python_interpreter = r"C:\Users\migue\PycharmProjects\sdpract\.venv\Scripts\python.exe"

    # Start servidor.py
    servidor_process = subprocess.Popen([python_interpreter, 'servidor.py'], env=os.environ)
    print(f"Started servidor.py with PID: {servidor_process.pid}")

    # Start nameServer.py
    name_server_process = subprocess.Popen([python_interpreter, 'nameServer.py'], env=os.environ)
    print(f"Started nameServer.py with PID: {name_server_process.pid}")

    # Wait for the processes to complete
    servidor_process.wait()
    name_server_process.wait()

if __name__ == "__main__":
    start_servers()
