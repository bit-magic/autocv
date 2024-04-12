import pyautogui
from utils import base642img
import pyperclip


# instr{type,args,func}
def inter(instrs, env={}, pc=0):
    while pc < len(instrs):
        inter0(env, instrs, pc)
        pc += 1
    return None


# [
#  [click base64 args(obj)...]
#  [input base64 var args(obj)..]
#  [keyboard args(str arr)..]
#  [syscall id args(obj)...]
#  [funcall resVar funname arg(obj)...]
#  [write source dest]
#  [read souce dest]
#  [define var var2]
#  [set var var2]
#  [label label]
#  [if test labname]
# ]


def inter0(env, instrs, pc):
    instr = instrs[pc]
    key = instr[0]
    if key == 'input':
        return __input(env, instr[1], instr[2], instr[3])
    elif key == 'click':
        return __click(env, instr[1], instr[2])
    elif key == '__syscall':
        return __click(env, instr[1], instr[2])
    elif key == 'keyboard':
        return __keyboard(env, instr[1])
    elif key == 'write':
        return __write(env, instr[1], instr[2])
    elif key == 'read':
        return __read(env, instr[1], instr[2])
    elif key == 'define':
        return __define(env, instr[1], instr[2])
    elif key == 'set':
        return __set(env, instr[1], instr[2])
    elif key == 'label':
        return __label(env, instr[1], pc)
    elif key == 'if':
        pc = __if(env, instr[1], instr[2])
        if pc > -1:
            return inter(instrs, env, pc)
        else:
            return None
    else:
        return __autogui(key, instr[1])


def __click(env, base64str, args):
    return __autogui('click', {** __getbox(base64str), ** args})


def __input(env, base64str, var, args):
    __click(env, base64str, args)
    return pyautogui.write(__getval(env, var))


def __syscall(env, id, args):
    if id == 'read_paste2var':
        varname = args
        __setval(env, varname,  pyperclip.paste())
    elif id == 'clear_paste':
        return pyperclip.copy()
    elif id == 'screenshot2var':
        # TODO
        im = pyautogui.screenshot()
        __setval(env, varname,  im)
    elif id == 'ocr2var':
        # TODO
        im = pyautogui.screenshot()
        __setval(env, varname,  im)


def __keyboard(env, args):
    pyautogui.hotkey(args)


# TODO 还不完善
def __write(env, source, dest):
    __setval(env, dest, __getval(env, source))


# TODO 还不完善
def __read(env, source, dest):
    __setval(env, dest, __getval(env, source))


def __define(env, var, var2):
    if var in env:
        __setval(env, var, __getval(env, var2))


def __set(env, var, var2):
    if var in env:
        return
    __setval(env, var, __getval(env, var2))


def __label(env, labelname, index):
    __setval(env, labelname, index)


def __if(env, test, labelname):
    if __getval(test):
        return __getval(env, labelname)
    else:
        return -1


def __getval(env, var):
    if isinstance(var, Symbol):
        return env[var.name]
    else:
        return var


def __setval(env, varkey, val):
    if isinstance(varkey, Symbol):
        env[varkey.name] = val


def __getbox(base64str):
    if len(base64str) > 10:
        box = pyautogui.\
            locateOnScreen(base642img(base64str), confidence=0.9, grayscale=True)
        return {'x': box.left+(box.width/2), 'y': box.top+(box.height/2)}
    else:
        return {}


def __autogui(func_name, args):
    func = getattr(pyautogui, func_name)
    return func(** args)


class Symbol:
    def __init__(self, name):
        self.name = name


print(inter([
    ['click', '', {'x': 100, 'y': 100}],
    ['input', '', 'sfdsfsd', {'x': 300, 'y': 100}]
]))

# : > ^


# // num str boolean
# [
#  [click base64 args...]
#  [input base64 var args..]
#  [keyboard args..]
#  [syscall id args...]
#  [funcall resVar funname arg...]
#  [write source dest]
#  [read souce dest]
#  [define var var2]
#  [set var var2]
#  [label label]
#  [if test labname]
# ]

# > f'./data.csv' excel
# = len len(excel)
# : summarizelabel
# = i 0
# = name excel[i][0] 
# @ click {x:1,y:2}
# @ typewrite name
# @ click {x:3,y:5}
# @ hotkey ['ctrl', 'c']
# = orderNo paste
# @ push excel[i] orderNo
# @ ++ i
# = flag (i < len)
# ^ flag summarizelabel
# > excel f'./data.csv'
# ((define excel (readfile './data.csv'))(define l (len excel))(def go(item)((define name (list-ref item 0)))(click (x 0) (y 1))))