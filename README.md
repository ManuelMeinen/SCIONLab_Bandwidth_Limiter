# SCIONLab bandwidth limiter

This program is supposed to be used on an attachment point of the SCIONLab network. 
It limits the bandwidth per IP-address for user-ASes using TC according to the configuration in the link_info.json file obtained by the SCIONLab server.


## Getting Started

To use this program clone it to the attachment point and run 

``./sconlab_bw_limiter -b DEFAULT_BANDWIDTH -p PATH/TO/LINK/INFO/FILE``


After that you are good to go. You can now use the following commands:

``./sconlab_bw_limiter -h`` (show help text)

``./sconlab_bw_limiter -l`` (limit the bandwidth)

``./sconlab_bw_limiter -r`` (reset bandwidth limitations)

``./sconlab_bw_limiter -s`` (show current TC configuration)

### Prerequisites

To be able to run this program you need Python3 and TC (iproute2) installed on your Ubuntu machine.


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## About SCION/SCIONLab
To learn more about SCIONLab visit:   
https://www.scionlab.org  
To learn more about SCION visit:  
https://www.scion-architecture.net



