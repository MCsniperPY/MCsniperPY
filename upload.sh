#!/bin/bash

declare -A manager;
manager[/etc/redhat-release]=yum;
manager[/etc/arch-release]=pacman;
manager[/etc/gentoo-release]=emerge;
manager[/etc/debian_version]=apt-get;

if ! [ -x "$(command -v twine)" ]; then
		if [ "$UID" -eq 0 ]; then
			echo "Press enter to install twine";
			choice="y";
		else
			echo "You do not have twine installed, do you want to restart with root permission and install it? (Y/N): ";
			read TMP;
			if [ $TMP  == "y" ] || [ $TMP == "Y"]; then
				exec sudo "$0" "$@"
			else
				echo "Quitting"
				exit
			fi
		fi
		if [ $choice == "y" ]; then
			for f in ${!manager[@]}
			do
				if [[ -f $f ]];then
					manager=${manager[$f]}
					echo "Detected $manager as your package manager";
					case $manager in
						pacman)
							pacman -S twine
						;;
						apt-get)
							apt install twine
						;;
						emerge)
							emerge twine
						;;
						yum)
							yum install twine
					esac
					echo "\"twine\" should be installed now."
					rm dist/*
					python3 setup.py sdist bdist_wheel
					twine upload dist/*
				fi
			done
		else
			echo "Quitting.."
			exit 1;
		fi
	else
		rm dist/*
		python3 setup.py sdist bdist_wheel
		twine upload dist/*
	fi
