def LOG(s):
    if logging:
        if type(s).__name__ == "str":
            print s
        else:
            print str(s)


logging = False