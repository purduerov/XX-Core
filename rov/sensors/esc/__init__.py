

def ESC():
    try:
        from ESC import ESC
        return ESC()
    except Exception as e:
        print("Failed to Initialize ESC")
        print("Error: %s" % e.message)
        print("Using Mock ESC")
        from ESC_Mock import ESC
        return ESC()
