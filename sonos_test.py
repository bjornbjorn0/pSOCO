def initialize_soco():
    import soco
    

def initialize_speaker(device):
    device.unjoin()

def check_device_availability(name):
    from soco.discovery import by_name
    print('Attempt to find device '+name)
    device = by_name(name)
    print(device)
    return device

# select sonos device. Return 'None' if device is not available    
def select_device(nr):
    # add here all numbers that refer to a sonos device
    if nr == '1':
        name = 'Kitchen'
        device = check_device_availability(name)
    elif nr == '2':
        name = 'Family Room'
        device = check_device_availability(name)

    else:
        device = 'None'

    if device != 'None':
         print('Device found: ' + device.player_name + ' with coordinator: ' + device.group.coordinator.player_name)
        
    else:        
        print(device)
        print('No device found')
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
    mykey = input('key:')

    if mykey=='w':
        device.volume=+10
    elif mykey =='x':
        device.volume=-10

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
    if nr == '11':
        print('Play studio brussel')
        coordinator.play_uri('http://icecast.vrtcdn.be/stubru-high.mp3')
    elif nr == 'p':
        coordinator.pause()
    elif nr=='w':
        group_volume(coordinator, +10)
    elif nr =='x':
        group_volume(coordinator, -10)
    
# start the code
initialize_soco()
coordinator = []


while True:
    nr = input('Action #? ')
    selected_device, coordinator = device_actions(nr, coordinator)

    group_actions(nr, coordinator)