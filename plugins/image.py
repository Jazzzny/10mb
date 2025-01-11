# 10mb image plugin

import os
from support import *

class image:
    def __init__(self):
        self.can_use_pngquant = True

    @staticmethod
    def can_handle(file_path):
        file_type = get_file_type(file_path)
        return "image" in file_type.mime

    def can_run(self):
        # we want to check for imagemagick
        if not check_command_exists("convert"):
            print("error: imagemagick not found. you can install it with your favourite package manager.")
            return False

        if not check_command_exists("pngquant"):
            print("warn: pngquant not found. you can install it with your favourite package manager. pngs will not be transparent.")
            self.can_use_pngquant = False
        else:
            print(f"image: pngquant found at {get_command_path('pngquant')}")

        print(f"image: imagemagick found at {get_command_path('convert')}")
        return True

    def compress(self, input_file, target_size, output_file, overwrite):
        is_png = "png" in get_file_type(input_file).mime

        if output_file is None:
            output_file = input_file + f".{target_size}mb.{'jpg' if not is_png else 'png'}"

        output_file = escape_filename(output_file)


        temp_file = make_temp_copy(input_file, "image")

        if overwrite:
        # we want to overwrite the original file. copy over the original file to a temporary location
            output_file = input_file
            os.remove(input_file)


        input_file = temp_file

        # cd to tempdir so we don't litter
        cd_to_temp_dir()

        # if png, we want to use special logic
        if "png" in get_file_type(input_file).mime and self.can_use_pngquant:
            self.run_png_conversion(input_file, target_size, output_file)
        else:
            self.run_imagemagick_conversion(input_file, target_size, output_file)

    def run_png_conversion(self, input_file, target_size, output_file):
        # we want to use pngquant for pngs
        run_command(f"pngquant --quality=0-100 --speed 1 --force --output {output_file} {input_file}")

        # we want to check if the file is smaller than the target size
        if get_file_size_kb(output_file) > target_size * 1024:
            print("warn: png is still too large! will use imagemagick to compress further (loses transparency)")
            self.run_imagemagick_conversion(input_file, target_size, output_file)

    def run_imagemagick_conversion(self, input_file, target_size, output_file):
        run_command(f"convert {input_file} -define jpeg:extent={target_size*1024}kb {output_file}")

