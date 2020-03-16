# My Little Doctor
Our Python-based healthcare assistant. 

### Setting up the Pi
1. Install `git`,`python3` and `python3-pip`:

  ```bash
  sudo apt-get update
  sudo apt-get upgrade
  sudo apt-get install git python3 python3-pip
  ```

2. Clone this repository:

  ```bash
  git clone https://github.com/RPi-Team-Mango/my-little-doctor/ MyLittleDoctor
  cd MyLittleDoctor
  ```
3. Connect the DS18B20 temperature sensor. We used the included one from the CamJam edukit - the guide can be found here:
https://github.com/CamJam-EduKit/EduKit2/blob/master/CamJam%20Edukit%202%20-%20RPi.GPIO/CamJam%20EduKit%202%20-%20Sensors%20Worksheet%203%20(RPi.GPIO)%20-%20Temperature.pdf

4. Install any required Python modules from `requirements.txt`. You should have most of the modules pre-installed, but run it on Tkinter just in case:

  ```bash
  sudo python3 -m pip install -r requirements.txt
  ```
5. (Optional) Set up the Pi's display:
We used the official Raspberry Pi 7" touchscreen display on our Pi specifically, and followed the following guide to set it up. However, My Little Doctor can work on any display. 
https://www.instructables.com/id/Raspberry-Pi-Touchscreen-Setup/
  
### Setting up Software
1. Ensure you run all the checks on the temperature sensor to make sure it is working. 
These can be found at the above-mentioned CamJam EduKit worksheet.

2. Setting up mailto links

A core part of My Little Doctor's functionality is the ability to send emails. In order to ensure this works appropriately, go to Chromium on the Pi. Click Settings > Privacy and Security > Site Settings and turn Handlers to on. 
Then, log into a Gmail account - a prompt should now ask you if you wish to allow Gmail to open all email links - allow this.

3. Run `gui.py` using Python, making sure you're in the correct directory to do so. 

  ```bash
  python gui.py
  ```
4. Enjoy!

## Guide Author

Anahitha Vijay ([lightspeedana](https://www.github.com/lightspeedana))
