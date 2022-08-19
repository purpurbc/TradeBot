import get_data as gd
import matplotlib.pyplot as plt
import itertools as it
from datetime import datetime
import atexit
import subprocess
import os 
import time

#col_list = ['unix', 'date', 'symbol', 'open', 'high', 'low', 'close', 'Volume ETH', 'Volume USD']
#gd.get_csv_data("Bitstamp_ETHUSD_1h.csv","open",col_list,32743,True)

url = 'https://tradingeconomics.com/solusd:cur' 
xpath = '//html/body/form/div[4]/div/div[2]/div/div[1]/div[1]/div/div/div[6]/table' 
crypto_name = 'Solana'
column_name = 'Unnamed: 0'
wanted_data = 'Actual'
update_rate = 60
kill_chrome = True
plot = True


"""prints the name of the arguments passed to the function as well as its value,
but only if the variable is in the global scope"""
def print_info(*argv):
    for arg in argv:
        try:
            print("\t",[name for name in globals() if globals()[name] is arg][0],": ",arg)
        except Exception as e:
            print(e) 

"""kill all of the chrome processes. Active window will be closed as well"""
def kill_chrome_processes():
    #subprocess.call("TASKKILL /f  /IM  CHROME.EXE")
    browserExe = "chrome.exe" 
    os.system("taskkill /f /im "+browserExe) 

"""start the tradebot"""
def initiate_tradebot(url_name,xpath,crypto_name,column_name,wanted_data,update_rate,kill_chrome,plot):
    
    #kill all of the chrome processes when we start
    #subprocesses of chrome are added every time we run the program
    #if we dont kill them, the memory will get full
    #this will unfortunately close the active browser window also
    #atexit didnt work, would have used it otherwise. Now we kill beforehand instead
    if kill_chrome: kill_chrome_processes()
    
    #get the saved data. If no saved data is available, an empty list is created
    data_values, time_values = gd.get_saved_data()
    
    
    
    step_size = 5 #the space between each x_label
    marker_size = 4 #size of the marker when plotting
    fail_count = 0 #how many times the program has failed
    fail_limit = 5 #how many times the program is allowed to fail
    
    #loop until termination or fail_limit is reached
    for i in it.count(start=1):
        try:
            print("Webscrape initiated!")
            
            #print the tradebot info
            print_info(url_name,xpath,crypto_name,column_name,wanted_data,update_rate,kill_chrome,plot)
            
            #load the webpage and get the driver
            driver = gd.load_webpage(url_name,10)

            print("Reading HTML table...")
            #read the html and get the dataframe from the table
            #initial read to get the index below
            df = gd.read_html(driver,xpath)
            print("HTML table read! List of dataframes created\n")

            #search the dataframe for the crypto_name at the column_name
            index = gd.search_in_dataframe(df,crypto_name,column_name,30)
            
            print("Start webscraping!\n")
            #create a new figure if one doesnt exist.    
            
            #style
            plt.rc('lines', linewidth = 1, color = 'r')
            plt.rc('axes', facecolor='#E6E6E6', edgecolor='none',axisbelow=True)
            plt.rc('xtick', direction='inout', color='gray',labelsize=6)
            plt.rc('ytick', direction='out', color='gray')
            plt.rc('patch', ec='#E6E6E6', force_edgecolor=True)

            
            fig, ax = plt.subplots()
            plt.gcf().set_size_inches(14,5)

            #loop until termination of the program
            for j in it.count(start=1):
                
                ax.set_title('tradeBot')
                
                #read the html to get the updated dataframe
 
                df = gd.read_html(driver,xpath)

                #log and save all of the data, i.e. update the lists and write to file
                gd.log_and_save_data(data_values,time_values,df,wanted_data,index)

                #plot a graph/update the currently plotted graph
                if plot:
                   gd.plot_graph(data_values,time_values,crypto_name,update_rate,step_size,marker_size) 

            
            plt.show()

        #resume if not fail_limit has been reached        
        except Exception as e: 
            fail_count += 1
            print(e,"\nTrying to resume... (", fail_count, "/",fail_limit,")\n")
            if fail_count >= fail_limit: break
          
    #close the chromedriver at exit
    atexit.register(gd.quit_chromedriver,driver=driver)  


initiate_tradebot(url,xpath,crypto_name,column_name,wanted_data,update_rate,kill_chrome,plot)
