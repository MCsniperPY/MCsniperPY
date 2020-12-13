#!/bin/bash


# checks

## python
clear
echo "--> starting command tests"
if ! command -v python3 &> /dev/null
then
    echo "[error] python could not be found.. please make sure you have python installed."
    echo "For ubuntu you can run 'sudo apt-get install python3' to install python"
    exit
else
    echo "[ok] python detected | moving on..."
fi

## git

if ! command -v git &> /dev/null
then
    echo "[error] git could not be found... please make sure you have git installed."
    exit
else
    echo "[ok] git detected | moving on..."
fi

if ! command -v nano &> /dev/null; then
    echo "[error] nano could not be found... This will cause errors later on with opening accounts.txt."
else
    echo "[ok] nano detected | moving on..."
fi


echo ""
echo ""


# Checks if MCsniperPY is already installed

if [ -d MCsniperPY ]; then
    cd MCsniperPY
elif [[ "${PWD##*/}" == "MCsniperPY" ]]; then
    echo "[ok] you are already in MCsniperPY"
    echo ""
    echo ""
else
    echo "[ok] installing MCsniperPY..."
    git clone -q https://github.com/MCsniperPY/MCsniperPY
    echo "[ok] installed MCsniperPY"
    cd MCsniperPY
    echo ""
    echo ""
fi

# Checks if the sniper is already setup

if [ ! -e already_setup ]
then
    echo "[ok] installing requirements..."
    python3 -m pip install -q -r requirements.txt
    echo "[ok] successfully installed requirements!"
    echo > already_setup
    echo ""
    echo ""
fi

changed=0
git remote update && git status -uno | grep -q 'Your branch is behind' && changed=1
if [ $changed = 1 ]; then
    echo "[warning] MCsniperPY has a new update!"
    echo "[warning] If you update MCsniperPY, and have modified any files including config.txt, this will not work!"
    read -p "would you like to update MCsniperPY (y/n)? " -n 1 -r
    echo ""
    if [[ $REPLY =~ ^[Yy]$ ]]
    then
        echo "[ok] updating MCsniperPY..."
	git pull -q
	echo "[ok] updated MCsniperPY..."

    else
	echo "[warning] not updating MCsniperPY."
    fi
else
    echo "[ok] MCsniperPY is up to date!"
fi

echo ""
echo ""

if [ ! -f accounts.txt ]
then
    echo > accounts.txt
    echo "[warning] no accounts.txt file detected"
    echo "[ok] created accounts.txt file"
    echo ""
    real_path=$(realpath accounts.txt)
    config_path=$(realpath config.txt)
    echo "Please enter your account(s) in accounts.txt"
    echo "The format is email:password OR email:password:answer:answer:answer if you have security questions. You can enter multiple accounts by seperating them with a new line."
    echo "To open this file again type 'nano $real_path'"
    read -p "press any key to open accounts.txt... " -n 1 -r
    nano accounts.txt
    echo ""
    echo ""
    echo "Save these commands for later use:"
    echo "'nano $real_path' <- Opens accounts.txt"
    echo "'nano $config_path' <- Opens the MCsniperPY configuration file"
    echo ""
    echo ""
    read -p "Press any key to continue... " -n -1 -r
else
    echo "[ok] accounts.txt already detected"
fi

# Clear the screen and run the sniper

clear

python3 snipe.py
