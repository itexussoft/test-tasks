# General description

The aim of this test is to be able to create a server able to decode binary files and populate a table with the retrieved information.
the result of this test should be a web service with:
  - an API able to retrieve binary files containing samples, and insert them in database, into a samples table.
  - an API able to send the content of the samples table as json data.

## decoding the binary file

The first step of this script is to code a buffer decoder. The binary data will be sent as a base64 buffer and will have the following format:

|File part   | Position | type (big endian)                        | Field                             | value
------------ | -------- | -----------------------------------------| --------------------------------- | -----
Header       | 0        | U8                                       | file_version                      | 0x00
Header       | [1:2]    | U16                                      | nb_entres                         | n
             |          |                                          |                                   |
Entry 0      | [3:6]    | U32                                      | capture_time (unix timestamp)     |
Entry 0      | [7:8]    | U16                                      | sensor_id                         |
Entry 0      | [9:10]   | U16                                      | light                             |
Entry 0      | [11:12]  | U16                                      | soil_moisture                     |
Entry 0      | [13:14]  | U16                                      | air_temperature                   |
             |          |                                          |                                   |
Entry 1      | [15:26]  |                                          | same fields as entry 0            |
------------ | -------- | ---------------------------------------- | --------------------------------- | -----
Entry (n-1)  |          |                                          | same fields as entry 0            |

### Exercise:
  1. Create a library allowing to decode a binary file of this kind.
  2. Implement the unit tests that you judge usefull to this decoding library.
  
provided material:
  - An example of sample list is provided in the file 4_example.csv
  - An example of binary file (encoded in base 64 is provided) in 3_example_input.json
  - The python script used to convert the csv into a binary file is provided in csv_to_binfile.py.
  
## Ruby on Rails web server decoding and storing samples

Given the file format previously used, implement in a web service an API which allow a client to send a binary buffer encoded in base64 and wrapped into a json object.
The web service should be able to decode this buffer and store the extracted lines in a table called 'samples'

Rules:
  - Two samples of a specific sensor can't have the same capture_time. If a buffer is received with a sample already present in the database, a warning should be logged and the raw ignored.
  - A sample can't have a capture_time in the future, a buffer containing samples in the future will be rejected.

### Exercise: 
Implement the API and the unit and integration tests you judge useful.

## API to retrieve samples from the web service

Add an API to retrieve samples from this web service in a json format. 
The parameters for this API will be:
  - sensor_id (mandatory)
  - start_time (optional) filter samples older than this datetime
  - end_time (optional)  filter samples more recent than this datetime

### Exercise: 
Implement the API and the unit and integration tests you judge useful.
