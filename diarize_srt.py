import sys

def seconds_to_hmsm(seconds):
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    milliseconds = int((seconds - int(seconds)) * 1000)
#    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"
    return f"{hours:02}:{minutes:02}:{seconds:02}"

def parse_srt(srt_data):
    subtitles = []
    for block in srt_data.split('\n\n'):
        if block.strip():
            lines = block.split('\n')
            if len(lines) >= 3:
                start_end = lines[1].split(' --> ')
                subtitles.append({'start': start_end[0], 'end': start_end[1], 'text': ' '.join(lines[2:])})
    return subtitles

def load_data(filename):
    data = []
    with open(filename, 'r') as file:
        for line in file:
            try:
                parts = line.strip().split()
                if len(parts) < 3:
                    print(f"Skipping malformed line: {line}")
                    continue
                start = seconds_to_hmsm(float(parts[0].split('=')[1].rstrip('s')))
                # start=parts[0].split('=')[1].rstrip('s')
                stop = seconds_to_hmsm(float(parts[1].split('=')[1].rstrip('s')))
                # stop=parts[1].split('=')[1].rstrip('s')
                speaker = parts[2]
                entry = {'start': start, 'stop': stop, 'speaker': speaker}
                data.append(entry)
            except Exception as e:
                print(f"Error processing line '{line}': {e}")
    return data


def remove_milliseconds(time_str):
    return time_str.split(',')[0]

def time_to_seconds(time_str):
    time_parts = time_str.split(',')
    hours, minutes, seconds = map(int, time_parts[0].split(':'))
    milliseconds = int(time_parts[1]) if len(time_parts) > 1 else 0
    return hours * 3600 + minutes * 60 + seconds + milliseconds / 1000.0

def is_within_interval(record, start_interval, end_interval):
    #just any coincidence of intervals is going to be considered as a match
    start_record = int(time_to_seconds(record['start']))
    stop_record = int(time_to_seconds(record['stop']))
    start_interval_sec = int(time_to_seconds(start_interval))
    end_interval_sec = int(time_to_seconds(end_interval))

    #print(f"start_interval={start_interval}, end_interval={end_interval}")
    #print(f"start_record={start_record}, stop_record={stop_record}, start_interval_sec={start_interval_sec}, end_interval_sec={end_interval_sec}")

    return  (start_record >= start_interval_sec and start_record <= end_interval_sec) or \
            (stop_record >= start_interval_sec and stop_record <= end_interval_sec) or \
            (start_interval_sec >= start_record and start_interval_sec <= stop_record) or \
            (end_interval_sec >= start_record and end_interval_sec <= stop_record)  

def get_speaker(data, start_time, end_time, last_speaker=None):
    for record in data:
        if is_within_interval(record, start_time, end_time):
            return record['speaker']
    print(f"WARNING: No speaker found for interval {start_time} - {end_time}")
    print(f"WARNING: Using last speaker: {last_speaker}")
    return last_speaker



def main():
    if len(sys.argv) != 4:
        print("Usage: python script.py <diarized_file> <str_file> <output_file>")
        sys.exit(1)
    diarized_file = sys.argv[1]
    data_diarization = load_data(diarized_file)
    print("data_diarization loaded: "+str(len(data_diarization))+" lines")
    srt_file=sys.argv[2]
    output_file=sys.argv[3]
    lines_kept=0
    with open(srt_file, 'r') as file:
        srt_data = file.read()
        subtitles = parse_srt(srt_data)
        print("subtitles loaded:"+str(len(subtitles))+" lines")
    with open(output_file, 'w') as file:
        last_speaker = None
        for subtitle in subtitles:
            start = subtitle['start']
            end = subtitle['end']
            # print(f"start={start}, end={end}")
            speaker = get_speaker(data_diarization,start,end,last_speaker)
            last_speaker = speaker
            file.write(f"{subtitle['start']} --> {subtitle['end']} {speaker}\n{subtitle['text']}\n\n")           
    print("Done")        
if __name__ == "__main__":
    main()
