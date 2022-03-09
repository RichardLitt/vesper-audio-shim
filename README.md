# Vesper Audio Shims

These are files to automatically rename audio recordings for Vesper.

*You will need to edit this file for it to work with your system. In particular, change the directories it accesses. Some familiarity with Python required.*

## Install

Clone this repository. Ensure you have Python3.

## Usage

Change directory to the directory where you have files that you wish to rename. For instance, I `cd` to my external AudioMoth SDD. AudioMoth automatically records files with the format `20211023_010006.WAV`. This isn't useful for Vesper.

Run:

```
python3 ~/src/vesper/vesper-audio-shim/rename_audiomoth_recordings.py
```

Your files should now be renamed, and in the same folder. I'm also instituting an automatic copying mechanism to copy files directly to the Vesper Recordings/ folder I need them to be in.

## Contribute

Sure!

## License

MIT.