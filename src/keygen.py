import os
import subprocess

import dotenv

dotenv_file = dotenv.find_dotenv()
dotenv.find_dotenv(dotenv_file)

CUR_USER = os.getlogin()
PRIV_SSH_DIR = f"/home/{CUR_USER}/.ssh"
KEY_NAME = 'jwtRS256.key'


def key_present():
    """Checks to see if there is an RSA already present. Returns a bool."""
    if "jwtRS256.key" in os.listdir(PRIV_SSH_DIR):
        return True
    else:
        return False


def show(msg):
    """Local print() function."""
    print(msg)


def add_to_env():
    try:
        with open(f'/home/{CUR_USER}/.ssh/{KEY_NAME}', 'r')as private_key:
            os.environ["SECRET_KEY_PRIVATE"] = private_key.read()
            dotenv.set_key(dotenv_file, "SECRET_KEY_PRIVATE", os.environ["SECRET_KEY_PRIVATE"])

        with open(f'/home/{CUR_USER}/.ssh/{KEY_NAME}.pub', 'r')as public_key:
            os.environ["SECRET_KEY_PUBLIC"] = public_key.read()
            dotenv.set_key(dotenv_file, "SECRET_KEY_PUBLIC", os.environ["SECRET_KEY_PUBLIC"])
    except FileNotFoundError:
        print('No such file or directory')


def gen_key():
    """Generate a SSH Key."""
    os.chdir(PRIV_SSH_DIR)
    if key_present():
        add_to_env()
        show("A key is already present.")
    else:
        # Genarate private key
        # subprocess.call(['ssh-keygen', '-t', 'rsa', '-b', '4096', '-m', 'PEM', '-f', KEY_NAME, '-P', '12345'],
        #                 shell=False)
        subprocess.call(['ssh-keygen', '-t', 'rsa', '-b', '4096', '-m', 'PEM', '-f', KEY_NAME],
                       shell=False)
        # subprocess.call(['openssl', 'rsa', '-in', KEY_NAME, '-pubout', '-outform', 'PEM', '-out', 'jwtRS256.key.pub', '-passin', 'pass:12345'],
        #                 shell=False)
        subprocess.call(
            ['openssl', 'rsa', '-in', KEY_NAME, '-pubout', '-outform', 'PEM', '-out', 'jwtRS256.key.pub'],
            shell=False)
        add_to_env()


def get_hs256():
    subprocess.call(
        ['openssl', 'rand', '-out', 'secret.key', '-base64', '64'], shell=False)


print(gen_key())