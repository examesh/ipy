

<p align="center">
<img src="https://raw.githubusercontent.com/examesh/ipy/master/ipy.png" width=250px>
</p>


***


**[ipy](https://github.com/examesh/ipy)** is an easy to use ip and network utility that supports multiple output formats like CSV, JSON and YAML. It is based on the awesome [netaddr](https://netaddr.readthedocs.io/en/latest/) library.



## Usage

#### Print ip details:

```shell
# json format
$ ipy info:json 10.0.0.1
{
  "ip": "10.0.0.1",
  "cidrBits": 32,
  "netmask": "255.255.255.255",
  "cidrNet": "10.0.0.1/32",
  "net": "10.0.0.1/255.255.255.255",
  "network": "10.0.0.1",
  "broadcast": null,
  "ipCount": 1,
  "version": "IPv4"
}


# txt format ("\n" as separator)
$ ipy info 10.0.0.1
10.0.0.1
32
255.255.255.255
10.0.0.1/32
10.0.0.1/255.255.255.255
10.0.0.1
-
1
IPv4


# csv format
$ IPY_ARG="," ipy.py info 10.0.0.1   # IPY_ARG defines separator
10.0.0.1,32,255.255.255.255,10.0.0.1/32,10.0.0.1/255.255.255.255,10.0.0.1,-,1,IPv4


# yaml format
$ ipy info:yaml 10.0.0.1
broadcast: null
cidrBits: 32
cidrNet: 10.0.0.1/32
ip: 10.0.0.1
ipCount: 1
net: 10.0.0.1/255.255.255.255
netmask: 255.255.255.255
network: 10.0.0.1
version: IPv4


# ini format
$ ipy info:ini 10.0.0.1
ip=10.0.0.1
cidrBits=32
netmask=255.255.255.255
cidrNet=10.0.0.1/32
net=10.0.0.1/255.255.255.255
network=10.0.0.1
broadcast=
ipCount=1
version=IPv4
```


#### Print network and host details:

```shell
$ ipy network 10.0.0.34/24
10.0.0.0

$ ipy hosts 10.0.1.34/24
10.0.0.1,10.0.0.2,...,10.0.0.254

$ ipy is_inside 10.0.0.1 10.10.10.0/24
False

$ ipy next 10.0.0.10/24
10.0.1.0/24
$ ipy next 10.0.0.10
10.0.0.11/32
$ ipy previous 10.0.0.10 3
10.0.0.7/32
```


#### All options:

```shell
$ ipy -h

    ipy <action> <ip[/netmask]>
        # action:     # configuration:
        info          # export IPY_ARG=,      # separator
        info:json     # export IPY_ARG=2      # pretty-print indent
        info:yaml     # export IPY_ARG='""'   # style character
        info:ini

    ipy <action> <ip[/netmask]>
        ip
        cidrBits
        netmask
        cidrNet
        net
        network
        broadcast
        version
        ipCount
        ips
        hosts
        next [<step>]
        previous [<step>]
        is_loopback
        is_public
        is_private
        is_reserved

    ipy <action> <ip[/netmask]> <ip[/netmask]>
        is_inside

    Examples:
        ipy info 10.0.0.1
        ipy info:yaml 10.0.0.0/24
        ipy version 10.0.0.1
        ipy ipCount 10.0.0.0/24
        ipy hosts 10.0.0.0/24
        ipy is_inside 10.0.0.1 10.0.0.0/24
        IPY_ARG=, ipy info 10.0.0.1
        IPY_ARG=0 ipy info:json 10.0.0.0/24
```




## Installation

#### Binary

The `dist/` folder contains a ready to use Linux x86-64 binary created with [pyinstaller](http://www.pyinstaller.org/). BUT: Cause of (glibc) library incompatibilities it doesn't work with all distributions. If you get execution errors, you can compile the binary by yourself with the included `dist/build.sh` (see the next section).

```shell
# try ipy binary
cd /usr/local/bin
sudo curl --fail -L -o ipy https://raw.githubusercontent.com/examesh/ipy/master/dist/ipy.linux_x86-64
sudo chmod 755 ipy
./ipy -h
```

#### Python

[ipy](https://github.com/examesh/ipy) is a [Python 3](https://www.python.org) application that has two package dependencies: [netaddr](https://netaddr.readthedocs.io/en/latest/) and [PyYAML](https://pyyaml.org/wiki/PyYAML).

```shell
mkdir -p ${HOME}/tmp
cd ${HOME}/tmp
git clone https://github.com/examesh/ipy.git
cd ipy
pip install --requirement requirements.txt  # also installs pyinstaller
./ipy.py -h
```

To create the Linux x86-64 binary:

```shell
cd ${HOME}/tmp/ipy/dist
./build.sh      # needs pyinstaller
./ipy.linux_x86-64 -h
```

<br><br>
<sub>[Powered by ExaMesh](https://examesh.de)</sub>
