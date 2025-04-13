#!/usr/bin/env python3
# sudo dnf5 install webkit2gtk4.0 python3-gobject

import gi
import os
import json
gi.require_version('Gtk', '3.0')
gi.require_version('WebKit2', '4.0')
from gi.repository import Gtk, WebKit2

# Set up the directory for storing cookies, cache, and last chat URL
data_dir = os.path.expanduser("~/.cache/chatgpt_webkit")
os.makedirs(data_dir, exist_ok=True)

# File to store the last opened chat URL
last_chat_file = os.path.join(data_dir, "last_chat.json")

# Load the last chat URL if it exists
if os.path.exists(last_chat_file):
    with open(last_chat_file, 'r') as f:
        last_chat_url = json.load(f).get("last_chat_url", "https://chat.openai.com/")
else:
    last_chat_url = "https://chat.openai.com/"  # Default URL if no chat was saved

# Set up WebKit WebContext
context = WebKit2.WebContext.get_default()

# Configure the Cookie Manager for persistent storage
cookie_manager = context.get_cookie_manager()
cookie_manager.set_persistent_storage(
    os.path.join(data_dir, "cookies.txt"),
    WebKit2.CookiePersistentStorage.TEXT
)

# Create the GTK window
window = Gtk.Window()
window.set_default_size(750, 450)
window.set_title("ChatGPT")

# Create the WebKit WebView with the context
webview = WebKit2.WebView.new_with_context(context)
webview.load_uri(last_chat_url)  # Load the last chat URL

# Function to save the current URL when the window is closed
def save_last_chat_url():
    current_url = webview.get_uri()
    with open(last_chat_file, 'w') as f:
        json.dump({"last_chat_url": current_url}, f)

# Signal handler for page loading
def on_load_changed(webview, load_event):
    if load_event == WebKit2.LoadEvent.FINISHED:
        print("Page loaded successfully.")
    elif load_event == WebKit2.LoadEvent.FAILED:
        print("Failed to load page.")

# Connect the load changed signal
webview.connect("load-changed", on_load_changed)

# Connect the signal to save the current URL on close
window.connect("destroy", lambda w: (save_last_chat_url(), Gtk.main_quit()))

# Add WebView to the window and display everything
window.add(webview)
window.show_all()

# Start the GTK main loop
Gtk.main()
