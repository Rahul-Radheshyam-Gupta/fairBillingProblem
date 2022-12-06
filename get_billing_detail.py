import os
import sys
from datetime import datetime

input_user_list = sys.argv[1:]

with open('input.txt') as f:
    text_data = f.read()
    if text_data:
        # Getting Valid User Names from the passed inputs
        valid_user_list = [name for name in input_user_list if text_data.find(name) != -1]
        
        # Getting list of entries in string format
        splitted_text_list = text_data.split('\n')

        # Storing Earliest Start Entry for Further Usage 
        earliest_start, latest_log = splitted_text_list[0].split(), splitted_text_list[-1].split()
        earliest_start[0] = datetime.strptime(earliest_start[0], '%H:%M:%S')
        latest_log[0] = datetime.strptime(latest_log[0], '%H:%M:%S')

        final_user_static_list = []
        for user in valid_user_list:
            user_statics = [user, 0, 0]
            # Filter Entries for the current User Name
            filtered_text_list = filter(lambda x: x.find(user) != -1, splitted_text_list)
            data  = [ item.split() for item in filtered_text_list ]
            for x in data:
                x[0]=datetime.strptime(x[0], '%H:%M:%S') 

            # Setting Some Required Variables
            lastIndex = len(data) - 1
            all_index = set(range(len(data)))
            paired_index = set()

            for i in range(len(data)):
                # Skip current iteration if the current index is already paired
                if i in paired_index:
                    continue

                current_log = data[i]
                # Get all unpaired logs, also exclude current index i
                unpair_index = all_index - paired_index - {i}
                paired_index.add(i)

                if current_log[2] == 'Start':
                    # For last entry has Start log then dont add durations as its 0
                    if i == lastIndex:
                        user_statics[1] += 1
                        break
                    # For each Start entry, we will check its end pair, 
                    # if its present and then add duration and number of session by 1 and also update paired_index 
                    for j in unpair_index:
                        if data[j][2] == 'End':
                            duration = data[j][0] - current_log[0] 
                            user_statics[1] += 1
                            user_statics[2] += int(duration.total_seconds())
                            paired_index.add(j)
                            break

                else:
                    # If there is last entry with End then we will consider earliest log as start for the duration calculation
                    duration = current_log[0] - earliest_start[0] 
                    user_statics[1] += 1
                    user_statics[2] += int(duration.total_seconds())
            
            final_user_static_list.append(user_statics)

        # Finally printing output  
        for user_static in final_user_static_list:
            print(f"{user_static[0]} {user_static[1]} {user_static[2]}")