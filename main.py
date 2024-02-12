import os


class Parser(object):

    def __init__(self, file_path):
        with open(file_path, 'r') as f:
            self.raw_data = f.read()
        self.data = self._parse_data()

    def _parse_data(self):
        # Initialize parsed data as empty dictionary.
        data = {}

        # Split raw data by new line.
        lines = self.raw_data.split('\n')

        # 1. The first line contains the network element name.
        first_line = lines[0]
        data['network_element_name'] = first_line.split()[1]

        # 2. The status of the command is on the fourth line.
        fourth_line = lines[3]
        # We ignore 'RETCODE = ...' from the beginning of the line, since the
        # status of the command is prefixed by this.
        status_command = fourth_line.split()[3:]
        data['status_command'] = ' '.join(status_command)

        # 3. From line 10 until line with 'Number of results' we have the
        # table with the static parameters.
        data['static_parameters'] = {
            'Local Cell ID': [],
            'Cell Name': [],
            'Column_2': [],
            'Column_3': [],
        }
        for line in lines[9:]:
            if 'Number of results' in line:
                # We reached the end of the table. Break the loop.
                break
            line_data = line.split()
            data['static_parameters']['Local Cell ID'].append(line_data[0])
            data['static_parameters']['Cell Name'].append(line_data[1])
            data['static_parameters']['Column_2'].append(line_data[2])
            data['static_parameters']['Column_3'].append(line_data[3])

        # Return the parsed data.
        return data

    def get_network_element_name(self):
        return self.data.get('network_element_name')

    def get_status_command(self):
        return self.data.get('status_command')

    def get_static_parameters(self, column_name):
        return self.data.get('static_parameters').get(column_name)


if __name__ == '__main__':
    data_file_path = os.path.join(
        os.path.dirname(__file__), 'network_element_data.txt')
    p = Parser(data_file_path)

    # Print the network element name.
    network_element_name = p.get_network_element_name()
    print(f"Network element name: {network_element_name}")

    # Print the status command.
    status_command = p.get_status_command()
    print(f"Status command: {status_command}")

    # Print the static parameters by column name.
    column_name = input("Enter column name: ")
    column_values = p.get_static_parameters(column_name)
    print(f"Column values: {column_values}")
