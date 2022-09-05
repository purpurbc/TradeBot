import copy
import variables as vb

"""calculate the current SMA from the provided current index"""
def calc_cur_SMA(cur_index,values,num_segments,segment_multitude,segment_type):

    """ segment = segment_multitude + segment_type. ex: 5minutes, 1hour etc...
            segment_multitude: 2, 4, 6 etc...
            segment_type: minutes, hours, days etc..."""

    #quick check if some of the input is valid
    if segment_multitude < 0:
        print("Error: segment_size must be positive\n")
        return
    if cur_index < 0:
        print("Error: cur_index must be positive\n")
        return
    if segment_type not in vb.segment_sizes:
        print("Error: segment_type must be positive\n")
        return
    
    #calculate the segment_size 
    segment_size = segment_multitude*vb.segment_sizes[segment_type]

    #list for containing the segments closing value
    segment_values = []

    #append all of the segment closing values to that list
    for i in range(num_segments):

        #check if the segment_size fit in the provided previous data
        if segment_size > cur_index and cur_index != 0:
            #if not, reduce the segmentssize to be equal to the number of elements that are left
            segment_size = cur_index

        #go to the next segment
        cur_index -= segment_size

        #append closing value to list
        segment_values.append(values[cur_index])

    #calculate the SMA and return it
    return sum(segment_values)/len(segment_values)

"""calculate EMA for one period from the provided current index"""
def calc_cur_EMA(cur_index,values,num_segments,segment_multitude,segment_type,decay,pre_EMA=None):

    #quick check if some of the input is valid
    if segment_multitude < 0:
        print("Error: segment_size must be positive\n")
        return
    if cur_index < 0:
        print("Error: cur_index must be positive\n")
        return
    if segment_type not in vb.segment_sizes:
        print("Error: segment_type must be positive\n")
        return

    #start EMA ( SMA )
    if pre_EMA is None:
        pre_EMA = calc_cur_SMA(cur_index,values,num_segments,segment_multitude,segment_type)

    #todays price
    value_today = values[cur_index]

    #multiplier
    a = (decay/(1+num_segments))

    #todays EMA
    EMA_today = (value_today*a)+(pre_EMA*(1-a))

    return EMA_today

"""calculate EMA for all of the periods of the values provided"""
def calc_EMA(cur_index,values,num_segments,segment_multitude,segment_type,decay):

    #quick check if some of the input is valid
    if segment_multitude < 0:
        print("Error: segment_size must be positive\n")
        return
    if cur_index < 0:
        print("Error: cur_index must be positive\n")
        return
    if segment_type not in vb.segment_sizes:
        print("Error: segment_type must be positive\n")
        return

    #the size of each segment (1 minute, 5 minutes, 3 hours, 1 day etc.)
    segment_size = segment_multitude*vb.segment_sizes[segment_type]

    #lists for EMA values and each corresponding index
    EMA_values = []
    indexes = []

    #current and previous EMA values
    cur_EMA = 0
    pre_EMA = None

    #start at the nth segment and from there step one segment forward each time
    for per_index in range((num_segments*segment_size)-1,len(values),segment_size):

        #calculate the current EMA value
        cur_EMA = calc_cur_EMA(per_index,values,num_segments,segment_multitude,segment_type,decay,pre_EMA)

        #save the index and the EMA value
        indexes.append(per_index)
        EMA_values.append(cur_EMA)

        #update the previous EMA value
        pre_EMA = copy.copy(cur_EMA)
    
    return EMA_values, indexes