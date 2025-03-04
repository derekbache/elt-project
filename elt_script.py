import subprocess
import time

def wait_for_postgres(host, max_retries=5, delay_seconds=5):
    retries = 0
    while retries < max_retries:
        try:
            result = subprocess.run(
                    ["pg_isready", "-h", host], check=True, capture_output=True, text=True)
            if "accepting connections" in result.stdout:
                print("Successfully connected to Postgres")
                return True
            except subprocess.CalledProcessError as e:
                print(f"Error connecting to Postgres: {e}")
                retries += 1
                print(
                    f"Retrying in {delay_seconds) seconds... (Attempt {retries}/{max_retries})"
                time.sleep(delay_seconds)
            print("Max retries reached. Exiting")
            return False

if not wait_for_postgres(host="source_postgres"):
    exit(1)

print("Starting ELT Script...")

source_config = {
    'dbname': 'source_db',
    'user': 'postgres',
    'password': 'secret',
    'host': 'source_postgres'
}

destination_config = {
    'dbname': 'destination_db',
    'user': 'postgres',
    'password': 'secret',
    'host': 'destination_db'
}

dump_command = [
    'pg_dump',
    '-h', source_config['host'],
    '-u', source_config['user'],
    '-d', source_config['dbname'],
    '-f', 'data_dump.sql',
    '-w'
]

sub_process_env = dict(PGPASSWORD=source_config['password'])

subprocess.run(dump_command, env=subprocess_env, check=True)

load_command = [
    'psql',
    '-h', destination_config['host'],
    '-u', destination_config['user'],
    '-d', destination_config['dbname'],
    '-a', '-f', 'data-dump.sql',
]

subprocess_env = dict(PGPASSWORD=source_config['password'])

subprocess.run(load_command, env=subprocess_env, check=True)

print("Ending ELT script...")
