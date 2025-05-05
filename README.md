# Activate All your PIMs
Activate all PIMs using Python

Version 1 (5/5/2025):
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


Upcoming updates:

- Will come up with the timing diff from the powershell script vs this solution.
- Will add alias so that you can run the command from anywhere.
- Will add more cli options on `starts-with` and `contains` which will activate only the ones that satisfy the conditions.
