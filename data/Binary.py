'''
Binary.py 
Example websocket connection for price data
Author: Dan Wallace
Date: 6/5/2021

-> Binary.py Example 
    1. This script contains two functions :: convert_to_binary(), unpack_binary_file().
        -> convert_to_binary()  :: Parses python dict(), where key's values are arrays, into a 1D binary file.
        -> convert_to_binary()  :: This can be used to optimize large data storage
        -> unpack_binary_file() :: Unpacks the saved binary file back into a usable python dict()
        -> unpack_binary_file() :: Fast method to retrieve large datasets quickly

    2. For the example we will uses Numpy to create arrays
        -> Type 'pip install numpy' in your terminal if you don't have it already

-> Struct Notes
    1. 'wb' overwrites binary file
    2. 'ab' appends to existing binary file
'''

# Imports
import struct
import numpy as np
import datetime as dt
###############################################################
# Saves python dict() to a binary file called :: binary_data
###############################################################
def convert_to_binary(data):

    # Print data passed into function
    print(str(dt.datetime.now())+' :: convert_to_binary()  :: Converting '+str(data)+ ' to 1D array.')

    # Blank array for iterations to append to
    arr = []

    # Loop through the data passed into the function and append to 'arr'
    # This will create a 1 dimensional array (all the data on the same line)
    [[arr.append(y) for y in data[x]] for x in data]

    # Insert the length of each dict() key so we can unpack the data later
    # This is needed because with the data flattend to one line, we need to know how to split it later
    arr.insert(0,len(data['key_1']))
    arr.insert(1,len(data['key_2']))

    # Print our 1 dimensional array
    print(str(dt.datetime.now())+' :: convert_to_binary()  :: 1D array :: '+str(arr)+'.')

    # Save it to binary by passing the 1 dimensional array into struct
    with open('binary_data', "wb") as f:
        f.write(struct.pack('f' * len(arr), *arr))
        f.close()

    # Print file save confirmation
    print(str(dt.datetime.now())+' :: convert_to_binary()  :: Saved to binary file.')

###############################################################
# Unpacks data from binary file into python dict()
###############################################################
def unpack_binary_file():
  
    # Open binary file and unpack to usable 1D array
    with open('binary_data', "rb") as file:
        f = file.read()
        data = list(struct.unpack('f' * int(len(f) / 4), f))

    # Print raw python list from unpacked binary array
    print(str(dt.datetime.now())+' :: unpack_binary_file() :: Raw array from binary :: '+str(data)+'.')

    # Use first two values of struct array to find split point for data
    # The length of each dataset is appended to the 1D array by convert_to_binary() before it saves to binary
    key_1_len, key_2_len = int(data.pop(0)), int(data.pop(0))

    # Split the 1D array into two arrays representing our original data
    key_1, key_2 = data[:key_1_len], data[key_2_len:]        

    # Append the split unpacked arrays to a new python dict()
    unpacked_dict = {'key_1':key_1,'key_2':key_2}

    # Print final python dict() created from unpacked binary data      
    print(str(dt.datetime.now())+' :: unpack_binary_file() :: Python dict from unpacked binary '+str(unpacked_dict)+'.') 
    
###############################################################
# Main
###############################################################

# Dictionary where each key holds an array
data = {
    'key_1':[np.random.randint(100),np.random.randint(100)],
    'key_2':[np.random.randint(100),np.random.randint(100)]
}

# Save data dict() to binary file
convert_to_binary(data)

# Unpack binary file to python dict
unpack_binary_file('binary_data')
