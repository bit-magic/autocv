from type import Symbol


def getval(env, var):
    if isinstance(var, Symbol):
        return env[var.name]
    else:
        return var


def setval(env, varkey, val):
    if isinstance(varkey, Symbol):
        env[varkey.name] = val
