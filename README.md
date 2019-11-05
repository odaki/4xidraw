# 4xiDraw

The 4xiDraw Extensions for Inkscape - Software to drive the 4xiDraw drawing machine.

More about 4xiDraw:  https://www.instructables.com/id/4xiDraw/

---------


Install as you would any other Inkscape extension.

I use the following GRBL setup:

```
$100=100.000
$101=100.000
$110=5000.000
$111=5000.000
$120=1000.000
$121=1000.000
$130=200.000
$131=200.000
$132=200.000
$N0=M3S90
```


---------

## Dependencies

This extensions requires some python modules and and Inkscape extensions to be installed.

### Python Modules

- [lxml](https://lxml.de/)
- [Pyserial](https://pypi.python.org/pypi/pyserial). (Note that an older version, 2.7, must be used on Windows.)

### Inkscape Extensions

To install a new extension, download and unpack the archive file. Copy the files into the directory listed at Edit > Preferences > System: User extensions. Be sure to copy the `*.py`, `*.pyc` and `*.inx` files from `inkscape driver` directly to this folder. After a restart of Inkscape, the new extension will be available.

1. [plotink](https://github.com/evil-mad/plotink) helper routines for Inkscape extensions.
2. eggbot_hatch.py from the [EggBot extensions for Inkscape](https://github.com/evil-mad/EggBot/).

---------

## Known issues:

- There is apparently a rounding error somewhere, so the start and end of a drawing does not always line up.
- The speed is lower than it should be.

### No module named lxml

Try to install the python2 version of the module to resolve this issue. See [this issue](https://github.com/NixOS/nixpkgs/issues/31800) for more detailed information.

### No module named serial

Again, make sure to install the python2 version.


---------

This is based on the AxiDraw inkscape plugin, https://github.com/evil-mad/AxiDraw/
