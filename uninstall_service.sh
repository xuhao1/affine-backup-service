#!/bin/bash

# 检查当前用户是否有 sudo 权限
if [ "$EUID" -ne 0 ]; then
    echo "This script requires sudo privileges. Please run the script with sudo:"
    echo "sudo ./uninstall_service.sh"
    exit 1
fi

# 停止和禁用定时器和服务
echo "Stopping and disabling the Affine backup service and timer..."
systemctl stop affine_daily_backup.timer
systemctl disable affine_daily_backup.timer
systemctl stop affine_daily_backup.service
systemctl disable affine_daily_backup.service

# 删除服务和定时器文件
echo "Removing service and timer files..."
rm -f /etc/systemd/system/affine_daily_backup.service
rm -f /etc/systemd/system/affine_daily_backup.timer

# 重新加载 systemd 守护进程
echo "Reloading systemd daemon..."
systemctl daemon-reload

echo "Affine backup service and timer have been uninstalled successfully."
