@echo off
echo Installing dependencies...
pip install -r requirements.txt
if not exist domains.txt (
    copy domains.example.txt domains.txt
    echo Created domains.txt - edit it to list the domains you want cleaned up.
)
echo Done.
