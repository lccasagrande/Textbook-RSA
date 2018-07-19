import RSA
import argparse
import gmpy2
import time as t
import random


def run(args):
    def exec_pollard_rho(n):  # Find prime factor of n
        x = random.randrange(1, n, 2)
        i, k = 1, 2
        y = x
        while True:
            i += 1
            x2 = (gmpy2.square(x) - 1) % n
            p = gmpy2.gcd(y - x2, n)
            if (p != 1) and (p != n):
                break

            x = x2
            if i == k:
                y = x2
                k *= 2
        return p

    if args.verbose:
        print("---- Executing Pollard Rho algorithm ----")

    public_key = RSA.PublicKey.import_from(args.public_key)

    t_start = t.time()
    p = exec_pollard_rho(public_key.n)
    time_passed = t.time() - t_start

    if args.verbose:
        print("---- Key broken in {} ms ----".format(round(time_passed*1000, 5)))

    q = public_key.n // p  # n = p * q
    phi = (p - 1)*(q - 1)
    d = RSA.get_inv_mul(public_key.x, phi)
    private_key = RSA.PrivateKey(d, public_key.n)

    if args.verbose:
        print("---- Exporting private key to {}".format(args.output_dir))

    private_key.export_to(args.output_dir + "pollard_")

    if args.verbose:
        print("---- Done ----")

    return private_key


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', type=int, default=1)
    parser.add_argument('--public_key', type=str, default="public_key.der")
    parser.add_argument('--output_dir', type=str, default='')
    args = parser.parse_args()

    random.seed(int(round(t.time())))
    run(args)
