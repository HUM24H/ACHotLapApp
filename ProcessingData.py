import FileOperations

# Fetch AC Car List
def processCarList(sRootInstall):
    # Fetch Car Directory List
    aCarList = FileOperations.ProcessCarDirList(sRootInstall)

    return aCarList

# Fetch AC Track List
def processTrackList(sRootInstall):
    # Fetch Track Directory List
    aTrackList = FileOperations.ProcessTrackDirList(sRootInstall)

    return aTrackList
