import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime

"""annotate either max or min value of specified data_values"""
def annot(y,x,type):

    xval = 0
    yval = 0

    #get max/min values
    if type == 'max':
        xval = x[np.argmax(y)]
        yval = max(y)
    elif type == 'min':
        xval = x[np.argmin(y)]
        yval = min(y)

    #create text
    text= "{:.3f}".format(float(yval))

    ax=plt.gca()

    #set the text at xy-pos with a specific style
    style = dict(size=10, color='gray')
    ax.text(xval, yval, text, **style)

"""set the spacing for the xticks in the plot"""
def set_plt_xticks(len_time_values,step_size):
    #regulate the spacing between the xlabels 
    step_size = (len_time_values/40)*5
    if step_size < 5: step_size = 5
    plt.xticks(np.arange(start=0, stop=len_time_values, step=step_size))

"""plot the graph for the data_values"""
def plot_graph(data_values,time_values,crypto_name,line_color):

    marker_size = 4 #size of the marker when plotting

    if len(time_values) > 80: 
        marker_size = 0

    #plot,legend,pause and clear
    plt.plot([(datetime.fromtimestamp(x)).strftime("%m/%d/%Y\n%H:%M:%S") for x in time_values], data_values, linestyle='solid', marker='p', ms=marker_size,  color=line_color, label=crypto_name)
   