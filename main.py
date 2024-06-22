# -*- coding: utf-8 -*-

import datetime
import os
import zipfile
from time import sleep

user_home = os.path.expanduser('~')
backup_dir = os.path.join(user_home, 'EldenRingBackups')
app_data_roaming = os.getenv('APPDATA')
elden_ring_save_dir = os.path.join(app_data_roaming, 'EldenRing')


def load_saves() -> list[str]:
    user_save_dir_list = []
    for item in os.listdir(elden_ring_save_dir):
        fullpath = os.path.join(elden_ring_save_dir, item)
        if os.path.isdir(fullpath):
            user_save_dir_list.append(fullpath)
    return user_save_dir_list


def create_archive(dirs: list[str]) -> str:
    date = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    archive_name = f'{date}.zip'
    archive_abs_path = os.path.join(backup_dir, archive_name)
    with zipfile.ZipFile(archive_abs_path, 'w', zipfile.ZIP_STORED) as z:
        for save in dirs:
            for dir_path, dir_names, filenames in os.walk(save):
                fpath = dir_path.replace(elden_ring_save_dir, '')
                if fpath != '':
                    fpath = fpath + os.sep
                for filename in filenames:
                    z.write(os.path.join(dir_path, filename), os.path.join(fpath, filename))
    return archive_name


def main():
    if not os.path.exists(backup_dir):
        os.makedirs(backup_dir)
    save_dirs = load_saves()
    zip_filename = create_archive(save_dirs)
    print(f'Archive filename：{zip_filename}')
    os.startfile(backup_dir)
    sleep(3)


if __name__ == '__main__':
    main()
