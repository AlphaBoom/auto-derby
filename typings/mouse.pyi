# -*- coding=UTF-8 -*-
# This typing file was generated by typing_from_help.py
"""
mouse

"""

from . import
from . import _os_mouse
import typing

"""
mouse
=====

Take full control of your mouse with this small Python library. Hook global events, register hotkeys, simulate mouse movement and clicks, and much more.

_Huge thanks to [Kirill Pavlov](http://kirillpavlov.com/) for donating the package name. If you are looking for the Cheddargetter.com client implementation, [`pip install mouse==0.5.0`](https://pypi.python.org/pypi/mouse/0.5.0)._

## Features

- Global event hook on all mice devices (captures events regardless of focus).
- **Listen** and **sends** mouse events.
- Works with **Windows** and **Linux** (requires sudo).
- **Pure Python**, no C modules to be compiled.
- **Zero dependencies**. Trivial to install and deploy, just copy the files.
- **Python 2 and 3**.
- Includes **high level API** (e.g. [record](#mouse.record) and [play](#mouse.play).
- Events automatically captured in separate thread, doesn't block main program.
- Tested and documented.

This program makes no attempt to hide itself, so don't use it for keyloggers.

## Usage

Install the [PyPI package](https://pypi.python.org/pypi/mouse/):

    $ sudo pip install mouse

or clone the repository (no installation required, source files are sufficient):

    $ git clone https://github.com/boppreh/mouse

Then check the [API docs](https://github.com/boppreh/mouse#api) to see what features are available.


## Known limitations:

- Events generated under Windows don't report device id (`event.device == None`). [#21](https://github.com/boppreh/keyboard/issues/21)
- To avoid depending on X the Linux parts reads raw device files (`/dev/input/input*`) but this requries root.
- Other applications, such as some games, may register hooks that swallow all key events. In this case `mouse` will be unable to report events.

"""


class ButtonEvent(builtins.tuple):
    """
    ButtonEvent(event_type, button, time)

    ButtonEvent(event_type, button, time)
    """

    _field_defaults: ...
    """
    """

    _fields: ... = ('event_type', 'button', 'time')
    """
    """

    _fields_defaults: ...
    """
    """

    @staticmethod
    def __new__(_cls, event_type, button, time):
        """
        Create new instance of ButtonEvent(event_type, button, time)
        """
        ...

    @classmethod
    def _make(cls, iterable):
        """
        Make a new ButtonEvent object from a sequence or iterable
        """
        ...

    def __getnewargs__(self):
        """
        Return self as a plain tuple.  Used by copy and pickle.
        """
        ...

    def __repr__(self):
        """
        Return a nicely formatted representation string
        """
        ...

    def _asdict(self):
        """
        Return a new dict which maps field names to their values.
        """
        ...

    def _replace(self, /, **kwds):
        """
        Return a new ButtonEvent object replacing specified fields with new values
        """
        ...

    ...


class MoveEvent(builtins.tuple):
    """
    MoveEvent(x, y, time)

    MoveEvent(x, y, time)
    """

    _field_defaults: ...
    """
    """

    _fields: ... = ('x', 'y', 'time')
    """
    """

    _fields_defaults: ...
    """
    """

    @staticmethod
    def __new__(_cls, x, y, time):
        """
        Create new instance of MoveEvent(x, y, time)
        """
        ...

    @classmethod
    def _make(cls, iterable):
        """
        Make a new MoveEvent object from a sequence or iterable
        """
        ...

    def __getnewargs__(self):
        """
        Return self as a plain tuple.  Used by copy and pickle.
        """
        ...

    def __repr__(self):
        """
        Return a nicely formatted representation string
        """
        ...

    def _asdict(self):
        """
        Return a new dict which maps field names to their values.
        """
        ...

    def _replace(self, /, **kwds):
        """
        Return a new MoveEvent object replacing specified fields with new values
        """
        ...

    ...


class WheelEvent(builtins.tuple):
    """
    WheelEvent(delta, time)

    WheelEvent(delta, time)
    """

    _field_defaults: ...
    """
    """

    _fields: ... = ('delta', 'time')
    """
    """

    _fields_defaults: ...
    """
    """

    @staticmethod
    def __new__(_cls, delta, time):
        """
        Create new instance of WheelEvent(delta, time)
        """
        ...

    @classmethod
    def _make(cls, iterable):
        """
        Make a new WheelEvent object from a sequence or iterable
        """
        ...

    def __getnewargs__(self):
        """
        Return self as a plain tuple.  Used by copy and pickle.
        """
        ...

    def __repr__(self):
        """
        Return a nicely formatted representation string
        """
        ...

    def _asdict(self):
        """
        Return a new dict which maps field names to their values.
        """
        ...

    def _replace(self, /, **kwds):
        """
        Return a new WheelEvent object replacing specified fields with new values
        """
        ...

    ...


_GenericListener = GenericListener


class _MouseListener(mouse._generic.GenericListener):
    def init(self):
        """
        """
        ...

    def listen(self):
        """
        """
        ...

    def pre_process_event(self, event):
        """
        """
        ...

    ...


def click(button: typing.Text = 'left') -> None:
    """
    Sends a click with the given button.
    """
    ...


def double_click(button: typing.Text = 'left') -> None:
    """
    Sends a double click with the given button.
    """
    ...


def drag(start_x: int, start_y: int, end_x: int, end_y: int, absolute: bool=True, duration: float=0) -> None:
    """
    Holds the left mouse button, moving from start to end position, then
    releases. `absolute` and `duration` are parameters regarding the mouse
    movement.
    """
    ...


def get_position():
    """
    Returns the (x, y) mouse position.
    """
    ...


hold = press


def hook(callback):
    """
    Installs a global listener on all available mouses, invoking `callback`
    each time it is moved, a key status changes or the wheel is spun. A mouse
    event is passed as argument, with type either `mouse.ButtonEvent`,
    `mouse.WheelEvent` or `mouse.MoveEvent`.

    Returns the given callback for easier development.
    """
    ...


def is_pressed(button: typing.Text = 'left') -> bool:
    """
    Returns True if the given button is currently pressed.
    """
    ...


def move(x: int, y: int, absolute: bool = True, duration: float = 0) -> None:
    """
    Moves the mouse. If `absolute`, to position (x, y), otherwise move relative
    to the current position. If `duration` is non-zero, animates the movement.
    """
    ...


def on_button(callback, args=(), buttons=('left', 'middle', 'right', 'x', 'x2'), types=('up', 'down', 'double')):
    """
    Invokes `callback` with `args` when the specified event happens.
    """
    ...


def on_click(callback, args=()):
    """
    Invokes `callback` with `args` when the left button is clicked.
    """
    ...


def on_double_click(callback, args=()):
    """
    Invokes `callback` with `args` when the left button is double clicked.
    """
    ...


def on_middle_click(callback, args=()):
    """
    Invokes `callback` with `args` when the middle button is clicked.
    """
    ...


def on_right_click(callback, args=()):
    """
    Invokes `callback` with `args` when the right button is clicked.
    """
    ...


def play(events, speed_factor=1.0, include_clicks=True, include_moves=True, include_wheel=True):
    """
    Plays a sequence of recorded events, maintaining the relative time
    intervals. If speed_factor is <= 0 then the actions are replayed as fast
    as the OS allows. Pairs well with `record()`.

    The parameters `include_*` define if events of that type should be inluded
    in the replay or ignored.
    """
    ...


def press(button: typing.Text = 'left') -> None:
    """
    Presses the given button (but doesn't release).
    """
    ...


def record(button='right', target_types=('down', )):
    """
    Records all mouse events until the user presses the given button.
    Then returns the list of events recorded. Pairs well with `play(events)`.

    Note: this is a blocking function.
    Note: for more details on the mouse hook and events see `hook`.
    """
    ...


def release(button: typing.Text = 'left') -> None:
    """
    Releases the given button.
    """
    ...


replay = play


def right_click():
    """
    Sends a right click with the given button.
    """
    ...


def unhook(callback):
    """
    Removes a previously installed hook.
    """
    ...


def unhook_all():
    """
    Removes all hooks registered by this application. Note this may include
    hooks installed by high level functions, such as `record`.
    """
    ...


def wait(button: typing.Text = 'left', target_types=('up', 'down', 'double')):
    """
    Blocks program execution until the given button performs an event.
    """
    ...


def wheel(delta: int =1) -> None:
    """
    Scrolls the wheel `delta` clicks. Sign indicates direction.
    """
    ...


DOUBLE: typing.Text
"""
'double'
"""

DOWN: typing.Text
"""
'down'
"""

LEFT: typing.Text
"""
'left'
"""

MIDDLE: typing.Text
"""
'middle'
"""

RIGHT: typing.Text
"""
'right'
"""

UP: typing.Text
"""
'up'
"""

X: typing.Text
"""
'x'
"""

X2: typing.Text
"""
'x2'
"""

__all__: ...
"""
['ButtonEvent', 'DOUBLE', 'DOWN', 'LEFT', 'MIDDLE', 'MoveEve...
"""

_listener: ...
"""
<mouse._MouseListener object>
"""

_pressed_events: ... = set()

version: typing.Text
"""
'0.7.1'
"""
