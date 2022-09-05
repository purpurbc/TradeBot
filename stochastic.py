import variables as vb


"""calculate the current stochastic oscillator value at the specified index"""
def calc_cur_stochastic_osc(values,cur_index,num_segments,segment_multitude,segment_type):

    segment_size = segment_multitude*vb.segment_sizes[segment_type] #size of one segment
    c = values[cur_index] #current cost

    #DEBUG
    #print(cur_index,",",num_segments*segment_size)

    #get the highest and lowest value and calculate  the difference
    low = min(values[cur_index-(num_segments*segment_size):cur_index+1]) 
    high = max(values[cur_index-(num_segments*segment_size):cur_index+1])
    diff = high - low

    #prevent division by zero
    if diff == 0: diff = 0.001
    
    #calculate the stochastic oscillator value
    k = ((c - low)/(diff))*100
    
    #DEBUG
    #print("c:",c," low:",low," high:",high," diff:",diff," segment_size:",segment_size," k:",k)

    return k

"""use the calc_cur_stochastic_value on the entire list of values"""
def calc_stochastic_osc(values,num_segments,segment_multitude,segment_type):

    segment_size = segment_multitude*vb.segment_sizes[segment_type] #size of one segment
    stochastics = []    #empty list for stochastic oscillator values
    indexes = []        #empty list for indexes

    stop = False        #stop indicator

    #iterate the list backwards. This way we always get a value for the current index
    for i in range(len(values)-1,-1,-(num_segments*segment_size)):

        #check if we have iterated over the whole list
        if i-(num_segments*segment_size) < 0: 
            #if so, stop after this iteration
            #also, set the index to the lowest possible
            i = num_segments*segment_size
            stop = True
            break

        #calculate the current stochastic oscillator value
        cur_stochastic = calc_cur_stochastic_osc(values,i,num_segments,segment_multitude,segment_type)
        
        #insert the values and indexes into the lists at the beginning
        stochastics.insert(0,cur_stochastic)
        indexes.insert(0,i)
        
        #break if the above criteria is met
        if stop: break

    return stochastics, indexes