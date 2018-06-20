def initialize_soco():
    import soco
    import os

def initialize_speaker(device):
    device.unjoin()

def check_device_availability(name):
    from soco.discovery import by_name
    print('Attempt to find device '+name)
    device = by_name(name)    
    return device

# select sonos device. Return 'None' if device is not available    
def select_device(nr):
    # add here all numbers that refer to a sonos device
    print('Looking for command '+nr)
    if nr == '1':
        name = 'Kitchen'
        device = check_device_availability(name)
        device.volume = 20
    elif nr == '2':
        name = 'Family Room'
        device = check_device_availability(name)
        device.volume = 20

    else:
        device = 'None'

    print(device)

    if device != 'None':
         print('Device found: ' + device.player_name + ' with coordinator: ' + device.group.coordinator.player_name)
        
    else:        
        print('Device selected by last key?: ' + device)
        print('Key does not select a device.')
    return device

def organize_device(selected_device, coordinator):

    isNew = 0
    if isinstance(coordinator, list):
        isNew = 1

    if selected_device !='None':

        # is speaker part of current group?        
        if selected_device.group.coordinator != coordinator: # there is a coordinator
            
            # unjoin device from current coordinator
            selected_device.unjoin()

            # is there a group already?
            if isinstance(coordinator,list): # NO, device is set to master of the group
                coordinator = selected_device # soco automatically set current device to coordinator so we only need to remember it for ourselves
            else: # YES, device is added to the group
                selected_device.join(coordinator)
            print("Coordinator of selected device set to: " + selected_device.group.coordinator.player_name)

    return selected_device, coordinator, isNew

def change_settings(device, subset):
    print('Device is already connected to group, please select action for this device.')
    

    while 1:
        mykey = input('Volume up/down [w/x], cancel [enter], unjoin [u]:')
        if mykey=='w':
            device.volume=device.volume+10
        elif mykey =='x':
            device.volume=device.volume-10
        elif mykey =='u':
            device.unjoin()
        else:
            break

# is speaker active?
def device_actions(nr, coordinator):
    
    # Is speaker available?
    selected_device = select_device(nr)    

    if selected_device != 'None':
        # organize speaker in current setup
        selected_device, coordinator, isNew = organize_device(selected_device, coordinator)

        # change device settings with keyboard
        if isNew != 1: # only when device was already coupled to zone earlier
            change_settings(selected_device, 'device')

    print(coordinator)
    return select_device, coordinator        
        
def group_volume(device, volumechange):
    for player in device.group:
        player.volume = player.volume+volumechange
        print(player.player_name + ' volume: ' + str(player.volume))

def group_actions(nr, coordinator):
    # print(coordinator)        
    if nr == 'a':         
        coordinator  = select_device('2')
        select_device('1')
        print('Play studio brussel')
        coordinator.play_uri('http://icecast.vrtcdn.be/stubru-high.mp3')
    elif nr == 'p':
        coordinator.pause()
    elif nr == ' ':
        coordinator.play()
    elif nr=='w':
        group_volume(coordinator, +5)
    elif nr =='x':
        group_volume(coordinator, -5)
    
    return coordinator

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
 
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

import sys, termios, tty, os, time

# code for continuously checking of keyboard
# while True:
#     char = getch()
 
#     if (char == "p"):
#         print("Stop!")
#         exit(0) 
button_delay = 0.2
# start the code
initialize_soco()
coordinator = []

import sys
from getkey import getkey, keys

print('You can start using it!')
while True:
    if sys.platform=='darwin':
        nr = input('Action #? ')
    else:
        while 1:
            key = getkey()
            print(key)
            if key == keys.N1:
                nr = 'a'
                print('Play VRT Studio brussel in the kitchen')
                break         
            if key == keys.CTRL_AT: 
                nr = 'p'
                print('Pause playing') 
                break
            if key == keys.AGE_UP:
                nr = 'w'
                print('Increase volume')
                break
            if key == keys.AGE_DOWN:
                nr = 'x'
                print('Decrease volumn')
                break

            print(keys.name(key))
            

    print('uit de loop')
    if type(nr)==int:
        nr = str(nr)

    selected_device, coordinator = device_actions(nr, coordinator)

    coordinator = group_actions(nr, coordinator)