import requests
import xmltodict
from configparser import ConfigParser
import os.path


class Panorama(object):
    def __init__(self):
        self.config = None
        self._read_config()
        self._server_url = self.config.get('server_url')
        self._username = self.config.get('username')
        self._password = self.config.get('password')
        self.__setupApiKey()

    def _read_config(self):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        config_filepath = dir_path+"/config.ini"
        # check if the config file exists
        exists = os.path.exists(config_filepath)
        config = None
        if exists:
            config = ConfigParser()
            config.read(config_filepath)
            self.config = config['Palo']
        else:
            print("---------config.ini file not found at ", config_filepath)

    def __setupApiKey(self):
        print('Fetching the api key.')
        self._key = None
        data = {'type': 'keygen', 'user': self._username,
                'password': self._password}
        response = requests.post(self._server_url, data=data, verify=False)
        if response.ok:
            xml = response.text
            if 'Invalid username or password' in xml and '__LOGIN_PAGE_FOR_PANORAMA_BACKWARD_COMPATIBILITY__' in xml:
                print('Invalid URL')
                print(xml)
                raise ConnectionError('Invalid URL')
            response_dict = xmltodict.parse(xml)
            status = response_dict.get('response').get('@status')
            if status == 'success':
                self._key = response_dict.get('response').get('result').get(
                    'key')
            else:
                print('Failed to get api key: %s Status Code: %s' % (response.text, str(response.status_code)))
                raise ConnectionError(
                    'Failed to get api key: %s Status Code: %s' % (response.text, str(response.status_code)))
        else:
            print('Failed to get api key: %s' % response.text)
            raise ConnectionError('Failed to get api key: %s' % response.text)

    def print_key(self):
        print(self._key)
