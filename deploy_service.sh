#!/bin/bash

# 检查当前用户是否有 sudo 权限
if [ "$EUID" -ne 0 ]; then
    echo "This script requires sudo privileges. Please run the script with sudo:"
    echo "sudo ./deploy_service.sh"
    exit 1
fi

# 检查是否已安装 zip 工具
if ! command -v zip &> /dev/null; then
    echo "zip is not installed. Installing zip..."
    # 检测操作系统并安装 zip（假设使用的是基于 Debian/Ubuntu 的系统）
    if [ -x "$(command -v apt-get)" ]; then
        apt-get update
        apt-get install -y zip
    else
        echo "Unsupported package manager. Please install 'zip' manually."
        exit 1
    fi
else
    echo "zip is already installed."
fi

# 检查是否存在日志目录或文件
LOG_DIR="/var/log/affine_backup"
if [ ! -d "$LOG_DIR" ]; then
    echo "Creating log directory at $LOG_DIR"
    sudo mkdir -p "$LOG_DIR"
    sudo chmod 755 "$LOG_DIR"
fi

# 获取当前工作目录
CURRENT_DIR=$(pwd)
BACKUP_SCRIPT_PATH="$CURRENT_DIR/backup_script.py"
CONFIG_PATH="$CURRENT_DIR/config.yaml"

# 检查脚本和配置文件是否存在
if [ ! -f "$BACKUP_SCRIPT_PATH" ] || [ ! -f "$CONFIG_PATH" ]; then
    echo "Error: backup_script.py or config.yaml not found in the current directory ($CURRENT_DIR)"
    exit 1
fi

# 读取 YAML 中的备份周期
BACKUP_CYCLE_DAYS=$(grep 'backup_cycle_days' config.yaml | awk '{print $2}')

# 创建定时器文件
cat <<EOL | sudo tee /etc/systemd/system/affine_daily_backup.timer
[Unit]
Description=Run Affine Backup Service Every $BACKUP_CYCLE_DAYS Days

[Timer]
OnCalendar=*-*-* 00:00:00/$BACKUP_CYCLE_DAYS
Persistent=true

[Install]
WantedBy=timers.target
EOL

# 创建服务文件
cat <<EOL | sudo tee /etc/systemd/system/affine_daily_backup.service
[Unit]
Description=Affine Backup Service
After=network.target

[Service]
Type=simple
ExecStart=/usr/bin/python3 $BACKUP_SCRIPT_PATH $CONFIG_PATH
User=your-username
Group=your-group
Restart=on-failure
StandardOutput=append:$LOG_DIR/backup_script.log
StandardError=append:$LOG_DIR/backup_script.log

[Install]
WantedBy=multi-user.target
EOL

# 重新加载 systemd 守护进程
sudo systemctl daemon-reload

# 启用并启动定时器
sudo systemctl enable affine_daily_backup.timer
sudo systemctl start affine_daily_backup.timer

echo "Affine backup service deployed and timer started. Logs will be available at $LOG_DIR/backup_script.log"
