# monitor-system-performance
monitor system performance and log CPU and memory usage over time.

## How to Use the Script:

1.  **Save the Code:** Save the code above as a Python file (e.g., `system_monitor.py`).
2.  **Install `psutil`:** If you don't have it installed, open your terminal or command prompt and run:
    ```bash
    pip install psutil
    ```
3.  **Run the Script:** Execute the script from your terminal:
    ```bash
    python system_monitor.py
    ```

    You can also use command-line arguments to customize its behavior:
    * **Specify Log File:**
        ```bash
        python system_monitor.py -f my_custom_log.txt
        ```
    * **Specify Logging Interval (in seconds):**
        ```bash
        python system_monitor.py -i 10  # Log every 10 seconds
        ```
    * **Specify Monitoring Duration (in seconds):**
        ```bash
        python system_monitor.py -d 60  # Monitor for 60 seconds
        ```
    * **Combine Arguments:**
        ```bash
        python system_monitor.py -f metrics.log -i 2 -d 300
        ```

4.  **View Logs:**
    * The script will print the CPU and memory usage to the console in real-time.
    * The logs will also be saved to the specified log file (default: `system_performance.log`) in the same directory where you run the script. Each log entry will be timestamped.

    **Example Log Output (in `system_performance.log` and console):**
    ```
    2025-05-13 04:05:10 - CPU: 12.5%, Memory: 45.8%
    2025-05-13 04:05:15 - CPU: 10.2%, Memory: 46.1%
    2025-05-13 04:05:20 - CPU: 15.0%, Memory: 45.9%
    ...
    ```

5.  **Stop the Script:** If you run it without a duration (indefinitely), you can stop it by pressing `Ctrl+C` in the terminal.

## Explanation:

* **`import psutil`**: This library is used to fetch system details like CPU and memory usage.
* **`import time`**: Used for pausing the script (`time.sleep()`) between log entries and for calculating the duration.
* **`import logging`**: Python's built-in module for flexible event logging.
* **`from datetime import datetime`**: Used to get the current timestamp for log entries (though `logging` module can also do this with `%(asctime)s`).
* **`import argparse`**: Used to create a command-line interface for specifying options like log file, interval, and duration.
* **`DEFAULT_LOG_FILE`, `DEFAULT_INTERVAL`, `DEFAULT_DURATION`**: Constants for default settings.
* **`get_system_stats()`**:
    * `psutil.cpu_percent(interval=1)`: Returns the current system-wide CPU utilization as a percentage. The `interval=1` argument means it will compare CPU times over a 1-second interval, providing a more accurate reading than `interval=None` or `0`.
    * `psutil.virtual_memory()`: Returns a named tuple with various memory statistics.
    * `memory_info.percent`: Extracts the percentage of memory usage from the tuple.
* **`setup_logging(log_file)`**:
    * `logging.basicConfig()`: Configures the root logger.
        * `filename=log_file`: Specifies the file to which logs will be written.
        * `level=logging.INFO`: Sets the minimum severity level of messages to be logged (DEBUG, INFO, WARNING, ERROR, CRITICAL).
        * `format='%(asctime)s - CPU: %(cpu)s%%, Memory: %(memory)s%%'`: Defines the format of the log messages. `%(asctime)s` is the time of the log record. `%(cpu)s` and `%(memory)s` are custom fields we will pass.
        * `datefmt='%Y-%m-%d %H:%M:%S'`: Sets the format for the `asctime`.
    * A `StreamHandler` is added to also output logs to the console.
* **`main()`**:
    * Sets up argument parsing using `argparse`.
    * Calls `setup_logging()` with the chosen log file.
    * Enters an infinite `while True` loop (or runs for the specified duration).
    * Inside the loop:
        * Calls `get_system_stats()` to get current CPU and memory usage.
        * `logging.info("", extra={'cpu': cpu, 'memory': mem})`: Logs the data. The `extra` dictionary allows us to pass custom fields to the log formatter.
        * Checks if the specified `duration` has been reached and breaks the loop if it has.
        * `time.sleep(args.interval)`: Pauses the script for the specified interval before the next reading.
    * Handles `KeyboardInterrupt` (when you press `Ctrl+C`) to gracefully stop the script.
    * Logs any other exceptions that might occur.
* **`if __name__ == "__main__":`**: Ensures that `main()` is called only when the script is executed directly (not when imported as a module).