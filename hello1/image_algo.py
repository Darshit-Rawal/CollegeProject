import base64
import cv2
import numpy as np
import skimage.measure
import matplotlib.pyplot as plt
from imutils import is_cv2
from PIL import Image
from io import BytesIO
import urllib
import io



def image_process(img_path1, img_path2):
    imageA = cv2.imread(img_path1)
    imageB = cv2.imread(img_path2)

    hsv = cv2.cvtColor(imageA, cv2.COLOR_BGR2HSV)
    hsv1 = cv2.cvtColor(imageB, cv2.COLOR_BGR2HSV)

    lower_green = np.array([30, 60, 50])
    upper_green = np.array([90, 255, 255])

    mask = cv2.inRange(hsv, lower_green, upper_green)
    mask1 = cv2.inRange(hsv1, lower_green, upper_green)

    res = cv2.bitwise_and(imageA, imageA, mask=mask)
    res1 = cv2.bitwise_and(imageB, imageB, mask=mask1)

    (score, diff) = skimage.metrics.structural_similarity(mask, mask1, full=True)
    diff = (diff * 255).astype("uint8")
    # print("SSIM: {}".format(score))

    thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if is_cv2() else cnts[1]

    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        cv2.rectangle(imageA, (x, y), (x + w, y + h), (255, 0, 0), 2)
        cv2.rectangle(imageB, (x, y), (x + w, y + h), (255, 0, 0), 2)

    #cv2.imshow("Original", imageA)
    Original = Image.fromarray(imageA)
    data1 = BytesIO()
    Original.save(data1, "png")
    data64_1 = base64.b64encode(data1.getvalue())
    url1 ='data:img/jpeg;base64,'+data64_1.decode('utf-8')
    #cv2.imshow("Modified", imageB)
    Modified = Image.fromarray(imageB)
    data2 = BytesIO()
    Modified.save(data2, "png")
    data64_2 = base64.b64encode(data2.getvalue())
    url2 ='data:img/jpeg;base64,'+data64_2.decode('utf-8')

    #cv2.imshow("Diff", diff)
    Diff = Image.fromarray(diff)
    data3 = BytesIO()
    Diff.save(data3, "png")
    data64_3 = base64.b64encode(data3.getvalue())
    url3 ='data:img/jpeg;base64,'+data64_3.decode('utf-8')
    #cv2.imshow('mask', mask)
    maskA = Image.fromarray(mask)
    # maskA.save("maskA.png")
    #cv2.imshow('maskB', mask1)
    maskB = Image.fromarray(mask1)
    # maskB.save("maskB.png")
    #percentage diff.

    res = cv2.absdiff(mask, mask1)
    res = res.astype(np.uint8)
    percentage = (np.count_nonzero(res) * 100)/ res.size
    # print(percentage)
    #graph
    values = [percentage]

    if values >= [50.00]:
        color = "red"
    elif values >= [20.00] and values < [50.00]:
        color = "orange"
    else:
        color = "green"

    #plt.figure(figsize=(9, 2))

    ax = plt.subplot(121)
    plt.bar("bar chart", values, color= color)
    ay = plt.subplot(122)
    plt.scatter("scatter", values,color= color)
    plt.suptitle('Forest Changes graph')


    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri =  urllib.parse.quote(string)
    plt.clf()
    cv2.waitKey(0)
    return url1, url2, url3, uri, percentage
