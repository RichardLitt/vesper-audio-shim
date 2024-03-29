import datetime
import sys
import argparse
import os
import re
# TODO Update to updated timezone dep
import pytz
import shutil

# Example: 20220302_040000.WAV

_FILE_NAME_RE = re.compile(
    r'^(\d\d\d\d)(\d\d)(\d\d)_(\d\d)(\d\d)(\d\d)\.WAV$')

# TODO Make this an arg
# May not be necessary - Audiomoth always records in Z, and Vesper can always read Z. 
_TIME_ZONE = pytz.timezone('Europe/London')


def _main(args):
    _rename_files('.', args)

def _rename_files(dir_path, args):
    for _, dir_names, file_names in os.walk(dir_path):
        for file_name in file_names:
            _rename_file(file_name, args)
        del dir_names[:]

def _rename_file(file_name, args):
    new_file_name = _transform_file_name(file_name, args)
    # TODO Should find a way to make this not brittle
    # new_file_name = args.outputDirectory + new_file_name
    # Another option
    # new_file_name = 'Renamed recordings/' + new_file_name
    if new_file_name is None:
        print('skipping "{}"...'.format(file_name))
    else:
        print('renaming "{}" to "{}"...'.format(file_name, new_file_name))
        os.rename(file_name, new_file_name)
        print('attempting to copy "{}"...'.format(new_file_name))
        ## TODO Re-add with logic
        # This copies to another directory. but it only _copies_, it doesn't move.
        # shutil.copy2(os.getcwd() + '/' + new_file_name, args.outputDirectory)


def _transform_file_name(file_name, args):

    m = _FILE_NAME_RE.match(file_name)

    if m is not None:

        (year, month, day, hour, minute, second) = m.groups()

        station = args.station

        month = int(month)
        day = int(day)
        year = int(year)
        hour = int(hour)
        minute = int(minute)
        second = int(second)
        dt = datetime.datetime(year, month, day, hour, minute, second)
        dt = _TIME_ZONE.localize(dt).astimezone(pytz.utc)

        return '{}_{}-{:02d}-{:02d}_{:02d}.{:02d}.{:02d}_Z.wav'.format(
                   station, dt.year, dt.month, dt.day, dt.hour, dt.minute, dt.second)

    else:
        return None

def create_arg_parser():
    # Creates and returns the ArgumentParser object
    parser = argparse.ArgumentParser(description='Description of your app.')
    parser.add_argument('station',
                    help='Station name')
    # TODO Implement
    parser.add_argument('--copy',
                    help='Copy the contents instead of moving them')
    # TODO Check renaming
    parser.add_argument('--dst',
                    help='Path to the output directory.')
    # TODO Implement
    # parser.add_argument('--tz',
    #                 help='Time zone (Default: UTC).')
    return parser


if __name__ == "__main__":
    arg_parser = create_arg_parser()
    parsed_args = arg_parser.parse_args(sys.argv[1:])
    _main(parsed_args)
