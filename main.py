import trade_bot as tb
import stochastic as st
import data_management as dm
import variables as vb

tb.initiate_tradebot(vb.store_file_name,vb.saved_file_name,vb.url,vb.xpath,
                     vb.crypto_name,vb.column_name,vb.wanted_data,
                     vb.update_rate,vb.kill_chrome,vb.plot)

