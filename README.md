# gdb-reattach-plugin
GDB command for reattaching to the new instance of the process (help exploit development)

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
