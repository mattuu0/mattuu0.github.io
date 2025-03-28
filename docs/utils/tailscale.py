import os
import shutil

os.system("apt update")
os.system("apt install -y curl")
os.system("curl -fsSL https://tailscale.com/install.sh | sh")
os.system("systemctl enable tailscaled")

original_path = "/etc/default/tailscaled"
backup_path = "/etc/default/tailscaled.org"

if not os.path.exists(backup_path):
    # バックアップが存在しないとき
    shutil.copyfile(original_path,backup_path)
    pass

with open(original_path,"w",encoding="utf-8") as writeScript:
    writeScript.write("""
# Set the port to listen on for incoming VPN packets.
# Remote nodes will automatically be informed about the new port number,
# but you might want to configure this in order to set external firewall
# settings.
PORT="41641"

# Extra flags you might want to pass to tailscaled.
FLAGS="--tun=userspace-networking --socks5-server=localhost:1055 --outbound-http-proxy-listen=localhost:1055 --state=/var/lib/tailscale/tailscaled.state --socket=/run/tailscale/tailscaled.sock"
""")
    
os.system("systemctl daemon-reload")
os.system("systemctl enable tailscaled")
os.system("tailscale up --ssh")