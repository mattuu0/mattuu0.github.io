import os
import shutil

os.system("apt update")
os.system("apt install -y curl")
os.system("curl -fsSL https://tailscale.com/install.sh | sh")
os.system("systemctl enable tailscaled")

original_path = "/etc/systemd/system/multi-user.target.wants/tailscaled.service"
backup_path = "/etc/systemd/system/multi-user.target.wants/tailscaled.service.org"

if not os.path.exists(backup_path):
    # バックアップが存在しないとき
    shutil.copyfile(original_path,backup_path)
    pass

with open("/etc/systemd/system/multi-user.target.wants/tailscaled.service","w",encoding="utf-8") as writeScript:
    writeScript.write("""
[Unit]
Description=Tailscale node agent
Documentation=https://tailscale.com/kb/
Wants=network-pre.target
After=network-pre.target NetworkManager.service systemd-resolved.service

[Service]
EnvironmentFile=/etc/default/tailscaled
ExecStart=/usr/sbin/tailscaled --tun=userspace-networking --socks5-server=localhost:1055 --outbound-http-proxy-listen=localhost:1055 --state=/var/lib/tailscale/tailscaled.state --socket=/run/tailscale/tailscaled.sock --port=${PORT} $FLAGS
ExecStopPost=/usr/sbin/tailscaled --cleanup

Restart=on-failure

RuntimeDirectory=tailscale
RuntimeDirectoryMode=0755
StateDirectory=tailscale
StateDirectoryMode=0700
CacheDirectory=tailscale
CacheDirectoryMode=0750
Type=notify

[Install]
WantedBy=multi-user.target
""")
    
os.system("systemctl daemon-reload")
os.system("systemctl enable tailscaled")
os.system("tailscale up --ssh")