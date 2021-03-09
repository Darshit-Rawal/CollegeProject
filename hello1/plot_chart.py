from matplotlib import pyplot as plt
import io
import numpy as np
from io import BytesIO
from io import StringIO
import urllib
import base64
import urllib.request


def plot_pie(lable, diff):
    fig1 = plt.figure(figsize=(10, 7))
    explode = (0.1, 0.2)
    lable[0] = lable[0] + "(" + str(diff[0]) + "%)"
    lable[1] = lable[1] + "(" + str(diff[1]) + "%)"
    plt.pie(diff, labels=lable, explode=explode)
    fig = plt.gcf()
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    urx = urllib.parse.quote(string)
    plt.clf()
    return urx
