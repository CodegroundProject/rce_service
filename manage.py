import os
from run_lang.run_lang import create_app

if __name__ == '__main__':
    port = int(os.getenv('RCE_PORT', 5000))
    create_app().run('0.0.0.0', port)