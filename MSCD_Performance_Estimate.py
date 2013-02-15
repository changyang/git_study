from pylab import *

usb_transfer_speed = 40.0 # MBytes/Second

def get_throughput(total_data = 1024 * 120,\
                   data_seg_length = 1024 * 4,\
                   data_consume_speed = 25.0,\
                   interrupt_latency = 10.0,\
                   schedule_latency = 10.0,\
                   CBW_CSW_Gap = 0.0):

    last_segment_is_short_one = False

    num_of_seg = total_data // data_seg_length

    if (0 != total_data % data_seg_length):
        last_segment_is_short_one = True
        last_segment_length = total_data % data_seg_length

    CBW_Time = interrupt_latency + schedule_latency

    # Time for data transmission over USB Bus
    data_transfer_time = data_seg_length / usb_transfer_speed

    # Time for read/write payload data
    if (200.0 != data_consume_speed):
        data_comsume_time = data_seg_length / data_consume_speed
    else:
        data_comsume_time = 0 # This means no data copy needed

    DATA_Time = (data_transfer_time + interrupt_latency + data_comsume_time)\
                * num_of_seg

    if (last_segment_is_short_one == True):
        DATA_Time += last_segment_length / usb_transfer_speed\
                     + interrupt_latency
        if (data_comsume_time != 0):
            DATA_Time += last_segment_length / data_consume_speed

    DATA_Time = DATA_Time + schedule_latency

    CSW_Time = interrupt_latency + schedule_latency

    mscd_throughput = total_data / (CBW_Time + DATA_Time + CSW_Time + CBW_CSW_Gap)

    #    print("For single buffer case:")
    #    print "Data phase length is", total_data // 1024, 'KBytes'
    #    print "When data segment length is:", data_seg_len, 'Bytes'
    #    if (data_comsume_speed != 200.0):
    #        print "Data consuming speed is", data_comsume_speed,
    #        print "Mbytes/Second"
    #    else:
    #        print("And no data copy needed")

    #    print 'Latency is', interrupt_latency, 'microseconds'

    #    print "Throughput expected is: ",
    #    print mscd_throughput,
    #    print "MBytes/Second"
    #    print

    return mscd_throughput

class mscd_parameters:
    param_index= 0
    possible_value_list = []
    def __init__(self, index, values):
        self.param_index = index
        self.possible_value_list = values

    def get_index(self):
        return param_index


color_list = ['blue', 'green', 'red', 'cyan', 'magenta', 'yellow', 'black']

# Length of data phase
total_data_fixed = True
total_data_default = 1024 * 120
total_data_list = [1024 * 64, 1024 * 120]
total_data_list_label = ['64kBytes', '120kBytes']

# Data segment or buffer length
data_seg_length_fixed = False
data_seg_length_default = 1024 * 4
data_seg_length_list = [512, 1024, 2048, 1024 * 3, 4096, 8192, 1024 * 16]
data_seg_length_label = ["0.5k", "1k", '2k', '3k', '4k', '8k', '16k']


# How fast the data in buffer could be read out from or write into chip
data_consume_speed_fixed = True
data_consume_speed_default = 10.0 # MBytes/Second
data_consume_speed_list = [4.0, 10.0, 25.0, 30.0, 95.0, 200.0]
data_consume_speed_list_label = ['4.0MB/s', '10.0MB/s', '25.0MB/s', '30.0MB/s', '95.0MB/s', "Infinite"]

interrupt_latency_fixed = True
interrupt_latency_default = 100.0 # microseconds
interrupt_latency_list = [1.0, 5.0, 10.0, 20.0, 50.0, 80.0, 100.0, 120.0, 150.0, 200.0, 250.0]
interrupt_latency_list_label = ['1.0uS', '5.0uS', '10.0uS', '20.0uS', '50.0uS', '80.0uS', '100.0uS', '120.0uS', '150.0uS', '200.0uS', '250.0uS']

schedule_latency_fixed = True
schedule_latency_default  = 100.0 # microseconds
schedule_latency_list =  [1.0, 5.0, 10.0, 20.0, 50.0, 80.0, 100.0, 120.0, 150.0, 200.0, 250.0]
schedule_latency_list_label = ['1.0uS', '5.0uS', '10.0uS', '20.0uS', '50.0uS', '80.0uS', '100.0uS', '120.0uS', '150.0uS', '200.0uS', '250.0uS']

#CBW_CSW_Gap = 0.0 #microseconds

throughput_param_list =\
[total_data_default,            # 0
 data_seg_length_default,       # 1
 data_consume_speed_default,    # 2
 interrupt_latency_default,     # 3
 schedule_latency_default]      # 4


def GetParamIndex(param_list):
    if (param_list == total_data_list):
        return 0
    if (param_list == data_seg_length_list):
        return 1
    if (param_list == data_consume_speed_list):
        return 2
    if (param_list == interrupt_latency_list):
        return 3
    if (param_list == schedule_latency_list):
        return 4

    print "Wrong parameter list\n"
    exit(-2)
    return

def GetNameFromIndex(index):
    if (index == 0):
        return "Data phase length"
    if (index == 1):
        return "Data segment length"
    if (index == 2):
        return "Data consuming speed"
    if (index == 3):
        return "Interrupt latency"
    if (index == 4):
        return "Schedule lantency"

    print "Wrong index value"
    exit(-3)


result_list_label = ['0.0 MBytes/S']


#param_list = [0.0]




major_param_values = data_seg_length_list
major_param_values_label = data_seg_length_label

minor_param_values = interrupt_latency_list
minor_param_values_label = interrupt_latency_list_label

#minor_param_values = data_consume_speed_list
#minor_param_values_label = data_consume_speed_list_label

#minor_param_values = total_data_list
#minor_param_values_label = total_data_list_label






i = 0
current_line = 0
major_param_index = GetParamIndex(major_param_values)
minor_param_index = GetParamIndex(minor_param_values)

for minor_param in minor_param_values:
    throughput_param_list[minor_param_index] = minor_param
    result_matrix = []
    result = [0.0]
    plot_x = [0.0]

    for major_param in major_param_values:
        throughput_param_list[major_param_index] = major_param

        throughput = get_throughput(
            total_data = throughput_param_list[0],
            data_seg_length = throughput_param_list[1],
            data_consume_speed = throughput_param_list[2],
            interrupt_latency = throughput_param_list[3],
            schedule_latency = throughput_param_list[4],
            CBW_CSW_Gap = 0.0)

        plot_x.append(major_param)
        result.append(throughput)
        result_list_label.append(('%.3f' % throughput) + "MBytes/S")
        result_matrix.append((major_param, throughput))

#    print '\n\n\nminor_param is', minor_param
#    for (x, y) in result_matrix:
#        print x, '\t\t\t', y
    xticks(major_param_values, major_param_values_label)
    plot(plot_x, result, linestyle='-', marker='o', color=color_list[i], label=minor_param_values_label[current_line])
    i = (i + 1) % len(color_list)
    current_line += 1

legend(loc='lower right')
other_parameters = 'Other parameters:\n'
for i in range(len(throughput_param_list)):
    if (i != major_param_index and i != minor_param_index):
        other_parameters = other_parameters + GetNameFromIndex(i) + ': %.1f' % throughput_param_list[i] + '\n'

print other_parameters

text(max(plot_x)/2, max(result)/2, other_parameters)

show()

exit(0)













# Check parameter fixed flags
flag_list = [total_data_fixed, data_seg_length_fixed, data_consume_speed_fixed, interrupt_latency_fixed, schedule_latency_fixed]

if (flag_list.count(False) > 1):
    print "Number of fixed parameter greater than ONE, error case\n"
    exit(-1)



# Process data phase length change effect
if (total_data_fixed == False):
    for total_data in total_data_list:

        throughput = get_throughput(total_data,\
            data_seg_length,\
            data_consume_speed,\
            interrupt_latency,\
            schedule_latency,\
            CBW_CSW_Gap)
        param_list.append(total_data)
        result_list.append(throughput)
        result_list_label.append(('%.3f' % throughput) + "MBytes/S")
        result_matrix.append((total_data, throughput))

    plot(param_list, result_list, linestyle=':', marker='o')
    title('Data phase size Vs Throughput')
    xlabel('Data phase size')
    ylabel('Throughput')
    yticks(result_list, result_list_label)
    xticks(total_data_list, total_data_list_label)
    show()

    print "Data phase length", "\t\t", "Throughput"
    for (x,y) in result_matrix:
        print x, '\t\t', y

# Process data segment length change effect
if (data_seg_length_fixed == False):
    for data_seg_length in data_seg_length_list:
    #        print "When data segment length is ", data_seg_length
        throughput = get_throughput(total_data,\
            data_seg_length,\
            data_consume_speed,\
            interrupt_latency,\
            schedule_latency,\
            CBW_CSW_Gap)
        param_list.append(data_seg_length)
        result_list.append(throughput)
        result_list_label.append(('%.3f' % throughput) + " MBytes/S")
        result_matrix.append((data_seg_length, throughput))

    print "Data segment length", "\t\t", "Throughput"

    plot(param_list, result_list, linestyle=':', marker='o')
    title('Data segment size Vs Throughput')
    xlabel('Data segment size')
    ylabel('Throughput')
    yticks(result_list, result_list_label)
    xticks(data_seg_length_list, data_seg_length_label)
    show()

    for (x,y) in result_matrix:
        print x, '\t\t\t\t', y

# Process data consume speed change effect
if (data_consume_speed_fixed == False):
    for data_consume_speed in data_consume_speed_list:
        print "When data consume speed is ", data_consume_speed, "MBytes/Second"
        throughput = get_throughput(total_data,\
            data_seg_length,\
            data_consume_speed,\
            interrupt_latency,\
            schedule_latency,\
            CBW_CSW_Gap)

        param_list.append(data_consume_speed)
        result_list.append(throughput)
        result_list_label.append(('%.3f' % throughput) + "MBytes/S")
        result_matrix.append((data_consume_speed, throughput))

    print "Data Consume speed", "\t\t", "Throughput"

    plot(param_list, result_list, linestyle=':', marker='o')
    title('Data consume speed Vs Throughput')
    xlabel('Data consume speed')
    ylabel('Throughput')
    yticks(result_list, result_list_label)
    xticks(data_consume_speed_list, data_consume_speed_list_label)
    show()

    for (x,y) in result_matrix:
        print x, '\t\t', y

# Process interrupt latency change effect
if (interrupt_latency_fixed == False):
    for interrupt_latency in interrupt_latency_list:
        print "When interrupt latency is ", interrupt_latency, "uS"
        throughput = get_throughput(total_data,\
            data_seg_length,\
            data_consume_speed,\
            interrupt_latency,\
            schedule_latency,\
            CBW_CSW_Gap)

        param_list.append(interrupt_latency)
        interrupt_latency_list_label.append('%.1f' % interrupt_latency + 'uS')

        result_list.append(throughput)
        result_list_label.append('%.3f' % throughput + "MBytes/S")
        result_matrix.append((interrupt_latency, throughput))

    print "Interrupt latency", "\t\t", "Throughput"

    plot(param_list, result_list, linestyle=':', marker='o')
    title('Interrupt latency speed Vs Throughput')
    xlabel('Interrupt latency')
    ylabel('Throughput')
    yticks(result_list, result_list_label)
    xticks(interrupt_latency_list, interrupt_latency_list_label)
    show()

    for (x,y) in result_matrix:
        print x, '\t\t', y


# Process schedule latency change effect
if (schedule_latency_fixed == False):
    for schedule_latency in schedule_latency_list:
        print "When interrupt latency is ", schedule_latency_list, "uS"
        throughput = get_throughput(total_data,\
            data_seg_length,\
            data_consume_speed,\
            interrupt_latency,\
            schedule_latency,\
            CBW_CSW_Gap)

        param_list.append(schedule_latency)
        schedule_latency_list_label.append('%.1f' % schedule_latency + 'uS')

        result_list.append(throughput)
        result_list_label.append('%.3f' % throughput + "MBytes/S")
        result_matrix.append((schedule_latency, throughput))

    print "Schedule latency", "\t\t", "Throughput"

    plot(param_list, result_list, linestyle=':', marker='o')
    title('Schedule latency speed Vs Throughput')
    xlabel('Schedule latency')
    ylabel('Throughput')
    yticks(result_list, result_list_label)
    xticks(schedule_latency_list, schedule_latency_list_label)
    show()

    for (x,y) in result_matrix:
        print x, '\t\t', y


# Only need to calcuate one value
if (flag_list.count(False) == 0):
    throughput = get_throughput(total_data,\
        data_seg_length,\
        data_consume_speed,\
        interrupt_latency,\
        schedule_latency,\
        CBW_CSW_Gap)
    print "Throughput is %f MBytes/Seconds" % throughput


