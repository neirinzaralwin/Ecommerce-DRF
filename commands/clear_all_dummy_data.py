import subprocess

subprocess.call("python3 manage.py clear_users", shell=True)
subprocess.call("python3 manage.py clear_products", shell=True)
