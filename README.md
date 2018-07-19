## Overview
This repository contains a Python implementation of Textbook RSA using Miller-Rabin primality test.

If you don't know how RSA works, take a look at this book: [CORMEN, Thomas H. et al. Introduction to algorithms. MIT press, 2009.](https://www.google.com/aclk?sa=L&ai=DChcSEwjfpuzMnarcAhVLWoYKHRGlCS4YABADGgJ2dQ&sig=AOD64_0f4syknDblF1b5gIop7EP6XBzExw&ctype=5&q=&ved=0ahUKEwjk--fMnarcAhXqzVkKHaodAkwQ9aACCDU&adurl=)

## Requirements
You'll need Python 3.x x64 to be able to run theses projects.

If you do not have Python installed yet, it is recommended that you install the [Anaconda](https://www.anaconda.com/download/) distribution of Python, which has almost all packages required in these project.

You can also install Python 3.x x64 from [here](https://www.python.org/downloads/)

## Instructions
1. Clone the repository and navigate to the downloaded folder.
    ```bash
    git clone https://github.com/lccasagrande/Textbook-RSA.git
    cd Textbook-RSA
    ```

2. Install required packages:
	```bash
	pip install -e .
	```
    Or:
	```bash
	pip install -e . --user
	```

3. Navigate to the src folder:
    ```bash
    cd src
    ```

4. Generate Keys:
    ```bash
    python keygen.py -v 1 --output_dir "../test/" --key_size 2048
    ```

5. Encrypt file
    ```bash
    python encrypt.py -v 1 --key "../test/public_key.der" --file "../test/text.txt"
    ```
6. Decrypt File
    ```bash
    python decrypt.py -v 1 --key "../test/private_key.der" --file "../test/text.txt"
    ```
7. Optional:
    It's possible to use the Pollard's Rho algorithm to break the RSA key. Do not use it with large key sizes, 32 bits should be a good first try.
    - Generate key with 32 bits:
    ```bash
    python keygen.py -v 1 --output_dir "../test/" --key_size 32
    ```
    - Encrypt file
    ```bash
    python encrypt.py -v 1 --key "../test/public_key.der" --file "../test/text.txt"
    ```
    - Run Pollard's Rho
    ```bash
    python pollard_rho.py -v 1 --public_key "../test/public_key.der" --output_dir "../test/"
    ```
    - Decrypt file
    ```bash
    python decrypt.py -v 1 --key "../test/pollard_private_key.der" --file "../test/text.txt"
    ```