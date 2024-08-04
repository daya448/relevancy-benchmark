import subprocess
import time
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def run_script(script_name):
    try:
        logging.info(f'Starting {script_name}...')
        subprocess.run(['python3', script_name], check=True)
        logging.info(f'Completed {script_name}.')
    except subprocess.CalledProcessError as e:
        logging.error(f'Error running {script_name}: {e}')

def main():
    logging.info('Generating requests...')
    run_script('generate_rank_eval_requests.py')

    logging.info('Running benchmark...')
    run_script('runBenchmark.py')

    logging.info('Output is generated successfully in the benchmark_output file.')

if __name__ == '__main__':
    main()
