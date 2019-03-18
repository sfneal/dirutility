import os
from databasetools import JSON
from dirutility import FTP


CONFIG_PATH = os.path.join(os.path.dirname(__file__), 'config.json')


def read_config(config_path):
    """
    Read/create a configuration file and prompt the user for values.

    :param config_path: Path to configuration file
    :return config: FTP configurations dictionary
    """
    # Create config file if it doesn't exist and return its values
    if not os.path.exists(config_path):
        print('Creating a FTP connection config file\nInput FTP configuration values...')
        config = {
            'connections': [
                {
                    'host': input('{0:10}: '.format('Host')),
                    'username': input('{0:10}: '.format('Username')),
                    'password': input('{0:10}: '.format('Password')),
                    'port': input('{0:10}: '.format('Port (hit enter to use port 21)')),
                }
            ]
        }

        # Set port to default of 21
        if len(config['connections'][0]['port']) < 1:
            config['connections'][0]['port'] = 21
        else:
            config['connections'][0]['port'] = int(config['connections'][0]['port'])

        JSON(config_path).write(config)
        return config

    # Read config.json
    else:
        print('Reading a FTP connection config file')
        return JSON(config_path).read()


def test_ftp_connection(config_path=CONFIG_PATH):
    """
    Read the FTP Connector configuration file.

    Create a configuration file and prompt the user for values if it doesn't exist.

    :param config_path: Path to configuration file
    :return: FTP parameters
    """
    print('FTP Connections Tester\n'.capitalize())

    # Retrieve FTP connection config
    config = read_config(config_path)

    print('\nTesting FTP connections')
    for connection in config['connections']:
        with FTP(**connection) as ftp:
            print('\tFTP connection success!')
            print('\t{0}'.format(ftp.session.getwelcome()))
            print('\n'.join('\t\t{0:10}: {1}'.format(k, v) for k, v in connection.items()) + '\n')


def main():
    test_ftp_connection()


if __name__ == '__main__':
    main()
