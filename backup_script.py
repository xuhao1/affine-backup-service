import os
import sys
import datetime
import subprocess
import yaml
import logging

# 设置日志配置
logging.basicConfig(
    filename='backup_script.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def load_config(config_path='config.yaml'):
    if not os.path.exists(config_path):
        logging.error(f"Configuration file {config_path} not found.")
        raise FileNotFoundError(f"Configuration file {config_path} not found.")
    logging.info(f"Loading configuration from {config_path}")
    with open(config_path, 'r') as file:
        config = yaml.safe_load(file)
    return config

def create_backup(config_path='config.yaml'):
    config = load_config(config_path)
    print(config)
    backup_dir = config['backup_directory']
    data_dir = config['data_directory']
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    backup_filename = f"affine-note-bk-{timestamp}.zip"
    # Check if backup_dir directory exists, if not, create it
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir, exist_ok=True)
        logging.info(f"Data directory {data_dir} created.")
    backup_path = os.path.join(backup_dir, backup_filename)

    try:
        logging.info("Starting pg_dump command...")
        subprocess.run(config["commands"]['pg_dump'], shell=True, check=True)
        logging.info("pg_dump command completed successfully.")
        
        logging.info(f"Creating zip archive: {backup_path}")
        subprocess.run(f"sudo zip -r {backup_path} {data_dir}", shell=True, check=True)
        logging.info(f"Backup archive {backup_path} created successfully.")
        
        subprocess.run(f"sudo chmod a+r {backup_path}", shell=True, check=True)
        logging.info(f"Permissions set for {backup_path}")
        
    except subprocess.CalledProcessError as e:
        logging.error(f"Backup failed during command execution: {e}")
        print(f"Backup failed: {e}")

    clean_old_backups(backup_dir, config['daily_retention_days'], config['weekly_retention_weeks'])

def clean_old_backups(backup_dir, daily_retention_days, weekly_retention_weeks):
    logging.info(f"Starting cleanup in {backup_dir}...")
    backups = sorted([f for f in os.listdir(backup_dir) if f.startswith("affine-note-bk-")], reverse=True)

    if len(backups) > daily_retention_days:
        daily_backups = backups[daily_retention_days:]
        for backup in daily_backups:
            backup_path = os.path.join(backup_dir, backup)
            if datetime.datetime.now() - datetime.datetime.strptime(backup[14:33], "%Y-%m-%d-%H-%M-%S") > datetime.timedelta(days=7):
                os.remove(backup_path)
                logging.info(f"Removed old backup: {backup_path}")

    weekly_backups = [backups[i] for i in range(0, len(backups), 7)]
    if len(weekly_backups) > weekly_retention_weeks:
        weekly_backups = weekly_backups[weekly_retention_weeks:]
        for backup in weekly_backups:
            backup_path = os.path.join(backup_dir, backup)
            os.remove(backup_path)
            logging.info(f"Removed old weekly backup: {backup_path}")

    logging.info("Cleanup completed.")

if __name__ == "__main__":
    config_path = sys.argv[1] if len(sys.argv) > 1 else 'config.yaml'
    try:
        create_backup(config_path)
        logging.info("Backup process completed successfully.")
    except Exception as e:
        logging.error(f"Backup process failed: {e}")
        print(f"Backup process failed: {e}")
