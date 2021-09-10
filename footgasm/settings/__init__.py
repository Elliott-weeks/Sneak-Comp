import os

env_name = os.getenv('ENV_NAME', 'prod')

if env_name == 'local':
    from .local import *
else:
    from .production import *
