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

"""GUI for Minecraft LANBroadcaster using Tkinter and ttk"""

import textwrap

import tkinter as tk
from tkinter import ttk

import lan_broadcaster

__version__ = '0.1.2'

__all__ = ['MainWindow', 'center_window']


class MainWindow:
    """A simple GUI for LANBroadcaster using Tkinter."""

    about_text = textwrap.dedent("""\
    LANBroadcaster GUI {} (base: {})
    by minerz029

    Licensed under the GNU GPL v3 license viewable using the 'License' menu item.
    """.format(__version__, lan_broadcaster.__version__))

    network_icon_data = b'R0lGODlhQABAAOf/ADEKAycVBTYUByMbCjQXCTwYBxIkEDkaB0QbDkEdDhsoFT4fDjggFxYtF0UgEj0jEEQkFEEnGS4sIx4yGEgnF00mExQ2H0koEj0qJE0rFSo2HSI5Hk4tHEovIVUtGVEvGAZGJlQxGyk/Hkw1IFYzHQBMKkw2JVwzGVszHlo2IFY3JFc4IEw7IwRRL0o8M2E3I0BCP2A8JWc8IgRZMGU/IyJKhmFBKDxMK1hDNmZBKkZIRUxHRlhHKUZOKg1eNElNL0tKSChOimtFKHFFKh1dNXNFJjdPe2ZINmlILzBSfGpJKzBaLm1IMC5Tj09QTiRgMiZXkj5TdHJLLlFSUB5lNWFQQnhLMEVUcG5OOnRNNTJYjj9fL0VYblVXVFBdMHNSOHlRNGhXMktaa0dhMjdckyZrO4BRNlpbSFFcaEBnNX5VOFZdZDpqNzxgl1tdWoBWM11fXCpyP3RbSVJhcjdvO0ljiUBkm19hXoNaPGBiXzlyN4paOUFnmF9kZohdOmRlYzl3O09oj4hfQUZ0OmNnaVJxOUVrnIViQmZoZYxhPnplVFNsjUluoGZrbZBlQZVkQkZ8QGttakxxo21ubI9oS1x0lm9ydVZ1oZhrSEmFQXJ0cVp4pZ5tS1GFRl15moVzZHV3dFuFPlCJP0WMTV58qaZySnl7eHd8fmF/rXGAkn6Afax3T2qCq26Gr1qWUV2WTISGg2KWUmyNtWiZT4mLiHOXU22ZV4KOm2afVHKcU42PjI6Qk2+hVpCSj3ehWJSWk3qkW5yXlXaoXX2nXpial3yrWpKeq5yem3+vXZigqJ+hnny0YYOzYYa1Y6Smo4G4ZYq4X4W6YIC+Yom/Zayuq52wyY7EaaK1zpTHZrW3tKy908C6uba90r+8zb2/vMS9ycK/0MW/ysHDwLnE0sPFwsbIxcrMyMrO3c3QzM7P2c3R4dPV0srW5M3W3tXW4NbY1dnb2Nze297g3eDj3+fk6eTm4uXn5Ofp5unr6Ovu6vHu8+3w7PPx9fb7/v7//P///yH5BAEKAP8ALAAAAABAAEAAAAj+AP8JHEiwoMGDCBMqXMiwocOHECNKnEixosWLGDNq3Mixo8eGeeCIHEmypMmPCuE4m5dv3758MGPmw4fvnk2b87z9gYPyYJ5e+8oR+0W0qNFeSJM6k+eNZ8+CecTJu2MsmVWrxrJq3WrMUrZ4Tp8OhFNuXR5/7sKp5eevrdu3/m45uxdW7D+yZtmpO8eXnd+/gP2mmltXLF44rBKjWkyK1KZLkCVJZsRoDmG7Y8mtg7MYlePHkSVRNkTajmW6mAXCIYcOzmfIlyYzIs3Hju02XJShTg1HXGvYsmnXbkMcSpDc9Qo/7d1a9GhDte0Qb0PGeI0ayJX37G0ODmlDtqX+UydDpkmQ69ezp74rrjtx6eShGA9Cvz59LsTArucOB73/KGuYJCBJbuSBEhzelNOffzWI0Qc15qAjITrmVFhhORhmWI44zuRxh0cIKsigEXCskw86GmpIzorkiOOiOOXUoyCICcJhXxBXnLLPLnDk4eOPQAYZ0i73mKKdRQi+04dJveQTSTv6pCMlPXBVOQ4h++hyZEUIzoOON2CCqUqTjUApZTpUVvnWlVluSdEd2cizzpx0wkKmJ9r0o+eesni2CWiSBYKllg35Yk00zBSzUB6/zAPPO5BCamc+jVTCjTuYZtpKaM/VMaib/zDDDDDINFMMMsAAk0tCcGQzzzz+8sQqDy1kWhoOON90o2srz0Fnm6dtIlSML8w0g8ypxaoKjC+lHiRSHpNMEsm0P+HTyCLaVEmKr7e1oUUSnxoUzTSiHvrMssWIOg0ww4w7LEF3IPJLL7rUW+8kvdxz7TVVXtItGVqcB24+hA4UDTbM+CIMos80M+4wvvhSTC7AOOxLLr7Uolo5N3WsS777VinJeOahNzAtYWWCizC25JJLMcIUI/Mw0yA8zbqoLotMLD7chU48dNYJch3VVGmIeef5d3LKgEAyizTTDFOMqohKDXG6zAjDSydEgACCz/W8KvY8tOhyDyFJoFLN2mxDwaDJhOSD8kCFjCGKHoO4ssz+uIiyyy4zyPjCyyhllFBCCwr84wYt4rDIoipmo/325HDLHRYPZwySRg96ZPLKLMMwAw0ywtQyTCxl+DDDE08oYMADArkxoC71SE755En0YflAeGDBwxY9pMFGJ5A4Dbg1uFDRAgglzECFBgkQcAFBiGSDCAwCTUG77bczmPvuAklhAyZhrMCC3aIAQgcdrsQxQwsbKGBBAxZIwAEFQxA0iTiR6CBQF7SzBBrEQMACGvCAYkCDJfAxN4GsQgWCyAIectCDMYTCC3TQQxlaQIQWWCAAAxgAABhAgQykgCCgQIcmnBA72nmDXvaKoQzt1Qt01KOB/+AEEwShiC/EgAP+LPiBDW6QhiVYQAQTmAACBCCAEJwgAyEgAQrXAQoW3kUX81gHPGTFxS52MR7wwKEgwIAJSoABDGrIAQ6OoAQWjEACFAjBAy5QAQ+8QAgUOEAGpljF2GnCUUELpCDp9A54aCIsiQADE9SABzA4wg94QAIYUhADCsQgBh2ogAwqEIIPpAAFH+CjFe/iqi/G45SohIcqV/kOatQlEXhgAhPEhwQpYAIPakCjADJgAhxUAAJRzEARqhABgpgiG6qYwkDuAAdaKOOZ0FTGMaZJzWMQ45rEgIVICKIGJmCCEzGwARLwMEY1qGEPDkDBEFJwgQJAgARQJEEFBqIKWtgTFsv+vMMfEMHPfvrzn/38wx0+NBAm5AAPjniEI6RwRjAgQQ1+QIEMUrCABADTChkggAyssAMd5IEW3siiLkChgy6oYh4dS6lKUzoPVYTFnFLAAyb8IAdK4CERmLCBFEhwABJ4wAMqMMEHIJABGdBgG+WY5k28oQtvgMIZ9VilVKVqDhiVI0LrKGQ9nOGGgSQiB0wYZyKwcAhcYkIOk7zAEIYgAw5A4AUWJQEEguGMXhxjqbRCBFSnytdyeIMcV0VHVuGx1S4QBA+lkEIO/KBIKawAD4oQAjxjQAMhpKAAGWgiCTCwAyDcAaT1WIcuNAGDKZy0HqhNrWpXu9qWKrMgfsBnwhF0qsgzpiCOFKDABy6QgQxMzyD2tOdYBkTckyDkE29IYw4eUQozJMC3BIgAB2KwHoZEMqaOAEMGHCAEDrigug/Bgx/UIIWi0gC8EyGBFNHL3va6973wja9850vf+tr3vvjNL0QCAgA7'

    def __init__(self):

        self.broadcaster = lan_broadcaster.LANBroadcaster()
        self.shell = lan_broadcaster.BroadcasterShell(self.broadcaster)

        self._master_root = tk.Tk()
        self._master_root.withdraw()

        self.root = tk.Toplevel(self._master_root)
        self.root.withdraw()
        self.root.title("LANBroadcaster")

        self.network_icon = tk.PhotoImage(data=self.network_icon_data)

        self.label_image = ttk.Label(self.root, image=self.network_icon)
        self.label_image.grid(row=0, column=0, columnspan=1)

        self.root.wm_iconphoto(True, self.network_icon)

        self.frame = ttk.Frame(self.root, name="entry_frame")

        self.header = ttk.Label(
            self.frame,
            text="LANBroadcaster {} by minerz029".format(__version__)
        )
        self.header.grid(row=0, columnspan=2)

        ### MOTD INPUT ###
        self.label_motd = ttk.Label(self.frame, text="MOTD: ")
        self.label_motd.grid(column=0, row=1, sticky='e')

        self.v_cmd = (self.root.register(self.update_attributes), '%P', '%W')
        self.entry_motd = ttk.Entry(self.frame, name="entry_motd",
                                    validate='key', validatecommand=self.v_cmd)
        self.entry_motd.bind('<FocusIn>',
                             lambda _: _.widget.selection_range(0, 'end'))
        self.entry_motd.bind('<Return>', lambda _: self.ok_button.invoke())
        self.entry_motd.grid(column=1, row=1, pady=(5, 0))
        self.entry_motd.focus_set()

        ### ADDRESS INPUT ###
        self.label_address = ttk.Label(self.frame, text="Address: ")
        self.label_address.grid(column=0, row=2, sticky='e')

        self.entry_address = ttk.Entry(self.frame, name="entry_address",
                                       validate='key',
                                       validatecommand=self.v_cmd)
        self.entry_address.bind('<FocusIn>',
                                lambda _: _.widget.selection_range(0, 'end'))
        self.entry_address.bind('<Return>', lambda _: self.ok_button.invoke())
        self.entry_address.grid(column=1, row=2, pady=(5, 0))

        self.ok_button = ttk.Button(
            self.frame,
            text="Start",
            width=20,
            default='active',
            command=self._toggle_broadcasting
        )
        self.ok_button.bind('<Return>', lambda _: self.ok_button.invoke())
        self.ok_button.grid(column=0, row=3, pady=(6, 0), padx=5, columnspan=2,
                            sticky='we')

        self.frame.grid(row=0, column=1, padx=10, pady=(5, 0), sticky='w',
                        columnspan=4)

        ### ===== OUTPUT TEXT ===== ###

        self.text_frame = tk.Frame(self.root)

        self.text_label = ttk.Label(self.text_frame,
                                    text="Command output, most recent first:",
                                    justify='left')
        self.text_label.grid(row=0, pady=(5, 0), sticky='e')

        self.clear_button = ttk.Button(
            self.text_frame,
            text="Clear",
            command=lambda: self.update_text(clear=True, ruler='', end='')
        )
        self.clear_button.grid(row=0, column=1, pady=5)

        self.text_scrollbar_y = ttk.Scrollbar(self.text_frame,
                                              orient='vertical')

        self.output_text = tk.Text(self.text_frame, height=20, state='normal',
                                   yscrollcommand=self.text_scrollbar_y.set,
                                   borderwidth=5, relief='flat')
        self.output_text.bind('<Key>', lambda _: 'break')
        self.output_text.bind('<Button-2>', lambda _: 'break')
        self.output_text.disabled_ = True
        self.text_scrollbar_y.config(command=self.output_text.yview)
        self.text_scrollbar_y.grid(row=1, column=3, sticky='ns')
        self.output_text.grid(row=1, column=0, columnspan=2)

        self.text_frame.grid(padx=5, pady=5, columnspan=5)

        ### ===== MENU BAR ===== ###

        self.menu_bar = tk.Menu(self.root)

        self.op_menu = tk.Menu(self.root, tearoff=False)
        self.op_menu.add_command(
            label="Show status",
            command=lambda: self.update_text(
                self.broadcaster.get_status())
        )
        self.op_menu.add_command(label="Broadcast once",
                                 command=self.broadcast_once)
        self.op_menu.add_separator()
        self.op_menu.add_command(label="Quit",
                                 command=self._master_root.destroy)
        self.menu_bar.add_cascade(label="Broadcaster", menu=self.op_menu)

        self.help_menu = tk.Menu(self.root, tearoff=False)
        self.help_menu.add_command(
            label="Show license",
            command=lambda: self.update_text(self.shell.gpl_license),
        )
        self.help_menu.add_command(
            label="About",
            command=lambda: self.update_text(self.about_text),
        )
        self.menu_bar.add_cascade(label="Help", menu=self.help_menu)

        self.root.config(menu=self.menu_bar)

        ### ===== STATUS BAR ===== ###

        self.status_text = tk.StringVar(self.root, value="Status: Stopped")
        self.status_bar = ttk.Label(self.root, textvariable=self.status_text)
        self.status_bar.grid(columnspan=10, pady=(0, 5), padx=5, sticky='w')

        ### ===== ROOT BINDS/PROTOCOLS ===== ###

        self.root.protocol('WM_DELETE_WINDOW', self._master_root.destroy)

        ### ===== STUFF ===== ###

        for widget in (self.entry_motd, self.entry_address, self.output_text):
            self.bind_shortcuts(widget)

    def do_mainloop(self):
        """Centers the window then runs the do_mainloop()."""

        center_window(self.root)
        self.root.deiconify()
        center_window(self.root)
        self.update_text(self.about_text)
        self.root.mainloop()
        if self.broadcaster.is_alive():
            self.broadcaster.stop()

    def _toggle_broadcasting(self):
        """Toggles broadcasting on or off. Used as a click event for
        the Button."""
        text = ""
        if not self.broadcaster.is_alive():
            self.broadcaster.motd = self.entry_motd.get()
            self.broadcaster.address = self.entry_address.get()
            try:
                self.broadcaster.start()
            except RuntimeError as exc:
                text = "\n".join(exc.args) + text
            else:
                text += "Started broadcasting."
                self.set_status_text("Broadcasting...")
                self.ok_button.config(text="Stop")
        else:
            self.set_status_text("Stopping...")
            self.ok_button.config(text="Stopping...")
            self.ok_button.update()
            self.status_bar.update()

            self.broadcaster.stop()
            text += "Stopped broadcasting."
            self.ok_button.config(text="Start")
            self.set_status_text("Stopped")
        text += "\n"*2 + self.broadcaster.get_status()
        self.update_text(text)

    def broadcast_once(self):
        """Runs the :func:`self.broadcaster.broadcast_message` function of the
         broadcaster attribute. Updates the text to reflect success or errror.

         """
        try:
            self.broadcaster.broadcast_message()
        except RuntimeError as exc:
            text = "\n".join(exc.args)
        else:
            text = "Broadcasted server message once"
        self.update_text(text)

    def update_text(self, *commands, clear=False, end="\n\n", ruler='-'):
        """Updates the output text field with the output of the arguments.

        :param commands: Commands to run and add to the output text
        :type commands: tuple of functions
        :param clear: True if the text field should be cleared
        :type clear: bool
        :param end: The string to print after `commands` have been run
        :type end: str
        :param ruler: Character to use as a line
        :type ruler: str

        """
        if clear:
            self.output_text.delete('0.0', 'end')
        if end or ruler:
            inserted_text = False
            for cmd in commands:
                if callable(cmd):
                    ret = cmd()
                else:
                    ret = cmd
                ret = ret.strip('\r\n\t ')
                if ret:
                    self.output_text.insert('insert', str(ret))
                    inserted_text = True
            if inserted_text:
                self.output_text.insert('insert', "\n")
                self.output_text.insert('insert',
                                        ruler*self.output_text.cget('width'))
                self.output_text.insert('insert', end)
                self.output_text.mark_set('insert', '0.0')
                if int(self.output_text.index('end-1c').split('.')[0]) > 175:
                    self.output_text.delete('175.0', 'end')

    def update_attributes(self, text, widget):
        """Updates the broadcaster with the new text.
        Used as a validate command for the MOTD and address Entry fields.

        :param text: Text to set
        :type text: str
        :param widget: Widget which was changed
        :type widget: str

        """

        if widget.endswith('.entry_motd'):
            self.broadcaster.motd = text
        else:
            self.broadcaster.address = text
        return True

    def set_status_text(self, text=None):
        """Sets the status bar text to `text`.

        :param text: New value for the status bar text
        :type text: str

        """
        if text is not None:
            self.status_text.set("Status: " + str(text))
        else:
            return self.status_text.get()[len('Status: '):]

    get_status_text = set_status_text

    def bind_shortcuts(self, widget):
        """Binds the *standard* keyboard shortcuts (e.g.: copy, paste, select
        all) to :param:`widget`.

        :param widget: The widget to bind to
        :type widget: tk.Entry or tk.Text

        """

        keyboard_shortcuts = {
            '<Control-c>': self.clipboard_copy,
            '<Control-v>': self.clipboard_paste,
            '<Control-x>': self.clipboard_cut,
            '<Control-a>': self.select_all,
        }

        for shortcut in keyboard_shortcuts:
            widget.bind(shortcut, keyboard_shortcuts[shortcut])

    def clipboard_copy(self, event):
        """Copies the selected text to the clipboard.

        :param event: Event which triggered the function.

        """

        self._master_root.clipboard_clear()
        self._master_root.clipboard_append(event.widget.selection_get())

    def clipboard_paste(self, event):
        """Pastes the clipboard into the widget.

        :param event: Event which triggered the function.

        """
        if ((not hasattr(event.widget, 'disabled_')) or
                (not getattr(event.widget, 'disabled_', False))):
            text = self._master_root.clipboard_get()
            # i = len(text)/2-1
            # if i % 1 != 0:
            #     i -= 0.5
            event.widget.insert('insert', text)
        return 'break'

    def clipboard_cut(self, event):
        """Copies the selected text then deletes it.

        :param event: Event which triggered the function.

        """

        self.clipboard_copy(event)
        event.widget.delete('sel.first', 'sel.last')

    @staticmethod
    def select_all(event):
        """Selects all of the text in the widget.

        :param event: Event which triggered the function.

        """

        try:
            event.widget.selection_range('0', 'end')
        except AttributeError:
            event.widget.tag_add("sel", "0.0", "end")
        return 'break'

    ### FILE LIKE OBJECTS ###

    def write(self, line):
        self.update_text(line)

    def close(self):
        pass

    def flush(self):
        pass


def center_window(_root):
    """Centers the window `_root`.

    :param _root: The window to center.
    :type _root: tk.Tk or tk.Toplevel
    """
    _root.lift()
    _root.update()
    _root.update_idletasks()
    w = _root.winfo_screenwidth()
    h = _root.winfo_screenheight()
    _rootsize = tuple(int(_) for _ in _root.geometry().split('+')[0].split('x'))
    x = w/2 - _rootsize[0]/2
    y = h/2 - _rootsize[1]/2
    _root.geometry("+%d+%d" % (x, y))


if __name__ == '__main__':
    main = MainWindow()
    main.do_mainloop()
