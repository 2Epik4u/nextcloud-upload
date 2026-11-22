import requests
import sys
import xml.etree.ElementTree as ET
import subprocess
import os
import time
start = time.time()
file = os.path.basename(sys.argv[3])
user = sys.argv[1]
password = sys.argv[2]
headers = {'user-agent': 'epikscript/1.0', "OCS-APIRequest": "true"}
with open(sys.argv[3], "rb") as f:
    r = requests.put(f"https://upload.ooodt.me/remote.php/dav/files/{user}/" + file, data=f, auth=(user, password), headers=headers)

share = requests.post("https://upload.ooodt.me/ocs/v2.php/apps/files_sharing/api/v1/shares", headers=headers, data={"path": file, "shareType": 3}, auth=(user,password))
try:
    root = ET.fromstring(share.text)
    pro = root.find('data')
    root = pro.find('url')
    calc = (time.time() - start)
    calc2 = str(calc) + " Seconds"
    subprocess.run(["notify-send", "Nextcloud API", root.text + "/download" +  "\n" + "Done! took " + calc2])
    subprocess.run(["wl-copy", "[" + file + "]" + "(" + root.text +"/download"+ ")" ])
except Exception as e:
    string = "WARNING WARNING WARNING ERROR! " + str(e)
    subprocess.run(["wl-copy", string + r.text + share.text])
    subprocess.run(["notify-send", "-u", "critical", "-i", "error", "Nextcloud API", string])