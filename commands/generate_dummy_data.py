import subprocess

subprocess.call("python3 manage.py generate_users 10", shell=True)
subprocess.call("python3 manage.py generate_products 30", shell=True)
