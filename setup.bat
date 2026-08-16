@echo off
echo Installing dependencies...
pip install -r requirements.txt
if not exist domains.txt (
    echo # One domain per line. Lines starting with # are ignored. > domains.txt
    echo # Any inbox email whose sender address is @^<domain^> will be trashed. >> domains.txt
    echo Created domains.txt - edit it to list the domains you want cleaned up.
)
echo Done.
