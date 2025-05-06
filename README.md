# Activate All your PIMs
Activate all PIMs using Python

### Pre-Requiste
- Python 3.1x [this was developed using 3.13]
- install az cli - https://learn.microsoft.com/en-us/cli/azure/install-azure-cli-windows?pivots=msi
  - run `az login` and successfully login to your subscription.

#### Version 2.0 (Current Version) - 5/5/2025:
- Steps to run it locally
  - Clone the repo
  - Run `cd PIM_Activate_Python` until you are in the folder where `setup.py`.
  - Create a virtual environment (recommended)
    - for creating a virutal environment - `python -m venv .venv`
    - Activate the virtual environment (Windows) - `.venv\Scripts\activate`
  - run `pip install .`
  - To activate all your PIMS run either
    - `activate_pims -b 10 -j "your justification"`
    - `activate_pims --batch-size 10 --justification "your justification"` 
  - if you want to uninstall the pim_activation: `pip uninstall pim_activation -y`

#### Available Options:
- `-b, --batch-size`: Number of roles to activate in parallel (default: 10)
- `-j, --justification`: Justification for role activation
- `-v, --verbose`: Enable verbose output
- `-dur, --duration`: Duration in minutes (default: 480)
- `-mr, --max_retries`: Max retries on failure (default: 5)
- `-rd, --retry-delay`: Delay between retries in seconds (default: 2)
- `-d, --delay`: Delay between batches in seconds (default: 0.25)

### Upcoming updates:

- Will come up with the timing diff from the powershell script vs this solution.
- Will add it to pypi so that it can be installed from there
- Will add alias so that you can run the command from anywhere - <img src="https://cdn.jsdelivr.net/gh/Readme-Workflows/Readme-Icons@main/icons/octicons/ApprovedChanges.svg" alt="Simple Icons" height="16" width="20">:
- Will add more cli options on `starts-with` and `contains` which will activate only the ones that satisfy the conditions.

----

### Previous Versions:

#### Version 1 (5/5/2025):
- Steps to run it locally
  - Clone the repo
  - Run `cd PIM_Activate_Python`
  - Create a virtual environment (recommended)
    - for creating a virutal environment - `python -m venv .venv`
    - Activate the virtual environment (Windows) - `.venv\Scripts\activate`
  - Run `python install -r requirements.txt`
  - To Activate all your PIMs run either
    - `python activatePIMs.py -b 10 -j "your justification"`
    - `python activatePIMS.py --batch-size 10 --justification "your justification"`
  
### Notes:
- When tried with no delay between the calls - we are getting 429. Hence, the introduction of the delay and 0.25 seems to be working.
- Recent run with a batch size of 25 for 267 roles -> 282 seconds or 4.7 mins
- I have been running with a batch size of 20 - seems to be working fine -will attempt with higher number and update here.