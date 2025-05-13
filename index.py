import psutil
import time
import logging
from datetime import datetime
import argparse

# --- Configuration ---
DEFAULT_LOG_FILE = 'system_performance.log'
DEFAULT_INTERVAL = 5  # seconds
DEFAULT_DURATION = None # seconds (None means indefinite)

def get_system_stats():
    """Retrieves current CPU and memory usage."""
    cpu_usage = psutil.cpu_percent(interval=1)  # The interval is important for accuracy
    memory_info = psutil.virtual_memory()
    memory_usage = memory_info.percent
    return cpu_usage, memory_usage

def setup_logging(log_file):
    """Configures logging to write to a specified file."""
    logging.basicConfig(
        filename=log_file,
        level=logging.INFO,
        format='%(asctime)s - CPU: %(cpu)s%%, Memory: %(memory)s%%',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    # Add a handler to also print to console
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - CPU: %(cpu)s%%, Memory: %(memory)s%%')
    console_handler.setFormatter(formatter)
    logging.getLogger().addHandler(console_handler)

    logging.info("Starting system performance monitoring.")
    print(f"Logging to: {log_file}")

def main():
    """Main function to monitor and log system performance."""
    parser = argparse.ArgumentParser(description="Monitor system CPU and memory usage.")
    parser.add_argument(
        "-f", "--file",
        default=DEFAULT_LOG_FILE,
        help=f"Log file name (default: {DEFAULT_LOG_FILE})"
    )
    parser.add_argument(
        "-i", "--interval",
        type=int,
        default=DEFAULT_INTERVAL,
        help=f"Logging interval in seconds (default: {DEFAULT_INTERVAL})"
    )
    parser.add_argument(
        "-d", "--duration",
        type=int,
        default=DEFAULT_DURATION,
        help="Duration of monitoring in seconds (default: run indefinitely until interrupted)"
    )
    args = parser.parse_args()

    setup_logging(args.file)

    start_time = time.time()

    try:
        while True:
            cpu, mem = get_system_stats()
            logging.info("", extra={'cpu': cpu, 'memory': mem})

            if args.duration is not None:
                if (time.time() - start_time) >= args.duration:
                    logging.info(f"Monitoring finished after {args.duration} seconds.")
                    print(f"Monitoring finished after {args.duration} seconds.")
                    break
            time.sleep(args.interval)
    except KeyboardInterrupt:
        logging.info("Monitoring stopped by user.")
        print("\nMonitoring stopped by user.")
    except Exception as e:
        logging.error(f"An error occurred: {e}", exc_info=True)
        print(f"An error occurred: {e}")
    finally:
        logging.info("System performance monitoring ended.")

if __name__ == "__main__":
    main()