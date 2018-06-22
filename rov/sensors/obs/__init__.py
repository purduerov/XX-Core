

def OBS(ip="192.168.42.1"):
    try:
        from OBS import OBS
        return OBS(ip = ip)
    except Exception as e:
        print("Failed to Initialize OBS")
        print("Error: %s" % e.message)
        print("Using Mock OBS")
        from OBS_Mock import OBS as OBS_Mock
        return OBS_Mock()
