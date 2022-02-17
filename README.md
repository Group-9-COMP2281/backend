# Backend for Panel
This is the repository containing the code and files pertaining to the backend. Your project should have a virtual
environment with all the packages installed. Before each commit, please ensure `requirements.txt` has been updated!

## Creating a virtual environment
To create one, run `python3 -m venv venv` in this directory.

## Using virtual environments
This must be done before running the project, or using pip, etc.
`source venv/bin/activate`

Within the virtual environment, to install a package, use `pip install <package>`, and to run a python file use `python <file.py>

To check you have all the packages listed in `requirements.txt`, use `pip install -r requirements.txt`

## Committing
`./commit.sh` will run a command doing some pre-commit tasks, including updating `requirements.txt`

## Pushing
`git push -u origin master`
