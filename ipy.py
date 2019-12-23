#!/usr/bin/env python

# pylint:disable=C0111,C0103

from sys import argv as sys_argv, exit as sys_exit, stderr as sys_stderr
from collections import OrderedDict
from os import environ as os_environ
from json import dumps as json_dumps
from yaml import dump as yaml_dump
from netaddr import (IPNetwork, AddrConversionError, AddrFormatError,
                     NotRegisteredError)


def usage():
    stderr('''
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
    ''')
    sys_exit(2)


def stderr(msg):
    print(msg, file=sys_stderr)


def to_int(val, dfltVal):
    return int(val) if str(val or '').isdigit() else dfltVal


def get_arg(ix, optional=False):
    if len(sys_argv) < (ix + 1):
        if optional:
            return None
        usage()
    return sys_argv[ix]


def end(val, **kwargs):
    if isinstance(val, bool):
        stderr(str(val))
        sys_exit(0 if val else 3)
    else:
        print(val, end=kwargs.get('end', '\n'))
        sys_exit(0)


def to_net(val, noneVal, inclObj=True):
    n = OrderedDict()
    try:
        n['_'] = IPNetwork(val)
    except (TypeError, ValueError, AddrConversionError, AddrFormatError,
            NotRegisteredError) as e:
        stderr('ERROR: Invalid input: {}'.format(e))
        sys_exit(1)
    bcast = n['_'].broadcast or noneVal
    n['ip'] = str(n['_'].ip)
    n['cidrBits'] = int(str(n['_'].cidr).split('/')[1])
    n['netmask'] = str(n['_'].netmask)
    n['cidrNet'] = '{}/{}'.format(n['_'].network, n['cidrBits'])
    n['net'] = '{}/{}'.format(n['_'].network, n['_'].netmask)
    n['network'] = str(n['_'].network)
    n['broadcast'] = bcast if bcast is None else str(bcast)
    n['ipCount'] = int(n['_'].size)
    n['version'] = 'IPv{}'.format(n['_'].version)
    if not inclObj:
        del n['_']
    return n


earg = str(os_environ.get('IPY_ARG') or '')
action = get_arg(1)

if action == 'info:ini':
    net = to_net(get_arg(2), '', False)
    end('\n'.join(['{}={}'.format(k, v) for k, v in net.items()]))

if action == 'info:json':
    net = to_net(get_arg(2), None, False)
    earg = to_int(earg, 2)
    earg = None if earg == 0 else earg
    end(json_dumps(net, indent=earg))

if action == 'info:yaml':
    net = to_net(get_arg(2), None, False)
    earg = earg or None
    end(yaml_dump(dict(net), default_flow_style=False, default_style=earg),
        end='')

net = to_net(get_arg(2), '-')
earg = earg or '\n'

if action == 'info':
    end(earg.join([str(v) for k, v in net.items() if k != '_']))
if action == 'ips':
    end(earg.join([str(ip) for ip in net['_']]))
if action == 'hosts':
    end(earg.join([str(ip) for ip in net['_'].iter_hosts()]))
if action == 'next':
    end(str(net['_'].next(to_int(get_arg(3, True), 1))))
if action == 'previous':
    end(str(net['_'].previous(to_int(get_arg(3, True), 1))))
if action == 'is_inside':
    net2 = to_net(get_arg(3), None)
    end(net['_'] in net2['_'])
if action == 'is_loopback':
    end(net['_'].is_loopback())
if action == 'is_public':
    end(not net['_'].is_private())
if action == 'is_private':
    end(net['_'].is_private())
if action == 'is_reserved':
    end(net['_'].is_reserved())

if action in net:
    end(net[action])

usage()
