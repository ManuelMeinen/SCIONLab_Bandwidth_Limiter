import sys
import json
from code_base import systeminfo

limit_option = '-l'
reset_option = '-r'
show_option = '-s'
help_option = '-h'
path_option = '-p'
bw_option = '-b'

options = [limit_option, reset_option, show_option, help_option, path_option, bw_option]

#Possible usages:
    # main.py -l
    # main.py -r
    # main.py -s
    # main.py -h
    # main.py -p path/to/link/info
    # main.py -b 1234
    # {l,r,s} can be combined with one or two of {p,b}
    # {h} can't be combined with anything

def main(args):
    print(args)
    if help_option in args and len(args) == 1:
        show_help()
    else:
        if help_option in args:
            error_exit()
        if path_option in args:
            path_index = args.index(path_option)+1
            if path_index+1 > len(args):
                error_exit()
            else:
                update_link_info_path(args[path_index])
            args.remove(args[path_index])
            args.remove(args[path_index-1])
        if bw_option in args:
            bw_index = args.index(bw_option)+1
            if bw_index+1 > len(args):
                error_exit()
            else:
                update_default_bw(args[bw_index])
            args.remove(args[bw_index])
            args.remove(args[bw_index-1])
    if len(args) > 1:
        error_exit()
    else:
        if limit_option in args:
            limit()
        else:
            if reset_option in args:
                reset()
            else:
                if show_option in args:
                    show()
                else:
                    error_exit()



def limit():
    pass


def reset():
    pass


def show():
    pass


def show_help():
    pass


def update_link_info_path(path_to_link_info):
    if not systeminfo.file_exists(path_to_link_info):
        print("File "+str(path_to_link_info)+" does not exist")
        exit(1)
    else:
        try:
            with open("config_files/config.json", "r") as jsonFile:
                data = json.load(jsonFile)

            data["PathToLinkInfo"] = path_to_link_info

            with open("config_files/config.json", "w") as jsonFile:
                json.dump(data, jsonFile, indent=4)
        except:
            print("Updating the path in config.json failed!")
            exit(1)


def update_default_bw(default_bandwidth):
    pass


def error_exit():
    print("Invalid arguments!")
    print("Type -h to get help.")
    exit(0)


if __name__ == '__main__':
    argv = sys.argv
    main(argv[1:])
