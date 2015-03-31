# gdb-reattach-plugin
GDB command for reattaching to the new instance of the latest running process (it can help exploit development with pwntools for example).

## Usage
Load plugin (while running GDB or by adding to ~/.gdbinit):
```
source gdb-reattach.py
```
    
Reattach:
```
ra [processName]
```

Where processName is only required the first time (will be passed to the pidof command) then cached.
