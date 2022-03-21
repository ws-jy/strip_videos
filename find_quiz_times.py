import sys
from collections import defaultdict
time_stamps = defaultdict(list)

def scrape_times(file_string):
    if len(sys.argv) != 2:
        print('Usage: python3 find_quiz_times.py transcript.vtt')
        sys.exit(1)
    with open(file_string) as file:
        for line in file:
            if '-->' in line:
                split_times = line.split()
                start_time, end_time = split_times[0][:8], split_times[2][:8]
            
            # Should always have time_stamps['start'] and time_stamps['end']
            # the same length before adding new one
            # Put a mark if there is a problem
            elif 'quiz start' in line.lower() or 'quiz starts' in line.lower():
                if len(time_stamps['start']) != len(time_stamps['end']):
                    time_stamps['end'].append(start_time + '*')
                time_stamps['start'].append(start_time)
            
            # Time_stamps['start'] should always be one more than time_stamps['end']
            elif 'quiz end' in line.lower() or 'quiz ends' in line.lower():
                if len(time_stamps['end']) == len(time_stamps['start']):
                    time_stamps['start'].append(start_time + '*')
                time_stamps['end'].append(end_time)
                
def pair_times(file_string):
    print('The times are:')
    
    with open(f'quiz_times_in_{file_string}', 'w') as file:
        for i in range(len(time_stamps['start'])):
            check = ''
            if '*' in time_stamps['start'][i]:
                check = 'check_start'
                time_stamps['start'][i] = time_stamps['start'][i][:-1]
                print(time_stamps['start'][i])
            elif '*' in time_stamps['end'][i]:
                check = 'check_end'
                time_stamps['end'][i] = time_stamps['end'][i][:-1]
                print(time_stamps['end'][i])
            string = f'{i+1};' + time_stamps['start'][i] \
                           + ';' + time_stamps['end'][i] + f';{check}\n'
            
            print(f'''{i+1}: start: {time_stamps['start'][i]} ''' + 
                  f'''end: {time_stamps['end'][i]} {check}''')
            
            file.write(string)


def run():
    file_string = str(sys.argv[1])
    scrape_times(file_string)
    pair_times(file_string)
    
if __name__ == '__main__':
    run()