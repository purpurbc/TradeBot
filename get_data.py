import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime,timedelta,timezone
from matplotlib.widgets import Cursor

def quit_chromedriver(driver):
    driver.quit()
    
def load_webpage(url_name,wait):
    
    #options
    options = webdriver.ChromeOptions()
    options.add_argument("--headless") #so that a new browser isnt opened each time
    options.add_experimental_option('excludeSwitches', ['enable-logging']) #used to disable annoying printouts by the webdriver
    #performance related options
    options.add_argument("start-maximized")
    options.add_argument("disable-infobars")
    options.add_argument("--disable-extensions")
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-application-cache')
    options.add_argument('--disable-gpu')
    options.add_argument("--disable-dev-shm-usage")
    
    print("Loading webpage...")
    #create driver and load the specified webpage
    try:
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=options)
        driver.implicitly_wait(wait) 
        driver.get(url_name)
    except Exception as e: 
        print(e)
        return
    print("Webpage successfully loaded!\n")
    
    #return the driver if successful
    return driver

def read_html(driver,xpath):
  
    try:
        df=pd.read_html(driver.find_element(By.XPATH, xpath).get_attribute("outerHTML"))
    except Exception as e: 
        print(e)
        return #empty return. Failure
    
    #return the dataframe
    return df

def search_in_dataframe(df,crypto_name,column_name,length):
    print("Searching for ", crypto_name, " in list...")
    for i in range(length):
        try:
            if crypto_name in df[0].loc[i].loc[column_name]:
                print(crypto_name, " found! (", df[0].loc[i].loc[column_name], ")\n")
                return i
        except Exception as e: 
            print(e)
            return

def log_and_save_data(data_values,time_values,df,wanted_data,index):
    
    #open the file for appending. Create if necessary
    fh = open('live_data', 'a+')
    
    #if the wanted data in the dataframe is a string (need to remove dollarsign)
    if isinstance(df[0].loc[index].loc[wanted_data], str):
        #remove dollarsign if necessary and append it to the data_values list
        data_values.append(float(df[0].loc[index].loc[wanted_data].replace('$','')))
        #write to the file, i.e. log the data in memory for future use. Also add the unix timestamp
        fh.write(df[0].loc[index].loc[wanted_data].replace('$','') + ", " + str(datetime.now(tz=timezone.utc).timestamp()) + "\n")
    
    #if the wanted data in the dataframe is a float
    elif isinstance(df[0].loc[index].loc[wanted_data], float):
        #append it to the data_values list
        data_values.append(df[0].loc[index].loc[wanted_data])
        #write to the file, i.e. log the data in memory for future use. Also add the unix timestamp
        fh.write(str(df[0].loc[index].loc[wanted_data]) + ", " + str(datetime.now(tz=timezone.utc).timestamp()) + "\n")
    
    #close the file
    fh.close()
    
    #append the time to the time_values list
    time_values.append((datetime.now(tz=timezone.utc)+timedelta(hours=2)).timestamp())


def annot_max(x,y, ax=None):

    xmax = x[np.argmax(y)]
    ymax = max(y)

    text= "{:.3f}".format(float(ymax))

    if not ax:
        ax=plt.gca()

    bbox_props = dict(facecolor='none', edgecolor='#434242', boxstyle='round')
    arrowprops=dict(arrowstyle="->",connectionstyle="arc3",color="#5f5e5d")
    kw = dict(xycoords='data',textcoords='offset points', arrowprops=arrowprops, bbox=bbox_props, ha="right", va="top")

    ax.annotate(text, xy=(xmax, ymax), xytext=(float(xmax),float(ymax)), **kw)


def annot_min(x,y, ax=None):

    xmin = x[np.argmin(y)]
    ymin = min(y)

    text= "{:.3f}".format(float(ymin))

    if not ax:
        ax=plt.gca()

    bbox_props = dict(facecolor='none', edgecolor='#434242', boxstyle='round')
    arrowprops=dict(arrowstyle="->",connectionstyle="arc3",color="#5f5e5d")
    kw = dict(xycoords='data',textcoords='offset points', arrowprops=arrowprops, bbox=bbox_props)

    ax.annotate(text, xy=(xmin, ymin), xytext=(float(xmin),float(ymin)), **kw)


def plot_graph(data_values,time_values,crypto_name,update_rate,step_size,marker_size):


    #regulate the spacing between the xlabels 
    step_size = (len(time_values)/40)*5
    if step_size < 5: step_size = 5
    if len(time_values) > 80: marker_size = 0
    plt.xticks(np.arange(start=0, stop=len(time_values), step=step_size))

    #plot,legend,pause and clear
    plt.plot([(datetime.fromtimestamp(x)).strftime("%m/%d/%Y\n%H:%M:%S") for x in time_values], data_values, linestyle='solid', marker='p', ms=marker_size,  color='r', label=crypto_name)

    annot_max(range(len(time_values)),data_values)
    annot_min(range(len(time_values)),data_values)

    plt.legend()
    plt.pause(update_rate)
    plt.clf()

    
    
    
def get_saved_data():
    
    #open textfile for reading only. Create a new file if one doesnt exist already
 
    txt_file = open("live_data", "r")
    
    #read the file
    file_content = txt_file.read()
    
    #split the content and transform values from string into floats
    data = [list(map(float,line.split(", "))) for line in (file_content.splitlines())]
    
    #append the values to the corresponding lists
    price_data = [x[0] for x in data]
    time_data = [x[1] for x in data]
    
    #close the file
    txt_file.close()
    
    #return the x/y-data
    return price_data,time_data


"""Reads a .csv file and plots the data with pyplot"""
def get_csv_data(filename, columnname, col_list, length, plot):
    
    #read csv file
    df = pd.read_csv(filename, usecols=col_list)
    
    #get starttime
    start_time = float(df["unix"][length])
    
    #change the dataframe to a list and convert the strings to floats
    data = list(map(float,df[columnname][0:length]))

    #get unix timestamps
    time_stamps = list(map(float,df["unix"][0:length]))
    #time_stamps = [x - start_time for x in time_stamps]

    #plot a graph of the gathered data
    if plot:
        plt.plot(time_stamps, data)
        plt.show()
    
    #return the data-list
    return data
    
    
    

