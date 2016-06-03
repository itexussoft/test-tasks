import time, struct, base64, calendar, json

class History:
    def __init__(self, csv_file):
        self.history_csv = csv_file
        self.entries = []
        self.read_csv()

    def get_raw_buffer(self):
        raw_buffer = struct.pack('>BH', 0, len(self.entries))

        for entry in self.entries:
            try:
                raw_buffer += struct.pack('>IHHHH',
                    calendar.timegm(entry["capture_time"]),
                    entry["sensor_id"],
                    entry["light"],
                    entry["soil_moisture"],
                    entry["air_temperature"])
            except:
                print entry
                raise

        return raw_buffer

    def base64_buffer(self):
        return base64.encodestring( self.get_raw_buffer())


    def read_csv (self):
        with open(self.history_csv, 'r') as csv_file:
            self.entries = []
            titles = csv_file.readline().strip().split(",")

            lines  = csv_file.readlines()
            for line in lines:
                values = {}
                tmp = line.strip().split(',')
                for idx in range(len(tmp)):
                    values[titles[idx]] = tmp[idx]
                entry = {
                    'capture_time': time.strptime(values['capture_time'], "%Y-%m-%d %H:%M:%S %Z"),
                    'sensor_id': int(values['sensor_id']),
                    'light': int(values['light']),
                    'soil_moisture': int(values['soil_moisture']),
                    'air_temperature': int(values['air_temperature'])
                }
                self.entries.append(entry)

if __name__ == '__main__':
    history = History('example.csv')
    print history.base64_buffer()
    with open('example.raw', 'wb') as raw_file:
        raw_file.write( history.get_raw_buffer())

    with open('example_input.json', 'w') as json_file:
        json = json.dumps({
            'buffer': history.base64_buffer()
            },
            indent=4 )
        json_file.write( json)
