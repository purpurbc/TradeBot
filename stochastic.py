#all of the different sizes of the 
segment_sizes = {"minutes":1, #cant be 1 since 1-1=0
                    "hours":60,
                    "days":1440,
                    "weeks":10080,
                    "months":43200}  

def calc_cur_stochastic_osc(values,cur_index,num_segments,segment_multitude,segment_type):

    segment_size = segment_multitude*segment_sizes[segment_type]
    c = values[cur_index]
    print(cur_index,",",num_segments*segment_size)

    low = min(values[cur_index-(num_segments*segment_size):cur_index+1])
    high = max(values[cur_index-(num_segments*segment_size):cur_index+1])
    diff = high - low
    if diff == 0: diff = 0.001
    
    k = ((c - low)/(diff))*100
    
    print("c:",c," low:",low," high:",high," diff:",diff," segment_size:",segment_size," k:",k)

    return k

def calc_stochastic_osc(values,num_segments,segment_multitude,segment_type):

    segment_size = segment_multitude*segment_sizes[segment_type]
    stochastics = []
    indexes = []

    stop = False

    for i in range(len(values)-1,-1,-(num_segments*segment_size)):

        if i-(num_segments*segment_size) < 0: 
            i = num_segments*segment_size
            stop = True

        cur_stochastic = calc_cur_stochastic_osc(values,i,num_segments,segment_multitude,segment_type)
        
        stochastics.insert(0,cur_stochastic)
        indexes.insert(0,i)

        if stop: break

    return stochastics, indexes