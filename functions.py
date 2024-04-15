import pyautogui
from utils import base642img, img2base64
import pyperclip
from env import getval, setval
from type import ArrayIterator, Symbol
import time
import requests
import json


def keyboard(env, *args):
    pyautogui.hotkey(*args)


def click(env, base64str, args={}):
    return pyautogui.click(** {** __getbox(base64str), ** args})


def scroll(env, varname):
    return pyautogui.scroll(getval(env, varname))


def input(env, base64str, varname, args={}):
    # print("{} {} {}".format(base64str, var, args))
    click(env, base64str, args)
    return pyautogui.write(getval(env, varname))


def getbox(env, base64str, varname):
    setval(env, varname, __getbox(base64str))


def syscall(env, id, arg):
    if id == 'readpaste2var':
        varname = arg
        copyText = pyperclip.paste()
        setval(env, varname, copyText)
    elif id == 'pastefrom':
        varname = arg
        pyperclip.copy(getval(env, varname))
    elif id == 'clearpaste':
        return pyperclip.copy()
    elif id == 'screenshot2var':
        im = pyautogui.screenshot()
        setval(env, varname, img2base64(im))
    elif id == 'ocr2var':
        im = pyautogui.screenshot()
        text = ocr(img2base64(im))
        setval(env, varname,  text)


def openfile(env, filename, varfilename):
    arr = []
    setval(env, varfilename, ArrayIterator(arr))


def read_next_line(env, varfilename, varname):
    file = getval(env, varfilename)
    setval(env, varname, file.next())


def hash_next_line(env, varfilename, varname):
    file = getval(env, varfilename)
    setval(env, varname, file.has_next())


def writeflush(env, varfilename):
    getval(env, varfilename)
    # TODO 更新数据


def getattr(env, attr, varname):
    [objvarname, fieldname] = attr.name.split('.')
    obj = getval(env, Symbol(objvarname))
    setval(env, varname, obj[fieldname])


def setattr(env, attr, varname):
    [objvarname, fieldname] = attr.name.split('.')
    obj = getval(env, Symbol(objvarname))
    obj[fieldname] = getval(env, varname)


def sleep(env, sec):
    time.sleep(sec)


def __getbox(base64str):
    if (not (base64str is None)) and len(base64str) > 10:
        im = base642img(base64str)
        box = pyautogui.\
            locateOnScreen(im, confidence=0.9, grayscale=True)
        return {'x': box.left+(box.width/2), 'y': box.top+(box.height/2)}
    else:
        return {}


def ocr(imgbase64):
    url = "http://ocr.3j168.cn/ocr"
    payload = json.dumps({
        "img": str(imgbase64, encoding="utf-8"),
    })
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)
    if response.status_code == 200:
        return response.text
    else:
        return "error"
