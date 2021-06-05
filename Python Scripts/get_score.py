import cv2
from os.path import dirname
from sys import argv, exit, stderr
from skimage.metrics import normalized_root_mse as compare_nrmse
from print_control import *


def get_score(path):
    # for debugging
    if type(path) == int:
        basepath = 'JUST_DIR'
        path = basepath + str(path).rjust(6, '0') + '.jpg'

    fst_file = path
    # Set current image and previous image
    curr = int(fst_file[-10:-4])
    prev = curr - 1

    def pause_print():
        pass

    # For the 1st and 2nd images, output 0
    # 1st image is used as background image
    # 2nd image has no previous image (gives errors as prev is BG)
    if curr == 0:
        print("0 nan")
        print("Background Image", file=stderr)
        return None

    if curr == 1:
        print("1 nan")
        print("First Image, no previous images", file=stderr)
        return None

    snd_file = fst_file[:-10] + str(prev).rjust(6, '0') + fst_file[-4:]

    bg_file = fst_file[:-10] + '000000.jpg'

    # load the two input images and background image
    # imageA = cv2.imread(fst_file)
    # imageB = cv2.imread(snd_file)
    # imageBG = cv2.imread(bg_file)

    # convert the images to grayscale
    grayA = cv2.imread(fst_file, 0)
    grayB = cv2.imread(snd_file, 0)
    grayBG = cv2.imread(bg_file, 0)

    # Remove background and threshold to remove shadow effects
    threshold = 1

    diffA = cv2.absdiff(grayA, grayBG)
    thresA = cv2.threshold(diffA, threshold, 255, cv2.THRESH_BINARY)[1]

    diffB = cv2.absdiff(grayB, grayBG)
    thresB = cv2.threshold(diffB, threshold, 255, cv2.THRESH_BINARY)[1]

    # compute the Normalised Root Mean-Squared Error (NRMSE) between the two
    # images
    score = compare_nrmse(thresA, thresB)

    # Compare the current image with the image from 5 layers ago
    # This is used to check for filament runout or huge deviance
    deviance = 1.0
    scr_diff = 0.0
    dev_diff = 0.

    logfile = dirname(fst_file) + '/output.log'
    if curr > 5:
        trd_file = fst_file[:-10] + str(curr - 5).rjust(6, '0') + fst_file[-4:]
        # imageC = cv2.imread(trd_file)
        grayC = cv2.imread(trd_file, 0)
        diffC = cv2.absdiff(grayC, grayBG)
        thresC = cv2.threshold(diffC, threshold, 255, cv2.THRESH_BINARY)[1]
        deviance = compare_nrmse(thresA, thresC)

        # Calculate difference compared with previous layer score and deviance

        with open(logfile) as log:
            data = log.readlines()
        prev_layer = data[-1]
        layer, scr, dev, s_diff, d_diff = prev_layer.split(" ")
        scr_diff = abs(score - float(scr))
        dev_diff = abs(deviance - float(dev))

    with open(logfile, 'a') as log:
        log.write(f'{curr} {score} {deviance} {scr_diff} {dev_diff}\n')

    print("{} {} {} {} {}".format(curr, score, deviance, scr_diff, dev_diff))
    print("Image: {:d}\t Score: {}\t Deviance: {}\tDiffs: {}/{}".format(curr, score, deviance, scr_diff, dev_diff),
          file=stderr)
    print_control(curr, score, deviance, scr_diff, dev_diff)

    '''
    SCORE = score
    DEVIANCE = deviance
    SCR_DIFF = scr_diff
    DEV_DIFF = dev_diff

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
        print("Cause: Print detached from bed")
        pause_print()
    # This indicates a part of the model has broken off
    elif SCR_DIFF > BR_SCR_THRES and DEV_DIFF > BR_DEV_THRES:
        print("Cause: Potential (partial) breakage")
        pause_print()
    elif SCORE < FIL_SCR_THRES and DEVIANCE < FIL_DEV_THRES:
        print("Cause: Filament ran out or nozzle/extruder clog")
        pause_print()
    '''

# for i in range(50):
#    get_score(i)
