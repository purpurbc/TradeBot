#------------------------------
#--VARIABLES FOR THE TRADEBOT--
#------------------------------

#webpage we retrieve the data from
url = 'https://tradingeconomics.com/solusd:cur' 

#xpath at the url above. Used to access the right table
xpath = '//html/body/form/div[4]/div/div[2]/div/div[1]/div[1]/div/div/div[6]/table' 

#name of the crypto we want to reach in the above table
crypto_name = 'Solana'

#name of the column that contains the wanted_data
column_name = 'Unnamed: 0'

#the name of the wanted data. "Actual" is the price
wanted_data = 'Actual'

#the rate in seconds that we want to wait between each read of the html
update_rate = 60

#if we want to kill all chrome processes or not. Closes the active window also
kill_chrome = True

#if we want to plot a graph or not
plot = True

#the name of the file that we store the retrieved data to
store_file_name = 'saved_data/live_data'

#the name of the file that we load data from
saved_file_name = 'saved_data/live_data_180822'

#all of the available segment_sizes
segment_sizes = {"minutes":1, 
                    "hours":60,
                    "days":1440,
                    "weeks":10080,
                    "months":43200}  

"""prints the name of the arguments passed to the function as well as its value,
but only if the variable is in the global scope"""
def print_variables(*argv):
    for arg in argv:
        try:
            print("\t",[name for name in globals() if globals()[name] is arg][0],": ",arg)
        except Exception as e:
            print(e) 
    print("\n")