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
with open(sys.argv[3], "rb") as f:
    r = requests.put("https://upload.2epik4u.lol/remote.php/dav/files/admin/" + file, data=f, auth=(user, password))

share = requests.post("https://upload.2epik4u.lol/ocs/v2.php/apps/files_sharing/api/v1/shares", headers={"OCS-APIRequest": "true"}, data={"path": file, "shareType": 3}, auth=(user,password))
root = ET.fromstring(share.text)
pro = root.find('data')
root = pro.find('url')
calc = (time.time() - start)
calc2 = str(calc) + " Seconds"
subprocess.run(["notify-send", "-a", "Nextcloud API", root.text + "/download" +  "\n" + "Done! took " + calc2])

subprocess.run(["wl-copy", root.text + "/download"])
