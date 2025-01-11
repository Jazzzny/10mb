# 10mb image plugin

import os
import sys
from support import *

class image:

    @staticmethod
    def can_handle(file_path):
        file_type = get_file_type(file_path)
        return "image" in file_type.mime

    def can_run(self):
        # we want to check for imagemagick
        if not check_command_exists("convert"):
            print("error: imagemagick not found. you can install it with your favourite package manager.")
            return False

        print(f"image: imagemagick found at {get_command_path('convert')}")
        return True

    def compress(self, input_file, target_size, output_file, overwrite):
        is_png = "png" in get_file_type(input_file).mime

        if output_file is None:
            output_file = input_file + f".{target_size}mb.{'jpg' if not is_png else 'png'}"
        else:
            output_file = escape_filename(output_file)

        temp_output_file = create_temp_file(".")

        # ffmpeg really doesn't like spaces in filenames. copy the file to a temporary location
        temp_file = make_temp_copy(input_file, "image")

        if overwrite:
        # we want to overwrite the original file. copy over the original file to a temporary location
            output_file = input_file
            os.remove(input_file)


        print(temp_file)
        input_file = temp_file

        # cd to tempdir so we don't litter
        cd_to_temp_dir()

        # if png, we want to use special logic
        if "png" in get_file_type(input_file).mime:
            self.run_png_conversion(input_file, target_size, output_file, overwrite)
        else:
            run_command(f"convert {input_file} -define jpeg:extent={target_size}mb {output_file}")


    def run_png_conversion(self, input_file, target_size, output_file, overwrite):
