import io
import os
import sys
import getopt

HOLIDAYS_FILE = os.path.join("./data-files/holidays.txt")
PARSHIOT_FILE = os.path.join("./data-files/parshiot.txt")
ROOT_DIRECTORY = os.path.join(".")
USAGE_MESSAGE = "generate-sermon-directories.py -r <root-directory>"
SPECIAL_SHABBATOT = "Special Shabbatot"
SEFARIM = [
    "Bereishit",
    "Shemot",
    "Vayikra",
    "Bamidbar",
    "Devarim"
]

def main (argv):
    init_root_directory(argv)
    create_parasha_directories()
    create_holiday_directories()
    return

def init_root_directory(argv):
    global ROOT_DIRECTORY
    input_dir = argv[0]
    if (not input_dir.endswith("\\")):
        input_dir += "\\"        
    ROOT_DIRECTORY = os.path.join(input_dir)
    if (not os.path.exists(ROOT_DIRECTORY)):
        create = input(f'Root directory {ROOT_DIRECTORY} does not exist. Create root directory?  [y/N]:  ').lower()
        if (create == 'y' or create == 'yes'):
            os.makedirs(ROOT_DIRECTORY)
            return
        else:
            print(f'Did not create root directory {ROOT_DIRECTORY}. Script cancelled')
            sys.exit(0)
    return


def create_parasha_directories():
    parasha_file = open(PARSHIOT_FILE, "r")
    parshiyot = parasha_file.readlines()
    parasha_file.close()
    sefer_count = 1
    parasha_count = 1
    working_dir = ROOT_DIRECTORY
    for parasha in parshiyot:
        parasha = parasha.rstrip()
        if is_sefer(parasha):
            sefer_path = make_dir_path(ROOT_DIRECTORY,sefer_count,parasha)
            if (not os.path.isdir(sefer_path)):
                print(f"Creating {sefer_path}...")
                os.mkdir(sefer_path)
            working_dir = sefer_path
            parasha_count = 1
            parasha_dir = make_dir_path(working_dir,1,parasha)
            if (not os.path.isdir(parasha_dir)):
                print(f"Creating {parasha_dir}...")
                os.mkdir(parasha_dir)
            sefer_count += 1
            parasha_count += 1
        elif is_special(parasha):
            sefer_path = os.path.join(ROOT_DIRECTORY,parasha)
            if (not os.path.isdir(sefer_path)):
                print(f"Creating {sefer_path}...")
                os.mkdir(sefer_path)
            working_dir = sefer_path
            parasha_count = 1
        else:
            parasha_dir = make_dir_path(working_dir,parasha_count,parasha)
            if (not os.path.isdir(parasha_dir)):
                print(f"Creating {parasha_dir}...")
                os.mkdir(parasha_dir)
            parasha_count += 1
    return
    
def create_holiday_directories():
    holiday_dir = os.path.join(ROOT_DIRECTORY, "Holidays")
    if (not os.path.isdir(holiday_dir)):
        print(f"Creating {holiday_dir}...")
        os.mkdir(holiday_dir)
    holiday_file = open(HOLIDAYS_FILE, "r")
    holidays = holiday_file.readlines()
    holiday_file.close()
    holiday_count = 1
    for holiday in holidays:
        holiday = holiday.rstrip()
        holiday_sub_dir = make_dir_path(holiday_dir,holiday_count,holiday)
        if (not os.path.isdir(holiday_sub_dir)):
            os.mkdir(holiday_sub_dir)
        holiday_count +=1
    return

def is_sefer(parasha):
    return parasha in SEFARIM

def is_special(parasha):
    return parasha == SPECIAL_SHABBATOT

def make_dir_path(working_dir,count,name):
    dir_name = format_directory_name(count,name)
    return os.path.join(working_dir,dir_name)

def format_directory_name (count, name):
    prefix = ""
    if (count < 10):
        prefix = "0" + str(count)
    else:
        prefix = str(count)
    return prefix + " - " + name

if __name__ == "__main__":
    if (len(sys.argv) !=2):
        print('\nUsage is: generate-sermon-directories.py <root-directory>')
        print('If <root-directory> path contains a space, it must be placed in quotes \"\"\n')
        print('Reccomdation: Use a root directory under a cloud service (Dropbox, Google Drive, etc) to automatically back up to the cloud')
        sys.exit(0)
    main(sys.argv[1:])
