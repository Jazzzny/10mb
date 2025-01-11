# support functions for the plugins

import filetype
import shutil
import subprocess
import tempfile
import os

def get_file_type(file_path):
    return filetype.guess(file_path)

def get_file_size_kb(file_path):
    return os.path.getsize(file_path) / 1024

def check_command_exists(command):
    return shutil.which(command) is not None

def get_command_path(command):
    return shutil.which(command)

def run_command(command):
    return subprocess.run(command, shell=True, check=True)

def run_command_quiet(command):
    return subprocess.run(command, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def run_command_output(command):
    return subprocess.run(command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

def make_temp_copy(file_path, file_name):
    # same extension as original, with the file name
    file_extension = os.path.splitext(file_path)[1]
    tempdir = tempfile.gettempdir()
    temp_file = os.path.join(tempdir, file_name + file_extension)

    shutil.copy(file_path, temp_file)
    # return the path.
    return temp_file

def create_temp_file(extension):
    # just name temp.whatever
    return tempfile.NamedTemporaryFile(delete=False, suffix=extension).name

def cleanup_temp_file(file_path):
    os.remove(file_path)

def escape_filename(file_path):
    return file_path.replace(" ", "\ ")

def unescape_filename(file_path):
    return file_path.replace("\ ", " ")

def cd_to_temp_dir():
    os.chdir(tempfile.gettempdir())