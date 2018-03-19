

def OBS():
    try:
        from OBS import OBS
        return OBS()
    except Exception as e:
        print("Failed to Initialize OBS")
        print("Error: %s" % e.message)
        print("Using Mock OBS")
        from OBS_Mock import OBS as OBS_Mock
        return OBS_Mock()
