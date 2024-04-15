import pyautogui
from type import Symbol
from env import getval, setval
from utils import is_num
import functions
import json


def eval(str="", env={}, pc=0, splitkey="\n", lines=[]):
    lines = lines if len(lines) > 0 else str.strip().split(splitkey)
    instrs = list(
        map(lambda line: list(
            map(__parese_el,
                line.strip().split(' '))), lines))
    return inter(instrs, env, pc)


def inter(instrs, env={}, pc=0):
    r = None
    while pc < len(instrs):
        r = __inter(env, instrs, pc)
        pc += 1
    return r


def __parese_el(str):
    str = str.strip()
    if str.find("'") == 0 or str.find('"') == 0:
        return str[1:-1]
    elif str.find("[") == 0 or str.find('{') == 0:
        return json.loads(str.replace("'", '"'))
    elif len(str) == 0 or 'null' == str:
        return None
    elif is_num(str):
        return float(str) if '.' in str else int(str)
    elif 'true' == str or 'false' == str:
        return 'true' == str
    else:
        return Symbol(str)


def __inter(env, instrs, pc):
    instr = instrs[pc]
    key = instr[0]
    if isinstance(key, Symbol):
        symbol = key.name
        if hasattr(functions, symbol):
            fun = getattr(functions, symbol)
            return fun(env, *instr[1:])
        elif symbol == 'label':
            return __label(env, instr[1], pc)
        elif symbol == 'if':
            pc = __branch(env, instr[1], instr[2])
            if pc > -1:
                return inter(instrs, env, pc)
            else:
                return None
        elif len(instr) == 1:
            return getval(env, key)
        else:
            return __autogui(symbol, instr[1:])
    else:
        key


def __label(env, labelname, index):
    setval(env, labelname, index)


def __branch(env, test, labelname):
    if getval(test):
        return getval(env, labelname)
    else:
        return -1


def __autogui(func_name, args):
    if hasattr(pyautogui, func_name):
        # print(func_name, args)
        func = getattr(pyautogui, func_name)
        if isinstance(args, list):
            if len(args) == 1:
                return func(args[0])
            else:
                return func(** args)
        else:
            return None
    else:
        return None


# print(is_num('0.5'))

# print(inter([
#     [Symbol('click'), '', {'x': 100, 'y': 100}],
#     [Symbol('input'), '', 'sfdsfsd', {'x': 300, 'y': 100}],
#     [Symbol('keyboard'), 'ctrl', 'a'],
#     [Symbol('keyboard'), 'ctrl', 'c'],
#     [Symbol('syscall'), 'read_paste2var', Symbol('a')],
#     [Symbol('a')]
# ]))

# print(eval("""
#     click null {"x":100,"y":100}
#     input null "sdfsdfsd" {"x":300,"y":100}
#     keyboard 'ctrl' 'a'
#     keyboard 'ctrl' 'c'
#     syscall 'readpaste2var' a
#     a
#      """))

# print(hasattr(functions, "input"))
# : > ^

# key key1 key2 key3
# // num str boolean
# [
#  [click base64 args]
#  [input base64 var args]
#  [keyboard args...3]
#  [syscall id args]
# -  [funcall resVar funname arg...]
#  [openfile file filevar]
#  [has-next-line filevar var]
#  [read-next-line filevar varobj]
#  [writeflush filevar]
#  [getattr varobj.attr var]
#  [setattr varobj.attr var]
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