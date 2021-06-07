from octoclient import OctoClient

URL = 'http://192.168.137.98:5000/'
API_KEY = 'API_KEY'


# Pause the printer
def pause_print():
    try:
        client = OctoClient(url=URL, apikey=API_KEY)
        flags = client.printer()['state']['flags']
        if flags['printing']:
            client.pause()
            print("Print paused.")
        elif flags['paused'] or flags['pausing']:
            print("Print already paused.")
        else:
            print("Print cancelled or error occurred.")
    except Exception as e:
        print(e)


def print_control(curr, score, deviance, scr_diff, dev_diff):
    # Get SCORE, DEVIANCE and current layer from get_score.py

    LAYER = curr
    SCORE = score
    DEVIANCE = deviance
    SCR_DIFF = scr_diff
    DEV_DIFF = dev_diff

    # Do nothing if it is the background or first layer
    if LAYER <= 7:
        return

    # Detachment thresholds
    SCR_THRES = 1.0
    DEV_THRES = 1.0

    # Partial Breakage thresholds for DIFF values
    BR_SCR_THRES = 0.15
    BR_DEV_THRES = 0.10

    # Filament run out/clog thresholds
    FIL_SCR_THRES = 0.23
    FIL_DEV_THRES = 0.28

    # This indicates the model has detached from the bed
    if SCORE > SCR_THRES and DEVIANCE > DEV_THRES:
        print("Cause: Print detached from bed", f'LAYER:{LAYER}')
        pause_print()
    # This indicates a part of the model has broken off
    elif SCR_DIFF > BR_SCR_THRES and DEV_DIFF > BR_DEV_THRES:
        print("Cause: Potential (partial) breakage", f'LAYER:{LAYER}')
        pause_print()
'''    elif SCORE < FIL_SCR_THRES and DEVIANCE < FIL_DEV_THRES:
        print("Cause: Filament ran out or nozzle/extruder clog", f'LAYER:{LAYER}')
        pause_print()'''
