import RSA
import time as t
import random
import argparse


def run(args):
    if args.verbose:
        print("---- Importing {} ----".format(args.key))

    public_key = RSA.PublicKey.import_from(args.key)

    if args.verbose:
        print("---- Encrypting file {} ----".format(args.file))

    start_time = t.time()

    public_key.encrypt_file(args.file)

    time_passed = round(t.time() - start_time, 2)

    if args.verbose:
        print("---- Done in {} ms ----".format(round(time_passed*1000, 5)))

    return time_passed


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-v', '--verbose', type=int, default=1)
    parser.add_argument('--key', type=str, default="public_key.der")
    parser.add_argument('--file', type=str, default="text.txt")

    random.seed(int(round(t.time())))
    args = parser.parse_args()
    run(args)
