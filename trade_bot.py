import data_management as dm
import plot_management as pm
import ema_and_sma as es
import stochastic as st
import variables as vb

import matplotlib.pyplot as plt
import itertools as it
import atexit
import os 
import time


#col_list = ['unix', 'date', 'symbol', 'open', 'high', 'low', 'close', 'Volume ETH', 'Volume USD']
#dm.get_csv_data("Bitstamp_ETHUSD_1h.csv","open",col_list,32743,True)

"""kill all of the chrome processes. Active window will be closed as well"""
def kill_chrome_processes():
    #subprocess.call("TASKKILL /f  /IM  CHROME.EXE")
    browserExe = "chrome.exe" 
    os.system("taskkill /f /im "+browserExe) 

"""start the tradebot"""
def initiate_tradebot(store_file_name,saved_file_name,url_name,xpath,crypto_name,column_name,wanted_data,update_rate,kill_chrome,plot):
    
    #kill all of the chrome processes when we start
    #subprocesses of chrome are added every time we run the program
    #if we dont kill them, the memory will get full
    #this will unfortunately close the active browser window also
    #atexit didnt work, would have used it otherwise. Now we kill beforehand instead
    if kill_chrome: kill_chrome_processes()
    
    #get the saved data. If no saved data is available, an empty list is created
    data_values, time_values = dm.get_saved_data(saved_file_name)
    
    step_size = 5 #the space between each x_label
    fail_count = 0 #how many times the program has failed
    fail_limit = 5 #how many times the program is allowed to fail

    #PROVISORISK
    #stylesheet for the graph
    if plot:
        plt.rc('lines', linewidth = 1, color = 'r')
        plt.rc('axes', facecolor='#E6E6E6', edgecolor='none',axisbelow=True)
        plt.rc('xtick', direction='inout', color='gray',labelsize=6)
        plt.rc('ytick', direction='out', color='gray')
        plt.rc('patch', ec='#E6E6E6', force_edgecolor=True)

    #set size
    plt.gcf().set_size_inches(14,5)
    
    #loop until termination or fail_limit is reached
    for i in it.count(start=1):
        try:
            print("Webscrape initiated!\n\nTradeBot info:\n")
            
            #print the tradebot info
            vb.print_variables(store_file_name,saved_file_name,url_name,xpath,crypto_name,column_name,wanted_data,update_rate,kill_chrome,plot)
            
            #load the webpage and get the driver
            driver = dm.load_webpage(url_name,10)

            print("Reading HTML table...")
            #read the html and get the dataframe from the table
            #initial read to get the index below
            df = dm.read_html(driver,xpath)
            print("HTML table read! List of dataframes created\n")

            #search the dataframe for the crypto_name at the column_name
            index = dm.search_in_dataframe(df,crypto_name,column_name,30)

            print("Start webscraping!\n") 

            #loop until termination of the program
            for j in it.count(start=1):
                
                #read the html to get the updated dataframe
                df = dm.read_html(driver,xpath)

                #log and save all of the data, i.e. update the lists and write to file
                dm.log_and_save_data(data_values,time_values,store_file_name,df,wanted_data,index)
        
                #TEST
                #EMA values
                EMA_x = []
                EMA_values,indexes = es.calc_EMA(len(data_values)-1,data_values,10,4,"minutes",2)  
                for i in indexes: EMA_x.append(time_values[i])
       
                #TEST
                #stochastic oscillator values
                stoch_x = []
                stoch_values, indx = st.calc_stochastic_osc(data_values,14,1,"minutes")
                for i in indx: stoch_x.append(time_values[i])
             
                #PROVISORISK
                #plot a graph/update the currently plotted graph
                if plot:
                    
                    #set the title of the plot
                    plt.suptitle('tradeBot')

                    #set xlabel spacings
                    pm.set_plt_xticks(len(time_values),step_size)

                    #plot everything
                    pm.plot_graph(data_values,time_values,crypto_name,'r')
                    pm.plot_graph(EMA_values,EMA_x,"EMA",'b')
                    
                    #annotate max and min
                    pm.annot(data_values,range(len(time_values)),'min')
                    pm.annot(data_values,range(len(time_values)),'max')
                        
                    #legend, pause and clear
                    plt.legend()
                    plt.pause(update_rate)
                    plt.clf()

                else:
                    #if we dont want to plot 
                    time.sleep(update_rate)

            plt.show()

        #resume if not fail_limit has been reached        
        except Exception as e: 
            fail_count += 1
            print(e,"\nTrying to resume... (", fail_count, "/",fail_limit,")\n")
            if fail_count >= fail_limit: break
          
    #close the chromedriver at exit
    atexit.register(dm.quit_chromedriver,driver=driver)  


