import requests
import os
import io
from pydub import AudioSegment
from datetime import datetime, timedelta
import time

# Stream URL (pls file)
pls_url = "http://localhost:8000/listen.pls?sid=1"

# Directory to save recordings
save_directory = "recordings"

# Duration of each recording in minutes
recording_duration = 30

# Retention period for recordings in days
retention_period = 30

# Ensure the save directory exists
if not os.path.exists(save_directory):
    os.makedirs(save_directory)

def delete_old_recordings():
    """Delete recordings older than the retention period."""
    now = time.time()
    cutoff = now - (retention_period * 86400)  # 86400 seconds in a day

    for filename in os.listdir(save_directory):
        file_path = os.path.join(save_directory, filename)
        if os.path.isfile(file_path):
            file_creation_time = os.path.getctime(file_path)
            if file_creation_time < cutoff:
                os.remove(file_path)
                print(f"Deleted: {file_path}")

def get_stream_url(pls_url):
    """Extract the actual stream URL from the .pls file."""
    response = requests.get(pls_url)
    if response.status_code == 200:
        for line in response.text.splitlines():
            if line.startswith("File1="):
                return line.split('=', 1)[1]
    raise Exception("Unable to extract stream URL from .pls file")

def record_shoutcast_stream():
    try:
        stream_url = get_stream_url(pls_url)
        while True:
            # Calculate end time for this recording segment
            end_time = datetime.now() + timedelta(minutes=recording_duration)
            
            # Prepare filename with current timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            temp_filename = os.path.join(save_directory, f"temp_recording_{timestamp}.mp3")
            final_filename = os.path.join(save_directory, f"recording_{timestamp}.mp3")
            
            # Open a stream and start recording
            response = requests.get(stream_url, stream=True)
            
            try:
                print("Recording...")
                with open(temp_filename, 'wb') as temp_file:
                    for chunk in response.iter_content(chunk_size=1024):
                        temp_file.write(chunk)
                        if datetime.now() >= end_time:
                            break
                
                # Load the temporary file with pydub and export as final mp3
                audio_segment = AudioSegment.from_file(temp_filename)
                audio_segment.export(final_filename, format="mp3")
                print(f"Saved: {final_filename}")
                
                # Delete the temporary file
                os.remove(temp_filename)
                
                # Delete old recordings
                delete_old_recordings()
                
            except Exception as e:
                print(f"Recording error: {e}")
                if os.path.exists(temp_filename):
                    os.remove(temp_filename)
                continue
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    record_shoutcast_stream()
