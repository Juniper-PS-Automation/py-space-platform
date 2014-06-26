import os

import requests
import logging
import yaml

class Space:
    """Encapsulates a Space REST endpoint"""

    def __init__(self, url, user, passwd):
        self.space_url = url
        self.space_user = user
        self.space_passwd = passwd
        self.logger = logging.getLogger('root')
        self.services = self._init_services()

    def _init_services(self):
        path = os.path.abspath(__file__)
        dir_path = os.path.dirname(path)
        with open(dir_path + '/services.yml') as f:
            services_dict = yaml.load(f)['services']

        services = {}
        from jnpr.space.platform.core import service
        for key, value in services_dict.iteritems():
            services[key] = service.Service(self, key, value)

        return services

    def _get_class_def(self, class_name):
        parts = class_name.split('.')
        module = ".".join(parts[:-1])
        m = __import__( module, globals=globals())
        for comp in parts[1:]:
            m = getattr(m, comp)
        return m

    def __getattr__(self, attr):
        return self.services[attr]

    def get(self, get_url, headers={}):
        req_url = self.space_url + get_url
        self.logger.debug("GET %s" % req_url)
        self.logger.debug(headers)
        r = requests.get(req_url, auth=(self.space_user, self.space_passwd), headers=headers, verify=False)
        self.logger.debug(r)
        self.logger.debug(r.text)
        return r

    def post(self, post_url, headers, body):
        req_url = self.space_url + post_url
        self.logger.debug("POST %s" % req_url)
        self.logger.debug(headers)
        self.logger.debug(body)
        r = requests.post(req_url, auth=(self.space_user, self.space_passwd), data=body, headers=headers, verify=False)
        self.logger.debug(r)
        self.logger.debug(r.text)
        return r

    def put(self, put_url, headers, body):
        req_url = self.space_url + put_url
        self.logger.debug("PUT %s" % req_url)
        self.logger.debug(headers)
        self.logger.debug(body)
        r = requests.put(req_url, auth=(self.space_user, self.space_passwd), data=body, headers=headers, verify=False)
        self.logger.debug(r)
        self.logger.debug(r.text)
        return r

    def delete(self, delete_url):
        req_url = self.space_url + delete_url
        self.logger.debug("DELETE %s" % req_url)
        r = requests.delete(req_url, auth=(self.space_user, self.space_passwd), verify=False)
        return r