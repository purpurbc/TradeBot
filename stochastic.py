#all of the different sizes of the 
segment_sizes = {"minutes":1, #cant be 1 since 1-1=0
                    "hours":60,
                    "days":1440,
                    "weeks":10080,
                    "months":43200}  

def calc_stochastic_osc(values,cur_index,num_segments,segment_multitude,segment_type):

    segment_size = segment_multitude*segment_sizes[segment_type]
    c = values[cur_index]
    low = min(values[cur_index-(num_segments*segment_size):cur_index])
    high = max(values[cur_index-(num_segments*segment_size):cur_index])

    k = ((c - low)/(high - low))*100
    
    print(k)

    return k
