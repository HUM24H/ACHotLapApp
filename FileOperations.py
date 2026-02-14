import os

def SetSepValue(sRootInstall):
    # Assign correct path separator value
    if "/" in sRootInstall:
        # Linux/Unix Path
        sReturn = "/"
    elif "\\" in sRootInstall:
        # Windows/NT Path
        sReturn = "\\"
    else:
        # Invalid Path
        sReturn = " "

    # Return Separator value
    return sReturn

def CheckACPath(sRootInstall):
    #Set initial return boolean
    bFound = False

    # Get Path Separator Value
    sSepString = SetSepValue(sRootInstall)

    # Set AC Install Binary Path
    sACBinary = sRootInstall + sSepString + "AssettoCorsa.exe"

    # Check if the file exists
    if os.path.isfile(sACBinary):
        bFound = True
    
    # Return whether AC Binary exists
    return bFound

def GetNameFromJson(sFullDir, sType):
    # Init Return Variable
    sReturn = ''

    # Get Path Separator Value
    sSepString = SetSepValue(sFullDir)

    # Set ui_car.json File
    sJsonFile = sFullDir + sSepString + "ui_" + sType + ".json"

    if os.path.exists(sJsonFile):
        with open(sJsonFile, encoding = "ISO-8859-1") as oJsonFile:
            # Note:
            # File is JSON but not using JSON parser due to technical issue
            # Reason:
            # Some JSON files in Assetto Corsa are technically invalid JSON files
            # This causes Python JSON parser to crash, so parsing as plain text file
            data = oJsonFile.read().replace('\n', '')
            
            # Getting position points to extract just JSON tag "name" value
            # Cannot use JSON parser as explained above
            iPosEnd = data.index(',')
            iPosStart = data[:iPosEnd - 1].index(':')

            # Assign JSON tag value to return variable
            sReturn = data[iPosStart + 3:iPosEnd - 1]

    # Return JSON tag value
    return sReturn

def ProcessCarDirList(sRootInstall):
    # Init Car Names List
    aCarNames = []

    # Get Path Separator Value
    sSepString = SetSepValue(sRootInstall)

    # Setup Car Content Path
    sCarDirPath = sRootInstall + sSepString + "content" + sSepString + "cars"

    for aRoot, aDirs, aFiles in os.walk(sCarDirPath):
        for sCarDir in aDirs:
            # Assign full path to Car Directory
            sFullCarDir = sCarDirPath + sSepString + sCarDir + sSepString + "ui"

            # Fetch Car Name from ui_car.json in Car Directory
            sValue = GetNameFromJson(sFullCarDir, "car")

            # Only assign value to Car Name List if there is data
            if sValue != "":
                aCarNames.append(sValue)
                aCarNames.append(sCarDir)
        
        # Break after initial iteration
        # We only care for initial directories in the root directory, not sub-directories
        break

    # Return Car Name List for usage later
    return aCarNames

def ProcessTrackDirList(sRootInstall):
    # Init Track Names List
    aTrackNames = []

    # Get Path Separator Value
    sSepString = SetSepValue(sRootInstall)

    # Setup Car Content Path
    sTrackDirPath = sRootInstall + sSepString + "content" + sSepString + "tracks"

    # Loop initial tracks directory
    for aRoot, aDirs, aFiles in os.walk(sTrackDirPath):
        
        # Loop through each track directory within the Content Tracks directory
        for sTrackDir in aDirs:
            aTrackNames.append("#" + sTrackDir)

            sUIDir = sTrackDirPath + sSepString + sTrackDir + sSepString + "ui"

            # Loop through each Directory and File in the tracks ui directory
            for aUIRoot, aUIDirs, aUIFiles in os.walk(sUIDir):

                # Fetch the Track Name for each track variant directory
                for sTrackUIDir in aUIDirs:
                    sFullDir = sUIDir + sSepString + sTrackUIDir
                    aTrackNames.append(GetNameFromJson(sFullDir, "track"))
                    aTrackNames.append(sTrackUIDir)
                
                # Fetch the Track Name for the main track
                # Only do this if a ui_track.json exists in the root track ui directory
                for sTrackUIFiles in aUIFiles:
                    if sTrackUIFiles == "ui_track.json":
                        aTrackNames.append(GetNameFromJson(sUIDir, "track"))
                        aTrackNames.append(sTrackDir)
                
                # Break after initial iteration
                break
        # Break after initial iteration
        break
    
    return aTrackNames

