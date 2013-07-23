def isset(value):
    try:
        type(eval(value))
    except:
        return 0
    else:
        return 1
