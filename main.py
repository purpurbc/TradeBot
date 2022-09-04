import trade_bot as tb
import stochastic as st
import get_data as gd

url = 'https://tradingeconomics.com/solusd:cur' 
xpath = '//html/body/form/div[4]/div/div[2]/div/div[1]/div[1]/div/div/div[6]/table' 
crypto_name = 'Solana'
column_name = 'Unnamed: 0'
wanted_data = 'Actual'
update_rate = 60
kill_chrome = True
plot = True
store_file_name = 'saved_data/live_data'
saved_file_name = 'saved_data/live_data_180822'

tb.initiate_tradebot(store_file_name,saved_file_name,url,xpath,crypto_name,column_name,wanted_data,update_rate,kill_chrome,plot)

