# Shoutcast Stream Recorder

This script records a Shoutcast stream in 30-minute segments, uploads the recordings to Dropbox, and deletes the local recordings after 30 days. The script is designed to run continuously, checking every minute to start a new recording if the previous one has finished.

## Features

- Records a Shoutcast stream in 30-minute segments.
- Uploads the recordings to Dropbox.
- Deletes local recordings older than 30 days.
- Displays recording progress and status messages.
- Handles connection errors and retries.

## Prerequisites

- Python 3.x
- `requests` library
- `dropbox` library

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/your-username/shoutcast-stream-recorder.git
   cd shoutcast-stream-recorder
Create a virtual environment and activate it (optional but recommended):
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
Run the script:
python main.py
Configuration
Stream URL: The script is currently configured to record from http://localhost:8000/index.html?sid=1. You can change this URL in the script.
Recording Duration: The recording duration is set to 30 minutes by default. You can change this value in the script.
Save Directory: The recordings are saved to a directory named recordings before being uploaded to Dropbox. You can change this directory in the script.

Troubleshooting
Connection Errors: If the script cannot connect to the stream, it will print an error message and retry after 60 seconds.


Replace `https://github.com/your-username/shoutcast-stream-recorder.git` with the actual URL of your GitHub repository. This `README.md` file provides an overview of the script, installation instructions, usage, configuration options, script explanation, example output, and troubleshooting tips.
