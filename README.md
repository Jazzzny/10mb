# 10mb: file compressor

A super simple multi-use file compressor written in Python that can compress files to a specified size, in a format supported by Discord, designed to make files easily uploadable to Discord.

## Design
Built with an extendable plugin system, 10mb can easily be adapted to support more file types and formats.

The plugin system is designed to be easy to use, with a simple class-based architecture. All built-in file types are supported through plugins.

## Supported File Types
- Image Files
- Video Files
- Audio Files

## Usage
```bash
python 10mb.py [-h] [--output OUTPUT] [--overwrite] [--size SIZE] input
```
Where:
- `input` is the path to the file you want to compress
- `--output` is the path to the output file (optional)
- `--overwrite` overwrites the input file with the compressed file (optional)
- `--size` is the target size of the compressed file in MB (default: 10)

## Installation
For best results, install the optional packages using the following command:
```bash
pip3 install -r requirements.txt
```
The following commands must be present in PATH:
- `ffmpeg`
- `ffprobe`
- `convert` (ImageMagick)

The following commands are optional:
- `pngquant` (for PNG files to remain transparent)

