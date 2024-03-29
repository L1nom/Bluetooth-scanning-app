import threading
import customtkinter
import asyncio
from bleak import BleakScanner
import requests
import json
from location import trilateration
import os
import sys

# Define our constants

root = customtkinter.CTk()
root.geometry("600x350")

destroy = False

beacons_list = [[]]

# 'DB:97:95:82:E4:90'
# 'C9:1C:20:01:05:6B'
# 'E8:CF:FE:45:29:C5'
# 'FD:78:D4:74:16:EF'
test = sys.argv[1]
splits = test.split('?')
if splits[1]:
    token = splits[1]
    token = token.split('=')[1]
if splits[2]:
    course_id = splits[2]
    course_id = course_id.split('=')[1]
if splits[3]:
    student_id = splits[3]
    student_id = student_id.split('=')[1]
if splits[4]:
    session_id = splits[4]
    session_id = session_id.split('=')[1].strip(',')


def join_session():
    url = "https://capstonebackendapi.fly.dev/join/session"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': token
    }

    payload = json.dumps({
                "course_id": course_id,
                "student_id ": student_id
            })

    response = requests.post(url, headers=headers, data=payload)


async def scanning_task():
    url = "https://capstonebackendapi.fly.dev/set/student_position"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': token
    }

    while True:

        scanning_message.pack()
        progress_bar.pack(pady=12, padx=10)
        progress_bar.start()
        progress_bar.step()

        if not check_active_session:
            os._quit(1)

        E8 = await BleakScanner.find_device_by_address('E8:CF:FE:45:29:C5', timeout=5)
        DB = await BleakScanner.find_device_by_address('DB:97:95:82:E4:90', timeout=5)
        FD = await BleakScanner.find_device_by_address('FD:78:D4:74:16:EF', timeout=5)
        C9 = await BleakScanner.find_device_by_address('C9:1C:20:01:05:6B', timeout=5)

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

        if C9 and DB and E8 and FD:
            try:
                # rssi_list = [C9.rssi, DB.rssi, E8.rssi, FD.rssi]
                # print(rssi_list)
                # beacon_location_list=[(0,0),(0,6.1), (6.1,0),(6.1, 6.1)]
                # location_x, location_y = trilateration(beacon_location_list, rssi_list)
                beacon_location_list=[(1.524,3.3),(6.24,3.3), (6.24, 6.756),(1.524, 6.756)]
                rssi_list = [-60, -73, -73, -75]
                
                # rssi_list = [-74, -68, -67, -78]
                location_x, location_y = trilateration(beacon_location_list, rssi_list)
                print(location_x, location_y)
            except:
                pass
            # location_x, location_y = 300, 400
            payload = json.dumps({
                "course_id": course_id,
                "x_position": location_x,
                "y_position": location_y
            })
            # location_x += 100
            # location_y += 100
            response = requests.post(url, headers=headers, data=payload)

            if response.status_code == 200:
                print('Position Updated')
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


def check_active_session():
    url = "https://capstonebackendapi.fly.dev/get/session/{}".format(str(session_id))
    headers = {
        'Content-Type': 'application/json',
        'Authorization': token
    }
    response = requests.get(url, headers=headers)
    response_dictionary = json.loads(response.text)
    active = response_dictionary['session']['active']
    return active


def on_raise_hand():
    url = "https://capstonebackendapi.fly.dev/raise_hand"
    headers = {
        'Content-Type': 'application/json',
        'Authorization': token
    }
    active = check_active_session()
    if active:        
        payload = json.dumps({
            "course_id": course_id,
            "student_id": student_id,
            "hand_raised": True
        })

        response = requests.put(url, headers=headers, data=payload)

        if response.status_code == 200:
            print('Hand Raised')
        else:
            print('Error Raising Hand')


    else:
        raise_button.destroy()
        error_message = customtkinter.CTkLabel(master=root, text="Class is over...")
        error_message.pack()
        
        payload = json.dumps({
            "course_id": course_id,
            "student_id": student_id,
            "hand_raised": False
        })

        response = requests.put(url, headers=headers, data=payload)
        error_message.after(5000, on_closing)
        

        
def on_closing():
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
join_session()
root.mainloop()

