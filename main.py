import sys
import json
from code_base import systeminfo
from code_base.bandwidth_configurator import BandwidthConfigurator
from code_base.constants import Constants

limit_option = '-l'
reset_option = '-r'
show_option = '-s'
help_option = '-h'
path_option = '-p'
bw_option = '-b'

options = [limit_option, reset_option, show_option, help_option, path_option, bw_option]


def main(args):
    """
    Execute the program according to command line inputs.
    :param args: command line inputs
    :return:
    """
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
    # TODO(mmeinen): implement
    bwc = BandwidthConfigurator()
    bwc.limit()


def reset():
    # TODO(mmeinen): implement
    pass


def show():
    # TODO(mmeinen): implement
    pass


def show_help():
    """
    Show help text that gives instructions on how to use the program.
    :return:
    """
    try:
        with open(Constants.path_to_help_file, "r") as jsonFile:
            data = json.load(jsonFile)
        print("Description:")
        print("             " + data['Description'])
        print("Options:")
        for k, v in data.items():
            if k == "Options":
                for k1, v1 in v.items():
                    print("             " + v1['Command'] + ": " + v1['Description'])
        print("Usage:")
        for k,v in data.items():
            if k == 'Usage':
                for k1, v1 in v.items():
                    print("             Example:")
                    print("             " + v1['Command'])
                    print("             " + v1['Description'])
                    print("")
    except json.JSONDecodeError as e:
        print("Showing help failed!")
        exit(1)


def update_link_info_path(path_to_link_info):
    """
    Update the path to the link info file in the config.json file
    :param path_to_link_info: The path to link_info.json
    :return:
    """
    if not systeminfo.file_exists(path_to_link_info):
        print("File "+str(path_to_link_info)+" does not exist")
        exit(1)
    else:
        try:
            with open(Constants.path_to_config_file, "r") as jsonFile:
                data = json.load(jsonFile)

            data["PathToLinkInfo"] = path_to_link_info

            with open(Constants.path_to_config_file, "w") as jsonFile:
                json.dump(data, jsonFile, indent=4)
        except json.JSONDecodeError as e:
            print("Updating the path in config.json failed!")
            exit(1)


def update_default_bw(default_bandwidth):
    """
    Update the default bandwidth in the config.json file
    :param default_bandwidth: The default bandwidth (positive integer)
    :return:
    """
    try:
        bw = int(default_bandwidth)
    except ValueError:
        error_exit()

    if bw < 0:
        error_exit()
    try:
        with open(Constants.path_to_config_file, "r") as jsonFile:
            data = json.load(jsonFile)

        data["DefaultBandwidth"] = bw

        with open(Constants.path_to_config_file, "w") as jsonFile:
            json.dump(data, jsonFile, indent=4)
    except json.JSONDecodeError as e:
        print("Updating the default bandwidth in config.json failed!")
        exit(1)


def error_exit():
    """
    Exit because there were invalid arguments.
    :return:
    """
    print("Invalid arguments!")
    print("Type -h to get help.")
    exit(0)


if __name__ == '__main__':
    argv = sys.argv
    main(argv[1:])
