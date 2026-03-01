import speech_recognition as sr  # For speech recognition
import threading  # For multithreading
import subprocess  # For running external commands
import os  # For executing system commands
import pyttsx3  # For text-to-speech
import time  # For delays
import queue  # For handling voice command queue

# Initialize speech recognizer
recognizer = sr.Recognizer()

# Initialize text-to-speech engine
engine = pyttsx3.init()

# Lock for controlling speech access
speech_lock = threading.Lock()

def speak(text):
    """Convert text to speech, ensuring only one instance at a time."""
    with speech_lock:
        engine.say(text)
        engine.runAndWait()

# Define the voice assistant class
class VoiceAssistant:
    def __init__(self):
        self.microphone = sr.Microphone()
        # Queue to avoid duplicate commands
        self.command_queue = queue.Queue()
        # Greet the user at startup
        self.greet_user()

    def greet_user(self):
        """Greet the user when the assistant starts."""
        greeting = "Good Morning."
        print(greeting)
        speak(greeting)

    def recognize_speech(self):
        """Capture and convert voice input to text with a timeout."""
        with self.microphone as source:
            recognizer.adjust_for_ambient_noise(source)
            print("Listening for voice input...")
            try:
                # Timeout to handle long periods of silence (5 seconds) and phrase length limit (10 seconds)
                audio_data = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            except sr.WaitTimeoutError:
                print("Listening timed out while waiting for phrase.")
                return ""  # Return empty if no speech was detected within timeout
        
        try:
            # Convert audio to text using Google Speech Recognition
            command_text = recognizer.recognize_google(audio_data)
            print(f"User said: {command_text}")
            return command_text.lower()  # Convert text to lowercase for consistency
        except sr.UnknownValueError:
            print("Didn't catch that.")
        except sr.RequestError as e:
            error_msg = f"Could not request from Speech Recognition: {e}"
            print(error_msg)
            speak(error_msg)
        
        return ""  # Return empty string if no valid speech is recognized

    def process_command(self, command_text):
        """Process the voice command and perform actions."""
        if not command_text:
            return

        # Avoid duplicate commands in quick succession
        if self.command_queue.qsize() > 0 and self.command_queue.queue[-1] == command_text:
            print("Duplicate command ignored.")
            return

        self.command_queue.put(command_text)

        current_time = time.time()
        self.last_command_time = current_time

        if "can you hear me" in command_text:
            response = "Yes, how can I help?"
            print(response)
            speak(response)
            return
        if "pancakes" in command_text:
            response = "thats not my name"
            print(response)
            speak(response)
            return
        if "hello" in command_text or "hi kiri" in command_text or "hey kiri" in command_text or "hi" in command_text:
            response = "Hi"
            print(response)
            speak(response)
            return
        if "who are you" in command_text or "what is your name" in command_text:
            response = "I am Kiri, your personal assistant on Ubuntu."
            print(response)
            speak(response)
            return
        if "how are you" in command_text:
            response = "I am functioning perfectly. How can I help you today?"
            print(response)
            speak(response)
            return
        if "what can you do" in command_text:
            response = "I can open applications, manage system settings, and update your Ubuntu system."
            print(response)
            speak(response)
            return

        # Check for specific update, upgrade, or autoremove commands
        if "update" in command_text:
            self.update_system()
            return
        if "upgrade" in command_text:
            self.upgrade_system()
            return
        if "remove" in command_text:
            self.autoremove_system()
            return

        self.execute_system_command(command_text)

    def execute_system_command(self, command_text):
        """Map voice commands to Ubuntu system actions using non-blocking subprocesses."""
        response = ""
        
        if "firefox" in command_text:
            subprocess.Popen(["firefox &"], shell=True)
            response = "Opening Firefox"
        elif "terminal" in command_text:
            subprocess.Popen(["gnome-terminal"])
            response = "Opening Terminal"
        elif "shut down" in command_text:
            response = "Shutting down the system in 10 seconds"
            print(response)
            speak(response)
            time.sleep(10)
            subprocess.Popen(["pkexec", "shutdown", "now"])
        elif "restart" in command_text:
            response = "Rebooting 3 2 1"
            print(response)
            speak(response)
            time.sleep(3)
            subprocess.Popen(["pkexec", "reboot"])
        elif "lock it" in command_text:
            subprocess.Popen(["gnome-screensaver-command", "-l"])
            response = "Locking the screen"
        elif "task" in command_text:
            subprocess.Popen(["gnome-system-monitor"])
            response = "Opening task manager"
        elif "folder" in command_text:
            subprocess.Popen(["nautilus"])
            response = "Opening File Manager"
        elif "thunder" in command_text:
            subprocess.Popen(["thunderbird"])
            response = "Opening thunderbird"
        elif "graphics" in command_text:
            subprocess.Popen(["gimp"])
            response = "Opening GIMP"
        elif "calculator" in command_text:
            response = "Opening calculator"
            subprocess.Popen(["gnome-calculator"])
        elif "google chrome" in command_text:
            response = "Opening Google Chrome"
            subprocess.Popen(["google-chrome"])
        elif "photoshop" in command_text:
            response = "Opening Gimp"
            subprocess.Popen(["gimp"])
        elif "system settings" in command_text:
            subprocess.Popen(["gnome-control-center"])
            response = "Opening system settings"
        elif "text editor" in command_text or "gedit" in command_text:
            subprocess.Popen(["gedit"])
            response = "Opening text editor"
        elif "calendar" in command_text:
            subprocess.Popen(["gnome-calendar"])
            response = "Opening calendar"
        elif "weather" in command_text:
            subprocess.Popen(["gnome-weather"])
            response = "Opening weather"
        elif "maps" in command_text:
            subprocess.Popen(["gnome-maps"])
            response = "Opening maps"
        elif "videos" in command_text or "video player" in command_text:
            subprocess.Popen(["totem"])
            response = "Opening video player"
        elif "music" in command_text or "music player" in command_text:
            subprocess.Popen(["rhythmbox"])
            response = "Opening music player"
        elif "photos" in command_text or "picture" in command_text:
            subprocess.Popen(["eog"])
            response = "Opening image viewer"
        elif "camera" in command_text or "webcam" in command_text:
            subprocess.Popen(["cheese"])
            response = "Opening camera"
        elif "screenshot" in command_text:
            subprocess.Popen(["gnome-screenshot"])
            response = "Taking a screenshot"
        elif "libreoffice" in command_text or "office" in command_text:
            subprocess.Popen(["libreoffice"])
            response = "Opening LibreOffice"
        elif "word document" in command_text or "writer" in command_text:
            subprocess.Popen(["libreoffice", "--writer"])
            response = "Opening word processor"
        elif "spreadsheet" in command_text or "excel" in command_text:
            subprocess.Popen(["libreoffice", "--calc"])
            response = "Opening spreadsheet"
        elif "presentation" in command_text or "powerpoint" in command_text:
            subprocess.Popen(["libreoffice", "--impress"])
            response = "Opening presentation"
        elif "software update" in command_text or "app store" in command_text or "software center" in command_text:
            subprocess.Popen(["gnome-software"])
            response = "Opening software center"
        elif "disk utility" in command_text:
            subprocess.Popen(["gnome-disks"])
            response = "Opening disk utility"
        elif "pdf" in command_text or "document viewer" in command_text:
            subprocess.Popen(["evince"])
            response = "Opening document viewer"
        elif "bluetooth settings" in command_text:
            subprocess.Popen(["gnome-control-center", "bluetooth"])
            response = "Opening Bluetooth settings"
        elif "wifi" in command_text or "wi-fi" in command_text or "y-fi" in command_text or "network settings" in command_text or "internet settings" in command_text:
            subprocess.Popen(["gnome-control-center", "wifi"])
            response = "Opening Network settings"
        elif "volume up" in command_text or "increase volume" in command_text:
            subprocess.Popen(["amixer", "-D", "pulse", "sset", "Master", "10%+"])
            response = "Increasing volume"
        elif "volume down" in command_text or "decrease volume" in command_text:
            subprocess.Popen(["amixer", "-D", "pulse", "sset", "Master", "10%-"])
            response = "Decreasing volume"
        elif "mute sound" in command_text or "mute volume" in command_text:
            subprocess.Popen(["amixer", "-D", "pulse", "sset", "Master", "toggle"])
            response = "Toggling volume mute"
        elif "empty trash" in command_text:
            subprocess.Popen(["gio", "trash", "--empty"])
            response = "Emptying trash"
        else:
            response = self.generate_chat_response(command_text)

        if response:
            print(response)
            speak(response)

    def generate_chat_response(self, command_text):
        """Fallback for unrecognized commands."""
        return "Command not recognized."

    def update_system(self):
        """Update system packages."""
        response = "Updating the system. You will be prompted."
        print(response)
        speak(response)
        try:
            # First, check for and remove faulty repositories
            subprocess.run(
                "sudo add-apt-repository --remove 'https://cli.github.com/packages'",
                shell=True,
                check=False  # Don't fail if it doesn't exist
            )
            
            # Perform the update
            process = subprocess.run(
                "sudo apt update -y",
                shell=True,
                check=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            print(process.stdout)
            speak("Update completed.")
        except subprocess.CalledProcessError as e:
            error_message = f"Error occurred during update: {e.stderr}"
            print(error_message)
            speak("An error occurred during the update.")

    def upgrade_system(self):
        """Upgrade system packages."""
        response = "Upgrading the system. You will be prompted."
        print(response)
        speak(response)
        try:
            process = subprocess.run(
                "sudo apt upgrade -y",
                shell=True,
                check=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            print(process.stdout)
            speak("Upgrade completed.")
        except subprocess.CalledProcessError as e:
            error_message = f"Error occurred during upgrade: {e.stderr}"
            print(error_message)
            speak("An error occurred during the upgrade.")

    def autoremove_system(self):
        """Remove unnecessary packages."""
        response = "Cleaning the system. You will be prompted."
        print(response)
        speak(response)
        try:
            process = subprocess.run(
                "sudo apt autoremove -y",
                shell=True,
                check=True,
                text=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            print(process.stdout)
            speak("Cleanup completed.")
        except subprocess.CalledProcessError as e:
            error_message = f"Error occurred during cleanup: {e.stderr}"
            print(error_message)
            speak("An error occurred during the cleanup.")

    def run(self):
        """Main loop for continuous voice interaction."""
        while True:
            command = self.recognize_speech()
            self.process_command(command)

# Initialize the assistant and run it in a separate thread
assistant = VoiceAssistant()

# Multithreading to handle voice interaction without blocking
def run_voice_assistant():
    assistant.run()

# Create a thread for the assistant
assistant_thread = threading.Thread(target=run_voice_assistant)
assistant_thread.start()

