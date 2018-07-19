import RSA
import time as t
import random
import argparse


def run(args):
    if args.verbose:
        print("---- Generating {} bits key ----".format(args.key_size))

    start_time = t.time()
    public_key, private_key = RSA.generate_keys(args.key_size)
    time_passed = t.time() - start_time

    if args.verbose:
        print("---- Keys generated in {} ms ----".format(round(time_passed*1000, 5)))

    if args.verbose:
        print("---- Exporting keys to {} ----".format(args.output_dir))

    private_key.export_to(args.output_dir)
    public_key.export_to(args.output_dir)

    if args.verbose:
        print("---- Done ----")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument('-v', '--verbose', type=int, default=1)
    parser.add_argument('--output_dir', type=str, default='')
    parser.add_argument('--key_size', type=int, default=16)

    args = parser.parse_args()
    if args.key_size < 16:
        raise argparse.ArgumentTypeError(
            'Key size cannot be less than 16 bits.')

    random.seed(int(round(t.time())))
    run(args)
