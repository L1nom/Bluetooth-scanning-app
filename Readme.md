
# Smart Localization with Bluetooth 

This project uses Bluetooth signals as a way to measure a user's position within a fixed space or environment. 

We use Bluetooth scanning with Python and Confidex Viking Bluetooth beacons to act as anchors to receive signal strenghts from. 


## Python Code:

This code was written using Python version 3.11. The main library utilized is the [Bleak scanner](https://pypi.org/project/bleak/). 

We use the scanner to access basic Bluetooth functionality of a laptop, such as scan and filter by MAC address, or scan for all devices. 

* Please make sure to incorporate asynchronous programming when calling the Bleak scanner instance. The simple usage is provided in the documentation, and asynchronous call of the scanner will help unblock other code

The necessary libraries can be installed using the requirements.txt file. To create the all-in-one executable, use py-auto-to-gui library to convert the files into a single executable. 

* If using CustomTkinker for the python frontend, you will have to manually add this package as an additional file in py-auto-to-gui before compiling. Instruction can be found [here](https://customtkinter.tomschimansky.com/documentation/packaging)

## Bluetooth Beacons:

The spec sheet for the beacons can be found through here: 


To set up the beacons, use the Confidex Viking app provided through the Apple or Android App Store on a mobile device with NFC connection. Load the app, and import the default beacon profiles. With NFC enabled, you can turn on each beacon, read their default settings, and even change the configurations as well. A basic overview of how the setup process works can be found here: [Instructions](https://support.tracerplus.com/hc/en-us/articles/360050830053-How-to-Enable-and-Configure-Confidex-Viking-Beacons)


## App overview

1. The app continually scans for nearby Bluetooth devices, and reads their respective RSSI (Received Signal Strength Indicators) values in dB. This value is a negative integer, the lower it is the nearer the device is to the beacon. 
2. We can mathematically convert the dB to meters (or other preferred unit)
3. Using trilateration, we can estimate the position of the user based on the distances from the user to static, known locations of beacons in a room. The approximation heavily relies on the acccuracy of the Bluetooth signals received and strength of the beacons itself
4. The room must be measured before hand. Strategically place the beacons and measure the X and Y locations and input them into the trilateration code. This will help output the user's location relative to the beacons. 
4. The app uses API routes to communicate student location data, which can then be mapped onto a frontend website. After calculating the location, we send this to our backend based on the student's id.

### Notes:
* Quality-of-life: we implemented automatic sign in by using a custom URL protocol scheme with the Windows registry. When the app is opened using our URL scheme, it will pass in a line of information to the app which is then parsed:
    * Token id
    * Student id
    * Course id
    * Session id
   We use these parameters within our request to identify the student. 

* We can instead use a normal log in method by asking the user to enter their user/pass. The custom URL scheme makes the app much more seamless to use, and is a one-time click from the user.

* Mapping of the room can be done by hand, or with the use of blueprints. 

* The raise-hand feature is one-way, the user does not know if has been acknowledged. A future improvement would be a two-way request so the user can see a pending request is made, or if the request has been satisfied






