# 10mb video plugin

import os
import sys
from support import *

class video:
    def __init__(self):
        self.can_use_progress = True
        self.prog = None

    @staticmethod
    def can_handle(file_path):
        file_type = get_file_type(file_path)
        return "video" in file_type.mime

    def can_run(self):
        if not check_command_exists("ffmpeg"):
            print("error: ffmpeg not found. you can install it with your favourite package manager.")
            return False

        if not check_command_exists("ffprobe"):
            print("error: ffprobe not found. you can install it with your favourite package manager.")
            return False

        print(f"video: ffmpeg found at {get_command_path('ffmpeg')}, ffprobe found at {get_command_path('ffprobe')}")

        try:
            import better_ffmpeg_progress
            self.prog = better_ffmpeg_progress
        except ImportError:
            self.can_use_progress = False
            print("warning: better_ffmpeg_progress not found. you can install it with pip install better-ffmpeg-progress.")
            print("warning: will use stdout for progress (ugly!!!)")

        return True

    def compress(self, input_file, target_size, output_file, overwrite):

        # if the full path is not provided, assume the file is in the current directory
        if "/" not in input_file:
            # full path of current directory
            input_folder = os.getcwd() + "/"
        else:
            input_folder = ""

        if output_file is None:
            output_file = input_folder + input_file + f".{target_size}mb.mp4"
        else:
            output_file = input_folder + escape_filename(output_file)

        temp_output_file = create_temp_file(".mp4")

        # ffmpeg really doesn't like spaces in filenames. copy the file to a temporary location
        temp_file = make_temp_copy(input_file, "video")

        if overwrite:
        # we want to overwrite the original file. copy over the original file to a temporary location
            output_file = input_file
            os.remove(input_file)


        input_file = temp_file

        # cd to tempdir so we don't litter
        cd_to_temp_dir()

        duration_s = self.get_video_duration(input_file)

        # if the output file exists, overwrite it
        if os.path.exists(unescape_filename(output_file)):
            print(f"video: output file {output_file} exists, overwriting")
            os.remove(unescape_filename(output_file))

        print(f"video: duration is {duration_s}s")

        # calculate the bitrate - target in kilobits per second / duration in seconds
        bitrate = round(((target_size * 7800 / duration_s)), 2)
        print(f"video: bitrate will be {bitrate}k")

        if self.can_use_progress:
            self.compress_video_dual_pass(input_file, bitrate, temp_output_file)
        else:
            self.compress_video_dual_pass_fallback(input_file, bitrate, temp_output_file)

        # if we're overwriting the original file, move the temp file back
        print(temp_output_file, output_file)
        os.rename(temp_output_file, unescape_filename(output_file))


        # cleanup
        cleanup_temp_file(input_file)




    def get_video_duration(self, file_path):
        command = f"{get_command_path('ffprobe')} -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 {file_path}"
        result = run_command_output(command)
        return float(result.stdout)

    def compress_video_dual_pass(self, input_file, bitrate, output_file):
        args = f"ffmpeg -y -i {input_file} -c:v libx264 -preset medium -b:v {bitrate}k -pass 1 -c:a libfdk_aac -b:a 128k -f mp4 /dev/null"
        process = self.prog.FfmpegProcess(args.split(), ffmpeg_log_level=0)
        success = process.run()
        if success:
            print("error: first pass failed")
            sys.exit(1)
        args2 = f"ffmpeg -y -i {input_file} -c:v libx264 -preset medium -b:v {bitrate}k -pass 2 -c:a libfdk_aac -b:a 128k {output_file}"
        process2 = self.prog.FfmpegProcess(args2.split(), ffmpeg_log_level=0)
        success2 = process2.run()
        if success2:
            print("error: second pass failed")
            sys.exit(1)


    def compress_video_dual_pass_fallback(self, input_file, bitrate, output_file):
        command_pass1 = f"ffmpeg -y -i {input_file} -c:v libx264 -preset medium -b:v {bitrate}k -pass 1 -c:a libfdk_aac -b:a 128k -f mp4 /dev/null"
        run_command(command_pass1)
        command_pass2 = f"ffmpeg -y -i {input_file} -c:v libx264 -preset medium -b:v {bitrate}k -pass 2 -c:a libfdk_aac -b:a 128k {output_file}"
        run_command(command_pass2)