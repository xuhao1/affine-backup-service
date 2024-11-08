import unittest
import os
import shutil
import subprocess
import yaml

from backup_script import create_backup, clean_old_backups

LOG_FILE_PATH = 'backup_script.log'

class TestBackupScript(unittest.TestCase):

    def setUp(self):
        # 创建测试备份和数据目录
        self.test_backup_dir = "/tmp/test_backup_directory"
        self.test_data_dir = "/tmp/test_data_directory"
        os.makedirs(self.test_backup_dir, exist_ok=True)
        os.makedirs(self.test_data_dir, exist_ok=True)

        # 创建一些假数据文件用于测试
        for i in range(5):
            with open(os.path.join(self.test_data_dir, f"test_file_{i}.txt"), 'w') as f:
                f.write(f"This is test file {i}\n")

        # 创建临时 config.yaml 文件
        self.test_config_path = 'test_config.yaml'
        with open(self.test_config_path, 'w') as file:
            file.write(f"""
backup_directory: "{self.test_backup_dir}"
data_directory: "{self.test_data_dir}"
daily_retention_days: 3
weekly_retention_weeks: 2
backup_cycle_days: 1
pg_dump: "echo 'Simulated pg_dump command'"
            """)

    def tearDown(self):
        # 删除测试生成的文件和目录
        if os.path.exists(self.test_backup_dir):
            shutil.rmtree(self.test_backup_dir)
        if os.path.exists(self.test_data_dir):
            shutil.rmtree(self.test_data_dir)
        if os.path.exists(self.test_config_path):
            os.remove(self.test_config_path)

    def print_log(self):
        """Prints the content of the log file if it exists."""
        if os.path.exists(LOG_FILE_PATH):
            print("\n--- Log File Content ---")
            with open(LOG_FILE_PATH, 'r') as log_file:
                print(log_file.read())
            print("--- End of Log File ---")

    def test_create_backup(self):
        try:
            # 在调用 create_backup 时传递测试配置路径
            create_backup(self.test_config_path)
            backup_files = [f for f in os.listdir(self.test_backup_dir) if f.endswith('.zip')]
            self.assertTrue(len(backup_files) > 0, "Backup file was not created.")
            print(f"Created backup files: {backup_files}")
        except Exception as e:
            print(f"Test failed: {e}")
            self.print_log()
            raise

    def test_clean_old_backups(self):
        # 创建多个备份文件用于测试
        try:
            # 运行清理函数
            clean_old_backups(self.test_backup_dir, 3, 2)

            # 检查是否清理了多余的备份
            backup_files = [f for f in os.listdir(self.test_backup_dir) if f.endswith('.zip')]
            self.assertTrue(len(backup_files) <= 3, "Old backups were not properly cleaned.")
            print(f"Remaining backup files after cleaning: {backup_files}")
        except Exception as e:
            print(f"Test failed: {e}")
            self.print_log()
            raise

    def test_shell_call_backup_script(self):
        try:
            # 通过 shell 调用 backup_script.py 并传递配置路径
            result = subprocess.run(
                f"python3 backup_script.py {self.test_config_path}",
                shell=True,
                capture_output=True,
                text=True
            )
            self.assertEqual(result.returncode, 0, "Shell call to backup_script.py failed.")
            print("Shell call output:", result.stdout)
        except Exception as e:
            print(f"Shell call test failed: {e}")
            self.print_log()
            raise

if __name__ == "__main__":
    unittest.main()
