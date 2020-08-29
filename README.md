# CMa Visualization

This project aims to provide a user-friendly visualization for TUM's CMa virtual machine. It's built on a Jupyter notebook students can use to see what their CMa code does.

## Usage

You can use the included [`Dockerfile`](Dockerfile) to build a Jupyter image from this repository:

```bash
# build the jupyter image
$ make image

# run the jupyter server on port 8888
$ make run

# remove the built image when you don't need it anymore
$ make clean
```

Notebooks created on the Jupyter instance are stored in the `notebooks` folder in this repository.

Once Jupyter starts up, you can create new notebooks on [localhost:8888](http://localhost:8888). You can run code in the virtual machine by supplying it to `VM`'s constructor and stepping through it. We overwrote `VM`'s Jupyter representation, so this snippet will print a visualization:

```python
from cma.vm import VM

# create a virtual machine with a "10 + 20" program
vm = VM("""
  loadc 10
  loadc 20
  add
  halt
""")

# step through the program
vm.step()
vm.step()

# show the vm state; don't use print or similar, as this
# implicitly calls Jupyter's rendering function
vm
```

If you run into permission errors when creating a new notebook, try changing the `notebooks` directory's permissions using:

```bash
$ chmod 777 notebooks/
```

## Supported instructions

-   [x] add
-   [x] and
-   [x] alloc
-   [x] call
-   [x] div
-   [x] dup
-   [x] enter
-   [x] eq
-   [x] geq
-   [x] gr
-   [x] halt
-   [x] jump
-   [x] jumpz
-   [x] jumpi
-   [x] leq
-   [x] le
-   [x] load
-   [x] loada
-   [x] loadc
-   [x] loadr
-   [x] loadrc
-   [x] mark
-   [x] mul
-   [x] neg
-   [x] neq
-   [x] not
-   [x] new
-   [x] or
-   [x] pop
-   [x] return
-   [x] slide
-   [x] store
-   [x] storea
-   [x] storer
-   [x] sub
