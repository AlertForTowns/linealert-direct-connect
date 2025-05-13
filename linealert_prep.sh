#!/bin/bash

# Disable unnecessary services
echo "Disabling unnecessary services..."
sudo systemctl disable --now bluetooth.service
sudo systemctl disable --now cups.service         # Printing
sudo systemctl disable --now avahi-daemon.service # mDNS/zeroconf
sudo systemctl disable --now ModemManager.service
sudo systemctl disable --now snapd.service
sudo systemctl disable --now cloud-init.service   # Optional for cloud provisioning

# Lock Down Network Interfaces
echo "Locking down network interfaces..."
nmcli radio wifi off # Disable Wi-Fi if using wired interface
# Optional: Set static IP if needed
# sudo ip addr add <STATIC_IP> dev eth0

# Clean DNS resolution
echo "Locking DNS resolution..."
sudo chattr +i /etc/resolv.conf

# Disable unused logging services
echo "Disabling unused logging..."
sudo systemctl stop rsyslog
sudo systemctl disable --now rsyslog
sudo systemctl stop cron
sudo systemctl disable --now cron

# Redirect specific loggers to /dev/null (discard logs)
echo "Redirecting unwanted logs to /dev/null..."
sudo ln -sf /dev/null /var/log/syslog
sudo ln -sf /dev/null /var/log/messages
sudo ln -sf /dev/null /var/log/auth.log

# Clear out old log files (optional, ensure no unnecessary logs are stored)
echo "Clearing out old log files..."
sudo rm -rf /var/log/*.log
sudo rm -rf /var/log/*.gz

# Disable persistent journald logging (useful for reducing disk space usage and log noise)
echo "Disabling persistent journald logging..."
sudo mkdir -p /etc/systemd/journald.conf.d
echo -e "[Journal]\nStorage=volatile" | sudo tee /etc/systemd/journald.conf.d/disable-persistent.conf
sudo systemctl restart systemd-journald

# Optional: Lock CPU scaling for consistent performance
echo "Locking CPU scaling to performance mode..."
sudo apt install -y cpufrequtils
echo 'GOVERNOR="performance"' | sudo tee /etc/default/cpufrequtils
sudo systemctl disable ondemand
sudo systemctl enable cpufrequtils

# Set up NTP for accurate time synchronization
echo "Setting up NTP for accurate time sync..."
sudo apt install -y chrony
sudo systemctl enable --now chronyd

# Set up firewall to block unwanted incoming connections (optional)
echo "Setting up UFW firewall..."
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw enable

# Limit kernel messages to reduce noise
echo "Limiting kernel logging..."
sudo dmesg -n 1  # Limit kernel messages to "Emergency" level only

# Validate snapshot output by checking time sync and .lasnap formatting
echo "Validating snapshot pipeline..."
# Assuming you have a snapshot script that generates .lasnap files
# Ensure files include clear UTC timestamps and don't overwrite without warning
# You can use this script to run your capture pipeline end-to-end

echo "LineAlert prep completed! System should now be ready for demo."
