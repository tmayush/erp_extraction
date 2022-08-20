# CBIT ERP Data Extraction Tool \[Unofficial]

## Setup for Windows

### Requirements

- Python 3.6+
- Git (VCS)

You can check if you have the above tools installed or not by opening command prompt and executing the following commands

```cmd
python --version
git --version
```

### Steps to install

Create a directory to clone the project. for example let's call our directory "erp extraction". You can create the directory in any location you prefer.

OR

You can open the command prompt and type in the following commands

```cmd
mkdir "erp extraction"
```

Move into the directory

```cmd
cd "erp extraction"
```

Clone the repo

```cmd
git clone https://github.com/tmayush/erp_extraction.git
```

Create a virtual environment (in our case, we will call it "cbit-erp-venv")

```cmd
python -m venv cbit-erp-venv
```

Let's activate the environment

```cmd
cbit-erp-venv\Scripts\activate
```

Let's change directory and install the required packages to run the app

```cmd
cd erp_extraction
pip install -r requirements.txt
```

We can now run the app!

```cmd
python -m erp_extraction
```

---

## Notice of Non-Affiliation and Disclaimer

We are not affiliated, associated, authorized, endorsed by, or in any way officially connected with CHAITANYA BHARATHI INSTITUTE OF TECHNOLOGY (CBIT), or any of its subsidiaries or its affiliates. The official CBIT website can be found at https://www.cbit.ac.in/.

The names CHAITANYA BHARATHI INSTITUTE OF TECHNOLOGY as well as related names, marks, emblems and images are registered trademarks of their respective owners.
