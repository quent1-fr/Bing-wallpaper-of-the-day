# -*- coding: utf-8 -*-
# Import all needed stuff
import urllib, sys, xml.dom.minidom, os, pynotify, time

# [Configuration] You can change these values
country_code = 'fr-FR' # Your country code
screen_resolution = '1366x768' # Your screen resolution
show_notification = True # Do you want a notification when the wallpaper changes?
time_to_wait = 15 # Time (in minutes) between two refreshes

# [Configuration] You mustn't change this value
script_directory = os.path.dirname(os.path.abspath(__file__))

while True:
    # Date of the day, YYYYMMDD
    today = time.strftime('%Y%m%d')
    
    try:
        # Getting the expiration date
        actual_end_date_file = open(script_directory + '/data/end_date','r')
        actual_end_date = actual_end_date_file.readline()
        actual_end_date_file.close()
        
        # If the wallpaper has expired
        if today > actual_end_date:   
            refresh = True
        
        # Otherwise
        else:
            refresh = False
            
    except:
        # If data/end_date don't exists, we refresh the wallpaper
        refresh = True
        
    if refresh:
        # Fetching the wallpaper of the day
        print('Reading the API...')
        address = 'https://www.bing.com/HPImageArchive.aspx?format=xml&idx=0&n=1&mkt=' + country_code
        image = xml.dom.minidom.parse(urllib.urlopen(address)).getElementsByTagName('image')[0]
        
        # This is the absolute url of the wallpaper
        url = 'https://www.bing.com' + image.getElementsByTagName('urlBase')[0].firstChild.data + '_' + screen_resolution + '.jpg'
            
        # This is the description of the wallpaper
        description = image.getElementsByTagName('copyright')[0].firstChild.data
            
        # This is the end date for the wallpaper
        end_date = image.getElementsByTagName('enddate')[0].firstChild.data
           
        # Saving the end date
        new_end_date_file = open(script_directory + '/data/end_date','w+')
        new_end_date_file.write(end_date)
        new_end_date_file.close()
        
        # Saving the wallpaper to data/bing_wallpaper.jpg
        print('Downloading...')
        urllib.urlretrieve(url, script_directory + '/data/bing_wallpaper.jpg')
            
        # Applying the new wallpaper
        print('Applying...')
        os.system('DISPLAY=:0 GSETTINGS_BACKEND=dconf gsettings set org.gnome.desktop.background picture-uri "file://' + script_directory + '/data/bing_wallpaper.jpg"')
        
        # Shows a notification to the user (if the user wants it)
        if show_notification:
            pynotify.init('Bing WOTD')
            n = pynotify.Notification('A new wallpaper has been applied', description, script_directory + '/data/bing_logo.png')
            n.show()
    
    else:
        print('The wallpaper is already up-to-date!')
        
    print('\nWaiting for ' + str(time_to_wait) + ' minutes...\n')
    time.sleep(time_to_wait * 60)
