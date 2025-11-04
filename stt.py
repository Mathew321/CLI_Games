import os
import json
import pyaudio
import subprocess 
from subprocess import DEVNULL
from vosk import Model, KaldiRecognizer, SetLogLevel

# ----------------------------------------------------
# 1. APPLICATION MAPPING AND COMMAND EXECUTION
# ----------------------------------------------------

apps = {
    "brave": "brave-browser",
    "kitty": "kitty",
    "discord": "Discord",
    "code": "code"
}

def instruction(cmd):
    """Executes a system command based on the recognized speech."""
    # Process the command once for stripping and lowercasing
    clean_cmd = cmd.strip().lower() 
    print(f"Executing: {clean_cmd}")
    
    # Split the command into parts for structured matching
    split_cmd = clean_cmd.split(" ")
    
    if len(split_cmd) >= 3: 
        
        # Match the "interpreter open" phrase
        match [split_cmd[0], split_cmd[1]]:
            case ["interpreter", "open"]:
                
                app_name_key = split_cmd[2]
                
                # Check if the target application is defined
                if app_name_key in apps:
                    
                    executable_name = apps[app_name_key]
                    print(f"Action: Opening {app_name_key} using executable '{executable_name}'")
                    
                    # --- Fully Detached Subprocess Execution ---
                    # Uses start_new_session=True and I/O redirection to ensure the 
                    # new app (e.g., kitty) survives the Python script's termination.
                    try:
                        subprocess.Popen(
                            [executable_name], 
                            start_new_session=True, 
                            stdin=DEVNULL, 
                            stdout=DEVNULL, 
                            stderr=DEVNULL
                        )
                    except FileNotFoundError:
                        print(f"Error: Executable '{executable_name}' not found. Check your system PATH.")
                
                else:
                    print(f"Command Error: Application '{app_name_key}' not defined.")

    # Catch-all for simple commands
    elif len(split_cmd) == 1:
        match clean_cmd:
            case "test":
                print("Action: Test successful!")
            case _:
                print(f"Command format '{clean_cmd}' not recognized.")
    else:
        print(f"Command format '{clean_cmd}' not recognized.")


# ----------------------------------------------------
# 2. VOSK SETUP AND MAIN LOOP
# ----------------------------------------------------

# Disable Vosk logs
SetLogLevel(-1) 

MODEL_PATH = '/home/jack/.config/hypr/stt/model' # Ensure this path is correct
SAMPLE_RATE = 16000
CHUNK_SIZE = 4096

# Define the custom vocabulary/grammar for high accuracy
custom_commands = [
    "interpreter open brave", 
    "interpreter open kitty", 
    "interpreter open discord", 
    "interpreter open code", 
    "test",
    "a", "the", "[unk]" # Include filler words and [unk]
]
grammar = json.dumps(custom_commands)

# Load the model and recognizer
model = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model, SAMPLE_RATE)
recognizer.SetGrammar(grammar) # APPLY THE CUSTOM GRAMMAR!

# Recognize from the microphone
cap = pyaudio.PyAudio()
stream = cap.open(format=pyaudio.paInt16, 
                  channels=1, 
                  rate=SAMPLE_RATE, 
                  input=True, 
                  frames_per_buffer=CHUNK_SIZE * 2)
stream.start_stream()

print("Voice Interpreter Active. Commands: interpreter open [app], test. Press Ctrl+C to stop.")

try:
    while True:
        data = stream.read(CHUNK_SIZE, exception_on_overflow=False)
        if len(data) == 0:
            break

        if recognizer.AcceptWaveform(data):
            # A full command is finalized
            result = json.loads(recognizer.Result())
            cmd = result.get('text', '').strip()
            
            if cmd:
                # 1. Execute the instruction
                instruction(cmd)
                # 2. Print final status
                print(f"--> FINAL: {cmd:<50}")
            
        else:
            # Continual real-time output while speaking
            partial = json.loads(recognizer.PartialResult())
            if partial.get('partial'):
                 print(f"PARTIAL: {partial['partial']}", end='\r')

except KeyboardInterrupt:
    print("\nStopping recognition...")
    # Get any remaining text
    final_result = json.loads(recognizer.FinalResult())
    if final_result.get('text'):
        print(f"--> Remaining: {final_result['text']}")

finally:
    # Cleanup resources
    stream.stop_stream()
    stream.close()
    cap.terminate()
    print("Recognition stream closed.")
