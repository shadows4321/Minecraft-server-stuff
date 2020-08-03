#!/usr/bin/env python3

# This file is part of LANBroadcaster.
#
# LANBroadcaster is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# LANBroadcaster is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with LANBroadcaster.  If not, see <http://www.gnu.org/licenses/>.

"""Minecraft LAN Broadcaster base and command line prompt.

This program is capable of broadcasting any Minecraft server as a LAN world.

It supports an interactive prompt to configure the broadcaster while it is
running and also supports command line arguments, running in the background
(non-interactively) and running silently (no output).

"""

import argparse
import cmd
import os
import shlex
import socket
import sys
import textwrap
import threading
import time


__version__ = '0.1.3'

__all__ = ['LANBroadcaster', 'BroadcasterShell']


class LANBroadcaster():
    """Announces any Minecraft server over the local LAN network."""

    send_address = '224.0.2.60'  #: Address to send to
    send_port = 4445  #: Port to send to

    def __init__(self, motd='', address=''):
        """Initializes the LANBroadcaster class.
        Sets the motd, address, and creates the socket and thread.

        :param motd: Server message of the day
        :type motd: str
        :param address: Server address
        :type address: str

        """
        self._motd = motd
        self._address = address
        self._stop = threading.Event()
        self._stop.set()

        self.sock = socket.socket(type=socket.SOCK_DGRAM)  # UDP

        self.thread = threading.Thread(target=self.broadcast_loop,
                                       name="Broadcaster")

    @property
    def motd(self):
        """Returns or sets the _motd attribute."""
        return self._motd

    @motd.setter
    def motd(self, value):
        """Sets the _motd attribute with stripped whitespace.

        :param value: The value to set _motd to
        :type value: str

        """
        self._motd = str(value).strip()

    @property
    def address(self):
        """Returns or sets the _address attribute."""
        return self._address

    @address.setter
    def address(self, value):
        """Sets the _address attribute with stripped whitespace.

        :param value: The value to set _address to
        :type value: str

        """
        self._address = str(value).strip()

    def broadcast_message(self):
        """Formats and broadcasts the message to 224.0.2.60:4445.

        :raises RuntimeError:"""

        if self.motd and self.address:
            self.sock.sendto(
                ("[MOTD]" + self.motd + "[/MOTD][AD]" +
                 self.address + "[/AD]").encode(),
                (self.send_address, self.send_port)
            )
        else:
            raise RuntimeError(
                "{0}.motd and {0}.address must be non zero length "
                "strings".format(
                    self.__class__.__qualname__)
            )

    def broadcast_loop(self, sleep=3):
        """Loops every `sleep` seconds and broadcasts message.
        Stops if _stop is set.

        :param sleep: Time in seconds to sleep between messages
        :type sleep: int or float

        """

        try:
            while not self._stop.is_set():
                self.broadcast_message()
                time.sleep(sleep)
        except KeyboardInterrupt:
            return

    def start(self):
        """Starts the broadcast_loop thread.

        :raises RuntimeError: if motd and address are zero-length
        :raises RuntimeError: if the broadcaster is already running

        """

        if not self.is_alive():
            if self.motd and self.address:
                self.thread = threading.Thread(target=self.broadcast_loop,
                                               name="Broadcaster")
                self._stop.clear()
                self.thread.start()
            else:
                raise RuntimeError(
                    "{0}.motd and {0}.address must be non zero length "
                    "strings".format(
                        self.__class__.__qualname__)
                )
        else:
            raise RuntimeError("Broadcaster is already running.")

    def stop(self):
        """Stops the broadcast_loop thread and waits for it to finish."""
        self._stop.set()
        if self.is_alive():
            self.thread.join()

    def is_alive(self):
        """Returns True if broadcasting, False otherwise."""

        return self.thread.is_alive()

    def ask_for_input(self, ask_motd=True, ask_add=True):
        """Asks the user for input on the broadcaster MOTD and address fields.

        :param ask_motd: True if the MOTD should be asked
        :type ask_motd: bool
        :param ask_add: True if the address should be asked
        :type ask_add: bool

        """

        if ask_motd:
            motd = ''
            while not motd:
                motd = input("Enter MOTD to broadcast: ").strip()
            if motd in ('quit', 'exit'):
                return
            self.motd = motd

        if ask_add:
            address = ''
            while not address:
                address = input("Enter address to broadcast: ").strip()
            if address in ('quit', 'exit'):
                return
            self.address = address

    def get_status(self):
        """Returns the current status of the broadcaster.

        :return: Status message of current broadcaster state
        :rtype: str

        """

        return "\n".join((
            ("NOT b" if not self.is_alive() else "B") + "roadcasting:",
            "    MOTD: " + self.motd,
            "    Address: " + self.address
        ))


class BroadcasterShell(cmd.Cmd):
    """A simple shell to interact with a `LANBroadcaster` instance.

    :param broadcaster_: The instance of LANBroadcaster to work with
    :type broadcaster_: LANBroadcaster

    """
    intro = "Welcome to LANBroadcaster. Type help to list commands."
    prompt = "> "

    gpl_license = textwrap.dedent(
        """\
        LANBroadcaster: Broadcast any Minecraft server as a LAN world.
        Copyright (C) 2013  minerz029

        This program is free software: you can redistribute it and/or modify
        it under the terms of the GNU General Public License as published by
        the Free Software Foundation, either version 3 of the License, or
        (at your option) any later version.

        This program is distributed in the hope that it will be useful,
        but WITHOUT ANY WARRANTY; without even the implied warranty of
        MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
        GNU General Public License for more details.

        You should have received a copy of the GNU General Public License
        along with this program.  If not, see <http://www.gnu.org/licenses/>
        """.rstrip('\r\n')
    )

    def __init__(self, broadcaster_, completekey='tab', stdin=None,
                 stdout=None):
        """Create a new BroadcasterShell."""
        super().__init__(completekey=completekey, stdin=stdin, stdout=stdout)
        self.broadcaster = broadcaster_

    def do_start(self, _args):
        """START: Starts the broadcaster."""
        try:
            self.broadcaster.start()
            self.stdout.write("Started the broadcaster.\n")
        except RuntimeError as _exc:
            self.stdout.write(", ".join(_exc.args) + "\n")

    def do_stop(self, args):
        """STOP: Stops broadcast of the server."""
        try:
            self.stdout.write("Stopping...")
            self.stdout.flush()
            self.broadcaster.stop()
            self.stdout.write("\rStopped the broadcaster.\n")
        except RuntimeError as exc:
            self.stdout.write(", ".join(exc.args) + "\n")

    def do_send(self, args):
        """SEND: Broadcasts the server *once*."""
        self.broadcaster.broadcast_message()
        self.stdout.write("Sent server message once.\n")

    def do_status(self, args):
        """STATUS: Prints the current status of the broadcaster."""
        self.stdout.write(self.broadcaster.get_status() + "\n")

    def do_config(self, arg):
        """CONFIG: Reconfigures the MOTD and address of the broadcaster.

        CONFIG [MOTD] [address]

        Allows the MOTD and/or address to be specified as arguments.

        """

        if not arg:
            self.broadcaster.ask_for_input()
        else:
            args = shlex.split(arg)
            try:
                self.broadcaster.motd = args[0]
                self.stdout.write("Set MOTD to " + broadcaster.motd + "\n")
                self.broadcaster.address = args[1]
                self.stdout.write("Set address to", broadcaster.address)
            except IndexError:
                return

    def do_about(self, args):
        """ABOUT: Shows information about the program."""
        self.stdout.write(textwrap.dedent(
            """\
            {prog} {v}
            by minerz029

            Licensed under the GNU GPL v3 license viewable with
            the `license` command.\
            \n""".format(prog=os.path.basename(sys.argv[0]), v=__version__)
        ))

    def do_license(self, args):
        """LICENSE: Prints the GNU GPL v3 license details."""
        self.stdout.write(self.gpl_license + "\n")

    @staticmethod
    def do_exit(args):
        """EXIT: Quits the program, stopping the broadcaster."""
        return True

    do_quit = do_exit

    def precmd(self, line):
        """Converts line to lowercase.

        :param line: The command line to convert to lowercase
        :type line: str

        """
        if line == 'EOF':
            raise EOFError
        else:
            return line.lower()

    def postloop(self):
        """Stops the broadcaster."""
        self.broadcaster.stop()

### __MAIN__ ###

if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description=__doc__
    )

    arg_motd = parser.add_argument('motd',
                                   metavar="MOTD",
                                   nargs='?',
                                   default='',
                                   help="MOTD to use for the server")

    arg_address = parser.add_argument(
        'address',
        metavar="address",
        nargs='?',
        default='',
        help="Address with port (or port only for 1.6+) of the server"
    )

    parser.add_argument('-b', '--background', action='store_true',
                        help="run in non-interactive mode without a prompt")

    parser.add_argument('-s', '--silent', action='store_true',
                        help=("run silently (no output is printed). "
                              "Implies -b"))

    parser.add_argument('--no-start', action='store_true',
                        help="prevents from automatically starting "
                             "broadcasting.")

    version_text = textwrap.dedent(
        """\
        %(prog)s {v}
        by minerz029\
        """.format(v=__version__)
    )

    parser.add_argument('--version', action='version',
                        version=version_text)
    cl_args = parser.parse_args()

    broadcaster = LANBroadcaster(cl_args.motd, cl_args.address)

    if cl_args.silent:
        sys.stdin = open(os.devnull)
        sys.stdout = open(os.devnull, 'w')
        cl_args.background = True
    if cl_args.background:
        sys.stdin = open(os.devnull)

    if not (cl_args.motd and cl_args.address):
        if not cl_args.background:
            broadcaster.ask_for_input(ask_motd=not cl_args.motd,
                                      ask_add=not cl_args.address)
        else:
            parser.error(
                "MOTD and address are required with -s or -b"
            )

    if not cl_args.no_start:
        broadcaster.start()

    try:
        print(broadcaster.get_status())

        if not cl_args.background:
            shell = BroadcasterShell(broadcaster)
            shell.cmdloop()
        else:
            print("Running in non-interactive mode. Ctrl+C to exit.")
            while True:
                try:
                    input()
                except EOFError:
                    try:
                        time.sleep(time.time())
                    except (KeyboardInterrupt, SystemExit) as exc:
                        raise exc from None
    finally:
        broadcaster.stop()
    sys.exit()
