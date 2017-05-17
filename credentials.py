import os

class Credentials(object):
    def __init__(self):
            self.username = os.environ['OS_USERNAME']
            self.password = os.environ['OS_PASSWORD']
            self.auth_url = os.environ['OS_AUTH_URL']
            if os.environ.get('OS_PROJECT_NAME'):
                self.project_name = os.environ['OS_PROJECT_NAME']
            elif os.environ.get('OS_TENANT_NAME'):
                print("WARNING: No $OS_PROJECT_NAME set, using $OS_TENANT_NAME")
                self.project_name = os.environ['OS_TENANT_NAME']
            else:
                print("ERROR: Please set either $OS_PROJECT_NAME or $OS_TENANT_NAME.")
                exit(1)
            self.identity_version = os.environ['OS_IDENTITY_API_VERSION']
            if os.environ['OS_IDENTITY_API_VERSION']:
                print("WARNING: $OS_IDENTITY_API_VERSION not specified, setting it to 3.")
                self.identity_version = 3
            self.user_domain_id='default',
            self.project_domain_id='default'

