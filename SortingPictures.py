import exifread
# Open image file for reading (must be in binary mode)

import exifread as ef
import requests
import os
def _convert_to_degress(value):
    """
    Helper function to convert the GPS coordinates stored in the EXIF to degress in float format
    :param value:
    :type value: exifread.utils.Ratio
    :rtype: float
    """
    d = float(value.values[0].num) / float(value.values[0].den)
    m = float(value.values[1].num) / float(value.values[1].den)
    s = float(value.values[2].num) / float(value.values[2].den)

    return d + (m / 60.0) + (s / 3600.0)

"""
def getGPS(filepath):
    '''
    returns gps data if present other wise returns empty dictionary
    '''
    with open(filepath, 'rb') as f:
        tags = ef.process_file(f)
        latitude = tags.get('GPS GPSLatitude')
        latitude_ref = tags.get('GPS GPSLatitudeRef')
        longitude = tags.get('GPS GPSLongitude')
        longitude_ref = tags.get('GPS GPSLongitudeRef')
        if latitude:
            lat_value = _convert_to_degress(latitude)
            if latitude_ref.values == 'S':
                lat_value = -lat_value
        else:
            return [None, None]
        if longitude:
            lon_value = _convert_to_degress(longitude)
            if longitude_ref.values == 'W':
                lon_value = -lon_value
        else:
            return [None, None]
        return [lat_value, lon_value]

"""

#file_path = "path_for_image/IMG_1644.JPG"
#gps = getGPS(file_path)
#print(gps) #{lat,long}

def getCity(coordinateList):
    if coordinateList[0] == None or coordinateList[1] == None:
        return None
    lat = coordinateList[0]
    long = coordinateList[1]
    res = requests.get("https://maps.googleapis.com/maps/api/geocode/json?latlng=" + str(lat) + "," + str(long) + "&key=AIzaSyCYD-Z5sZM0rAmLt5mcSqcc9WHOqXSS188")
    city = res.json()['plus_code']['compound_code'].split(' ',1)[1]
    #return city
    noSpacesCity = ""
    for part in city.split(" "):
        noSpacesCity = noSpacesCity + part
    return noSpacesCity

#print(getCity(getGPS(file_path)))

def getMonthYearCity(filepath):
    with open(filepath, 'rb') as f:
        #Getting Month, Year
        tags = ef.process_file(f)
        date = tags.get('EXIF DateTimeOriginal')
        #Getting Lat, Long
        latitude = tags.get('GPS GPSLatitude')
        latitude_ref = tags.get('GPS GPSLatitudeRef')
        longitude = tags.get('GPS GPSLongitude')
        longitude_ref = tags.get('GPS GPSLongitudeRef')
        if latitude:
            lat_value = _convert_to_degress(latitude)
            if latitude_ref.values == 'S':
                lat_value = -lat_value
        else:
            lat_value = None
        if longitude:
            lon_value = _convert_to_degress(longitude)
            if longitude_ref.values == 'W':
                lon_value = -lon_value
        else:
            lon_value = None
        city = getCity([lat_value, lon_value])
    if not date:
        return [None, None, city]
    return [date.values[5:7], date.values[0:4], city]

#print(">>>>>>>>>")
#print(getMonthYearCity(file_path))

"""
def getMonth(filepath):
    with open(filepath, 'rb') as f:
        tags = ef.process_file(f)
        date = tags.get('EXIF DateTimeOriginal')
    return date.values[5:7]
print(getMonth(file_path))
"""
"""
def listAllPhotos(directory):
    dir = str(directory)
    for filename in os.listdir(dir):
        if filename.endswith(".JPG") or filename.endswith(".png"):
            print(os.path.join(dir, filename))
"""
#exampleDirectory = "path_for_directory"
#print(listAllPhotos(exampleDirectory))

def createDirectory(rootDirectory,listSubdirectories):
    path = rootDirectory
    for dir in listSubdirectories:
        path = path + "/" + dir
    try:
        os.makedirs(path)
    except OSError:
        print ("Creation of the directory %s failed" % path)


def extractPhotos(dir, outputDirectory):
    for filename in os.listdir(dir):
        suffix = filename.lower().split(".")[-1]
        if suffix in ['jpg', 'png', 'jpeg', 'gif']:
            img_path = os.path.join(dir, filename)
            year = getMonthYearCity(img_path)[1]
            city = getMonthYearCity(img_path)[2]
            if city == None:
                city = 'No Location Found'
            if year == None:
                year = 'No Date Found'
            #print(">>>>>>")
            #print(img_path)
            #print(outputDirectory + "/" + year + "/" + city + "/" + img_path.split("/")[-1])
            try:
                os.rename(img_path, outputDirectory + "/" + year + "/" + city + "/" + img_path.split("/")[-1])
            except FileNotFoundError:
                createDirectory(outputDirectory, [year, city])
                os.rename(img_path, outputDirectory + "/" + year + "/" + city + "/" + img_path.split("/")[-1])

#FINAL COMMAND
#extractPhotos("path of folder of photos","path of sorted pictures directory")

#https://stackabuse.com/creating-and-deleting-directories-with-python/
#https://stackabuse.com/how-to-create-move-and-delete-files-in-python/
