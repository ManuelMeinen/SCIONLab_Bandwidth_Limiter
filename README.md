# SCIONLab bandwidth limiter

This program is supposed to be used on an attachment point of the SCIONLab network. 
It limits the bandwidth per IP-address for user-ASes using TC according to the configuration in the link_info.json file obtained by the SCIONLab server.


## Getting Started

To use this program clone it to the attachment point and run 

``python3 main.py -b DEFAULT_BANDWIDTH -p PATH/TO/LINK/INFO/FILE``


After that you are good to go. You can now use the following commands:

``python3 main.py -h`` (show help text)

``python3 main.py -l`` (limit the bandwidth)

``python3 main.py -r`` (reset bandwidth limitations)

``python3 main.py -s`` (show current TC configuration)

### Prerequisites

To be able to run this program you need Python3 and TC (iproute2) installed on your Ubuntu machine.


## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## About SCION/SCIONLab
To learn more about SCIONLab visit:   
https://www.scionlab.org  
To learn more about SCION visit:  
https://www.scion-architecture.net



