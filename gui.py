import threading
import asyncio
import tkinter as tk
import customtkinter
import asyncio
from bleak import BleakScanner
import requests
import json
import threading
from location import trilateration
import threading
import os

# Define our constants

root = customtkinter.CTk()
root.geometry("600x350")

destroy = False

# test = sys.argv[1]
test = "zlocatify:?token=\"aqqweqweqwwe\"?course_id=\"qweqeqwqwe\"?session_id=\"qweqeqwqwe\"?student_id=\"qweqeqwqwe\""
splits = test.split('?')
if splits[1]:
    token = splits[1]
    token = token.split('=')[1]
if splits[2]:
    course_id = splits[2]
    course_id = course_id.split('=')[1]
if splits[3]:
    session_id = splits[3]
    session_id = session_id.split('=')[1]
if splits[3]:
    student_id = splits[3]
    student_id = student_id.split('=')[1]
print(token, course_id, session_id, student_id)


def join_session():
    url = "https://capstonebackend.fly.dev/join/session"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': token
    }

    payload = json.dumps({
                "course_id": course_id,
                "student_id ": student_id
            })
    
    requests.post(url, headers=headers, data=payload)


async def scanning_task():
    url = "https://capstonebackend.fly.dev/set/student_position"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': token
    }

    while True:

        scanning_message.pack()
        progress_bar.pack(pady=12, padx=10)
        progress_bar.start()
        progress_bar.step()

        devices = await BleakScanner.discover(timeout=10.0)
        device_list = []
        for d in devices:
            device_list.append([d.address, d.rssi])
        print("Done")

        await asyncio.sleep(1)

        if destroy:
            try:
                os._exit(1)

            except Exception:
                os._exit(1)
                
        scanning_message.forget()
        scanning_success.pack()
        scanning_success.after(3000, scanning_success.forget)
        progress_bar.stop()
        progress_bar.forget()

        if device_list:
            # location_x, location_y = trilateration(beacon_location_list, rssi_list)
            location_x, location_y = 300, 400
            payload = json.dumps({
                "course_id": course_id,
                "x_position": location_x,
                "y_position": location_y
            })
            location_x += 100
            location_y += 100
            response = requests.post(url, headers=headers, data=payload)

            if response.status_code == 200:
                print('pushed')
            if response.status_code != 200:
                error_message.pack()
                error_message.after(3000, error_message.forget)

        # Wait for 1 minute before running again
        await asyncio.sleep(10)


def start_scanning_task():
    # Start the event loop in a new thread
    global loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.create_task(scanning_task())
    try:
        loop.run_forever()
    finally:
        try:
            
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.close()
            root.destroy()
            os._exit(1)

        except Exception:
            os._exit(1)


def on_raise_hand():
    print("Hello")
    url = "https://capstonebackend.fly.dev/raise_hand"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': token
    }

    payload = json.dumps({
        "course_id": course_id,
        "student_id": student_id,
        "hand_raised": True
    })

    response = requests.put(url, headers=headers, data=payload)
    print(response.status_code)



def on_closing():
    global destroy
    root.destroy()
    loop.stop()
    os._exit(1)

root.protocol("WM_DELETE_WINDOW", on_closing)


# Create a Tkinter UI elements
label = customtkinter.CTkLabel(master=root, text="Smart LMS", font=("Roboto", 24))
label.pack(pady=12, padx=10)

raise_button = customtkinter.CTkButton(root, text="Raise", command=on_raise_hand)
raise_button.pack()

scanning_message = customtkinter.CTkLabel(master=root, text="Scanning...")
scanning_success = customtkinter.CTkLabel(master=root, text="Finished scanning!")
error_message = customtkinter.CTkLabel(master=root,
                                       text="Scan error! Position not found. \n Please check Bluetooth, Internet, "
                                            "and an active class are available")

progress_bar = customtkinter.CTkProgressBar(root, orientation='horizontal', mode='indeterminate')


# Start the background task in a new thread
thread = threading.Thread(target=start_scanning_task)
thread.start()

# Start the Tkinter event loop on the main thread
root.mainloop()
