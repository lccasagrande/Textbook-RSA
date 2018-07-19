import RSA
import time as t
import random
import argparse


def run(args):
    random.seed(int(round(t.time())))

    if args.verbose:
        print("---- Importing {} ----".format(args.key))

    private_key = RSA.PrivateKey.import_from(args.key)

    if args.verbose:
        print("---- Decrypting file {} ----".format(args.file))

    start_time = t.time()

    private_key.decrypt_file(args.file)

    time_passed = round(t.time() - start_time, 2)

    if args.verbose:
        print("---- Done in {} s ----".format(time_passed))

    return time_passed


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', type=int, default=1)
    parser.add_argument('--key', type=str, default="private_key.der")
    parser.add_argument('--file', type=str, default="text.txt")
    args = parser.parse_args()

    run(args)
