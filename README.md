# CMa Visualization

This project aims to provide a user-friendly visualization for TUM's CMa virtual machine. It's built on a Jupyter notebook students can use to see what their CMa code does.

## Usage

You can use the included [`Dockerfile`](Dockerfile) to build a Jupyter image from this repository:

```bash
# build the jupyter image
$ make image

# run the jupyter server on port 8888
$ make run

# remove the built image
$ make clean
```

Notebooks created on the Jupyter instance are stored in the `notebooks` folder in this repository.
