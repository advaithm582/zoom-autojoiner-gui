# Zoom Autojoiner

TL;DR A tool to join Zoom meetings quickly. Comes with a GUI. Prior configuration needed.

## Goals:
* To serve as a meeting notice board (see Todo)
* To remind that it is time to join a meeting
* To aid in typing long meeting IDs and passcodes

## Use Scenario:
You are working on an assignment, and you are so focused that you forget that your meeting is now. When you realise that you had the meeting, you open Whatsapp Web to get the passcode and ID. It takes 10 minutes to load, only to show you that it can't connect to the phone. Now you scramble about for your cell phone. You are furious as Fingerprint Unlock fails. Finally, you copy the Meeting ID to the Zoom interface, enter the passcode wrongly once, and join the meeting. Once you join, you realise that you have joined in your mother's account.

Now you found this. You just add your meeting in the intutive interface and BAM! When it is time, you will find your cursor automatically moving, and you will now remember about the meeting, and you can get ready while we do the clicking for you!

## What **not** to use this program for:
* Overloading Zoom Servers with Join Meeting requests
* Attending your classes/meetings on your behalf
* Other uses that do not fit in to the goals of this program

# User Manual
## Installation and Configuration
### Configuring constants in `config.json`

> **WARNING:** This portion of the user manual is outdated!!! 
> Also, with detailed comments in the config files (see below), this portion of the manual may be considered redundant.
> 
> * [Application Configuration Sample File](https://github.com/advaithm582/zoom-autojoiner-gui/blob/main/zoom_autojoiner_gui/config/application-default.ini)
> * [Extensions Configuration Sample File](https://github.com/advaithm582/zoom-autojoiner-gui/blob/main/zoom_autojoiner_gui/config/extensions-default.ini)

```
{
	"ICON_FILE" : "ZoomAJIcon.ico",
	"PYAG_PICS_DIR" : "",
	"DB_URL" : "sqlite:///database.db",
	"THEME_FILE" : "default_theme.thm.json",
	"MY_NAME" : "Lorem"
}
```
Key | Value
----|-------
ICON_FILE | The File used by Tcl/Tk to display the favicon. Do not change this unless you wish to change the favicon.
PYAG_PICS_DIR | This directory contains all `.png` files required for the Autojoiner to function. See below for instructions.
DB_URL | SQLAlchemy DB URI to be used. You can also connect to a common database server and then, Whoa! You have a network-wide Meeting Notice Board!
THEME_FILE | A simple theme file to change the appearance of the window. You can meddle around with the colors, fonts, etc.
MY_NAME | The name Autojoiner will change to when you join the meeting. Required.

### Adding the images to `PYAG_PICS_DIR`

First, pin Zoom to your taskbar. This will be how ZAJ opens Zoom. Then, take screenshots and name the files as below:

All images must be in .png format only.

File Name | Description of the screenshot | Example
----------|-------------------------------|--------
zoom_taskbar.png | A picture of Zoom in the taskbar. | 
join_btn.png | A picture of the blue Join button in the Zoom home screen. to the right of orange New Meeting. | 
name_box.png | A picture of your name in the Join meeting box. Below the Meeting ID prompt. | 
join_btn_after_mtg_id.png | The Join Meeting button in the Enter Passcode page. |


## Usage
Using the software is quite simple - just go to Menubar - Meetings - Add meeting. 

> Tip: You can also use shortcut key Ctrl+N.

Date must be in YYYY:MM:DD HH:MM:SS in 24-hour format (ISO standard)

Similarly you can edit your meeting too

# To be implemented (Todo)
* Support for clearing data in menubar
* Support for a common office notice board using a common database, including privilleges.
