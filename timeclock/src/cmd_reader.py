import sys

def reader():
    cmd = sys.argv[1]
    options = {k: v for k, v in zip(sys.argv[2::2], sys.argv[3::2])}
    return cmd, options