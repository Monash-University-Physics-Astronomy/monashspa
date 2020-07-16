import os
import h5py
from monashspa.common.download_gdrive import download_file_from_google_drive

def getframe(fname):
    """
    Get a dataframe from an HDF5 file. If the file is not already available in the local directory,
    then download it from Google Drive.

    Example: getframe('data.h5')
    """
    files = {'data.h5':'1c8FPxYIdRNY8WmB8G4k7p_DSNrWwaFZU',
             'data-uppersideband.h5':'1_iVJIcjVgTgWEQZQGtsfSXwpPtIRZWAR',
             'simulation.h5':'1A5KVeiSdF0WlvfpbQpgkKT7SvUwA6RBQ'}


    if not os.path.isfile(fname):
        print('{f} not available locally. Downloading might take a while.'.format(f=fname))
        download_file_from_google_drive(files[fname], fname)

    hdf5file = h5py.File(fname, "r")
    return hdf5file['events']
