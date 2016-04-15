#!/usr/bin/env python

#
# The author disclaims copyright to this source code.  In place of
# a legal notice, here is a blessing:
#
#    May you do good and not evil.
#    May you find forgiveness for yourself and forgive others.
#    May you share freely, never taking more than you give.
#

#
# Standard library imports.
#

import array
import getpass
import sha as sha_module
import struct
import sys

#
# Third-party imports.
#

try:
    # http://www.amk.ca/python/code/crypto
    from Crypto.Cipher import Blowfish
    def new_blowfish_cipher(key):
        return Blowfish.new(key)
except ImportError:
    sys.stderr.write('PyCrypto not installed. Using blowfish.py.\n')
    # http://bofh.concordia.ca/blowfish.py
    from pwsafe import blowfish
    def new_blowfish_cipher(key):
        return blowfish.Blowfish(key)

# http://codespeak.net/svn/pypy/dist/pypy/lib/sha.py
from pwsafe import sha_pypy

#
# Utility functions.
#

def dump_bytes(out, s):
    for c in s:
        out.write('%02X' % ord(c))
    print

def swap_bytes(s):
    a = array.array('L', s)
    a.byteswap()
    return a.tostring()

#
# This is the good stuff.
#

def read_entries(path_to_file, password):
    f = file(path_to_file, 'rb')

    rnd = f.read(8)
    hash_rnd = f.read(20)

    sha = sha_module.new()
    sha.update(rnd)
    sha.update('\0\0')
    sha.update(password)
    temp_salt = sha.digest()

    cipher = new_blowfish_cipher(temp_salt)

    for i in range(1000):
        rnd = swap_bytes(rnd)
        rnd = cipher.encrypt(rnd)
        rnd = swap_bytes(rnd)

    sha = sha_pypy.new()
    sha.H0 = 0
    sha.H1 = 0
    sha.H2 = 0
    sha.H3 = 0
    sha.H4 = 0
    sha.update(rnd)
    sha.update('\0\0')
    check_hash = sha.digest()

    if check_hash != hash_rnd:
        sys.stderr.write('Invalid password!\n')
        sys.exit(1)

    salt = f.read(20)
    ip = f.read(8)

    sha = sha_module.new()
    sha.update(password)
    sha.update(salt)
    key = sha.digest()

    cipher = new_blowfish_cipher(key)

    record_types = {
        0x00: 'None',
        0x01: 'UUID',
        0x02: 'Group',
        0x03: 'Title',
        0x04: 'Username',
        0x05: 'Notes',
        0x06: 'Password',
        0x07: 'Creation Time',
        0x08: 'Password Modification Time',
        0x09: 'Last Access Time',
        0x0A: 'Password Lifetime',
        0x0B: 'Password Policy',
        0x0C: 'Last Mod. Time',
        0xFF: 'End of Entry'
    }

    record_count = 0

    entries = []
    entry = {}

    while True:

        data = f.read(8)

        if not data:
            break

        next_ip = data
        data = swap_bytes(data)
        data = cipher.decrypt(data)
        data = swap_bytes(data)
        da = array.array('L', data)
        ipa = array.array('L', ip)
        da[0] ^= ipa[0]
        da[1] ^= ipa[1]
        data = da.tostring()
        length, record_type = struct.unpack('<LL', data)
        ip = next_ip

        #print 'length:', length
        #print 'record_type:', record_type

        if length == 0:
            length = 8

        s = ''

        while length > 0:
            data = f.read(8)
            next_ip = data
            data = swap_bytes(data)
            data = cipher.decrypt(data)
            data = swap_bytes(data)
            da = array.array('L', data)
            ipa = array.array('L', ip)
            da[0] = da[0] ^ ipa[0]
            da[1] = da[1] ^ ipa[1]
            data = da.tostring()
            s += data[:length]
            ip = next_ip
            length -= 8

        if record_type == 1:
            uuid = array.array('B', s).tolist()
            s = '%02X%02X%02X%02X-%02X%02X-%02X%02X-%02X%02X-%02X%02X%02X%02X%02X%02X' % tuple(uuid)
        elif 2 <= record_type <= 6:
            s = s.decode('latin-1')

        if record_count >= 3 and 1 <= record_type <= 6:
            entry[record_types[record_type]] = s.rstrip('\0')
        elif record_type == 255:
            entries.append(entry)
            entry = {}

        record_count += 1

    f.close()

    return entries

def dump_entries(entries):
    for entry in entries:
        for name, value in entry.items():
            print '%s: %s' % (name, value.encode('ascii', 'replace'))
        print

if __name__ == '__main__':
    if len(sys.argv) < 2:
        sys.stderr.write('usage: %s path/to/file.dat\n' % sys.argv[0])
        sys.exit(1)

    path_to_file = sys.argv[1]

    sys.stderr.write('password: ')
    password = getpass.getpass('')
    sys.stderr.write('\n')

    entries = read_entries(path_to_file, password)
    dump_entries(entries)
