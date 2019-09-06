import datetime
import os
import re

import pytz


_FILE_NAME_RE = re.compile(
    r'^(\d\d\d\d)-(Aug|Sep)-(\d\d)-(\d\d)-(\d\d)-(\d\d)\.wav$')

_TIME_ZONE = pytz.timezone('US/Eastern')


def _main():
    _rename_files('.')

    # _test_transform_file_name()


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


def _transform_file_name(file_name):

    m = _FILE_NAME_RE.match(file_name)

    if m is not None:

        (year, month, day, hour, minute, second) = m.groups()

        station = 'NBNC'

        if month == 'Aug':
            month  = 8
        if month == 'Sep':
            month = 9

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


def _test_transform_file_name():

    cases = (
        '6 4-13-2016_8;30;00_PM.wav',
        '2 4-29-2016_8;30;00_PM.wav',
        '5 4-12-2016_8;30;00_PM.wav',
        '3 4-24-2016_8;30;00_PM.wav',
        '7 4-23-2016_8;30;00_PM.wav',
        '8 4-24-2016_8;30;00_PM.wav',
        '4 4-24-2016_8;30;00_PM.wav',
        '1 4-24-2016_8;30;00_AM.wav',
        '1 10-3-2016_11;30;00_PM.wav'
    )

    for case in cases:
        print('"{}" "{}"'.format(case, _transform_file_name(case)))


if __name__ == '__main__':
    _main()
