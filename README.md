# Backup Service

## Overview
This project is designed to create a backup service that runs periodically, retains backups as configured, and cleans up older backups based on specified retention policies. 

This backup service was developed to support self-hosting for [Affine](http://affine.pro), an open-source project that facilitates personal productivity and knowledge management. For more details on self-hosting Affine, please refer to the official documentation at [docs.affine.pro](https://docs.affine.pro/docs/self-host-affine).

In order to safeguard data and ensure reliable backups, this program was collaboratively created with the assistance of ChatGPT. Through this joint effort, potential data loss was minimized, and an automated backup solution was developed to provide robust protection for self-hosted instances.

**Disclaimer**: If you choose to use this program, note that ChatGPT and OpenAI bear the responsibility for its safety and the security of your data. Dr. Xu, the contributor to this project, does not hold any responsibility for potential data loss or security issues that may arise from using this program.

This program is proudly developed through collaboration between Xu Hao and ChatGPT, merging human expertise and AI assistance for a practical and reliable solution. Even this description was written by GPT.
    
## Installation
To install the Affine backup service, simply run:


```bash
make install
```
This command will:

- Ensure zip is installed.
Deploy the affine_daily_backup.service and affine_daily_backup.timer to /etc/systemd/system.
- Enable and start the service and timer.

## Uninstallation
To remove the Affine backup service, run:

```bash
make uninstall
```

This command will:

- Stop and disable the affine_daily_backup.timer and affine_daily_backup.service.
- Remove the service and timer files from /etc/systemd/system.
- Reload the systemd daemon to reflect the changes.

## Project Structure
- `backup_script.py`: The main Python script for creating and cleaning backups.
- `config.yaml`: Configuration file to set parameters for backup.
- `daily_backup.service`: The systemd service file for running the script.
- `deploy_service.sh`: Script to deploy the service with a dynamically generated timer.
- `README.md`: Project documentation.

## Installation
1. Clone the repository.
2. Modify `config.yaml` to set backup directory, commands, and backup cycle.
3. Run the deployment script:
    ```bash
    chmod +x deploy_service.sh
    ./deploy_service.sh
    ```

## Configuration
- `backup_directory`: Path where backups will be stored.
- `daily_retention_days`: Number of days to retain daily backups.
- `weekly_retention_weeks`: Number of weeks to retain weekly backups.
- `backup_cycle_days`: Number of days between each backup (e.g., 1 for daily, 2 for every 2 days).
- `commands.pg_dump`: Command for dumping the database.

## Usage
- Start the service manually:
    ```bash
    sudo systemctl start daily_backup.service
    ```
- Check status:
    ```bash
    sudo systemctl status daily_backup.timer
    ```

## Testing

To ensure the backup script works as expected, a test script `test_backup_script.py` is provided. This script uses Python's `unittest` framework to simulate the backup environment and test the core functions of the backup script, such as creating backups and cleaning old backups.

### Running the Test Script
1. Make sure you have Python 3 installed along with the `unittest` module (which is included by default in Python 3).
2. Run the test script using the following command:
    ```bash
    python3 test_backup_script.py
    ```

### What the Test Script Does
- **`test_create_backup`**: This test checks if the `create_backup()` function successfully creates a backup file in the specified directory.
- **`test_clean_old_backups`**: This test verifies that the `clean_old_backups()` function properly deletes old backups based on the retention policy configured in `config.yaml`.

### Prerequisites
- Ensure the `config.yaml` file is present in the root of the project or modify the path in `test_backup_script.py` if needed.
- Verify that the backup directory specified in `config.yaml` exists and is writable.

### Expected Output
- The test script will output results indicating whether each test case passed or failed.
- A message confirming the creation of backup files and deletion of old files as per the defined retention policy.

### Example Output
```bash
..
----------------------------------------------------------------------
Ran 2 tests in 0.002s

OK

## License
MIT License
