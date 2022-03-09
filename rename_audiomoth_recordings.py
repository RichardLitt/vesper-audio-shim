import datetime
import os
import re
import pytz
import shutil

# Example: 20220302_040000.WAV

_FILE_NAME_RE = re.compile(
    r'^(\d\d\d\d)(\d\d)(\d\d)_(\d\d)(\d\d)(\d\d)\.WAV$')

_TIME_ZONE = pytz.timezone('Europe/London')


def _main():
    _rename_files('.')

def _rename_files(dir_path):
    for _, dir_names, file_names in os.walk(dir_path):
        for file_name in file_names:
            _rename_file(file_name)
        del dir_names[:]



def _rename_file(file_name):
    new_file_name = _transform_file_name(file_name)
    if new_file_name is None:
        print('skipping "{}"...'.format(file_name))
    else:
        print('renaming "{}" to "{}"...'.format(file_name, new_file_name))
        os.rename(file_name, new_file_name)
        print('attempting to copy "{}"...'.format(file_name))
        shutil.copy2(file_name, '/Users/richard/Sound/edinburgh-nocmig/Recordings/')


def _transform_file_name(file_name):

    m = _FILE_NAME_RE.match(file_name)

    if m is not None:

        (year, month, day, hour, minute, second) = m.groups()

        station = 'Edinburgh'

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

if __name__ == '__main__':
    _main()
