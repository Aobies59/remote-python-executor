# Remote Python Executor

Made to execute code in a Rasberry Pi from a remote computer.
In the executing computer, just run:

```bash
python ./execute.py
```

And in the computer with the code, run:

```bash
python ./send.py <IP> <code>
```

Where `<IP>` is the IP of the computer that will execute the code and `<code>` is the python file with the code to be executed
