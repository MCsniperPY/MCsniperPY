<h1 align="center">
	<img
		width="500"
		alt="MCsniperPY"
		src="https://i.imgur.com/hl7h1ta.png?sanitize=true">
</h1>

<h3 align="center">
	A Fast, async, and open source Minecraft name sniper.
</h3>

<p align="center">
	<strong>
		<a href="https://mcsniperpy.github.io/">Website</a>
		•
		<a href="https://">Usage</a>
	</strong>
</p>
<p align="center">
	<a href="https://github.com/MCsniperPY/MCsniperPY">
	<img
		alt="GitHub Stars"
		src="https://img.shields.io/github/stars/MCsniperPY/MCsniperPY?color=%2370a1d2&label=Stars%20%E2%AD%90"></a>
	<a href="https://python.org/download"><img
		alt="Python Versions"
		src="https://img.shields.io/badge/Python%20Versions%20%F0%9F%90%8D-3.7%20%7C%203.8-%2370a1d2"></a>
		<a href="https://mcsniperpy.github.io/discord"><img src="https://img.shields.io/discord/734794891258757160?color=%2370a1d2&label=Discord&logo=discord&logoColor=white"></a>
</p>

<p align="center">
	<img src="https://i.imgur.com/5PUNwfR.gif" width="550">
</p>

## Overview

- **Asynchronous**  • MCsniperPY is asynchronous meaning it tends to be faster and more efficient than multithreaded name snipers
- **Open source** • MCsniperPY is open source, meaning you can look at everything that goes on behind the scenes to get you a name. This means you can be sure it doesn't steal your account.
- **Fast** • MCsniperPY is fast, but not so fast that your requests run out instantly.

## Table of Contents

<ul>
    <li><a href="#Installing">Installing</a></li>
    <li><a href="#Setup">Setup</a></li>
    <li><a href="#Config">Config</a></li>
    <li><a href="#Delays">Delays</a></li>
    <li><a href="#Running-the-sniper">Running the sniper</a></li>
    <li><a href="#Understanding-the-logs">Understanding the logs</a></li>
  </ul>

## Installing

### Linux easy installation

Run `bash -c "curl -sLo mcsniperpy.sh https://raw.githubusercontent.com/MCsniperPY/MCsniperPY/master/install.sh && chmod +x mcsniperpy.sh && ./mcsniperpy.sh"` in your terminal to install the sniper. To run it again just type `./mcsniperpy.sh`.


### Windows installation

You will have to have a few things installed before running the sniper. This installation guide assumes that you are on a 64bit Windows system.

First, you will need to install Python. It's recommended to use either version `3.8.5` or `3.8.6`. You must use a Python version above `3.0`. 

### Installing Python

Go to the following link and download Python:

`https://www.python.org/ftp/python/3.8.5/python-3.8.5-amd64.exe`

Once you have opened the installer, make sure that you add Python to path. Your installer should look like this:

<img align="center" src="https://i.imgur.com/iefWNyw.png">

Run through the installer as normal, then download the McSniperPY files.

### Downloading McSniperPY

Download the following file:

`https://github.com/MCsniperPY/MCsniperPY/archive/master.zip`

Extract the folder to somewhere easily accessible, such as your desktop.

You should have a folder containing the following files:

<img src="https://i.imgur.com/pdB8Y8P.png">

If you have more files than this don't worry, the sniper has most likely been updated since this guide was written.
If your folder doesn't have a file called `accounts.txt`, then create one.

### Installing dependencies

You now need to open a command prompt to the McSniperPY path. An easy way to do this is by opening the folder and typing `cmd` in the path:

<img src="https://i.imgur.com/qWfwXIL.png">

Your command prompt should have a line similar to this:

`C:\Users\%USERNAME%\%PATH%\MCsniperPY-master>`

If there is nothing after your Windows username, you will have to type the following command:

`cd path_to_folder`

Once you have a commant prompt open to the correct path, you should type the following command:

`py -m pip install -r requirements.txt`

If you get the following message:

`'py' is not recognized as an internal or external command, operable program or batch file.`

then you will need to reinstall Python following the guide above, make sure that you added Python to PATH.

If you get a red error, with this message inside:

`error: Microsoft Visual C++ 14.0 is required.`

then you will need to download Microsoft Build Tools, you can do that by downloading the following program and installing Build Tools:

`https://visualstudio.microsoft.com/thank-you-downloading-visual-studio/?sku=BuildTools`

Otherwise, you have installed the correct dependencies and can follow on with the tutorial.
If you have a problem and can't figure it out, feel free to ask in `#support` in the McSniperPY Discord server.

### Installing Dimension 4

Sometimes your computer's time can come out of sync. If this happens to you then all of your name snipes will be inconsistent, meaning you can't figure out your delays properly and all of your snipes are just lucky. Dimension 4 fixes this. The UNIX equivalent to this is called chrony.

Download Dimension 4 from the following link (download is at the bottom of the page):
 
`http://www.thinkman.com/dimension4/download.htm` 

Install Dimension 4, then open it.

<img src="https://i.imgur.com/sFTBS44.png">

Click the "Sync Now" button at the top right, your time should now be synced.

You can check if your time is synced by visiting the following website:

`https://time.is/`

## Setup

You have to provide the sniper with accounts, you can also edit the config file if wanted. 

### Accounts

Open the file `accounts.txt` and put your accounts in.

The order for accounts are:

`email:password:sq1:sq2:sq3`

Sq1, 2 and 3 being the answer to security questions. The order of these are the same order that they appear on the Minecraft website.
The security questions are optional.

Here's an example of a valid `accounts.txt`:

```
email@gmail.com:Password1
email@hotmail.co.uk:Password2:Dogs:Cats:Llamas
```

###### Note that currently only Mojang accounts are supported.

### Config

The config is where you can customise the sniper, it is found at `config.txt`.

You can modify all of these values, please note that you shouldn't put quotes.

Here's what all of the current features do:


| Key | Possible Values| Explanation|
| ------------- |:-------------:| -----:|
| timing_system      | namemc | What timing system to use |
| skin      | path      |  The path to a skin to upload when a snipe is successful|
| skin_model | slim, classic      | What skin type to use when uploading |
| change_skin | true, false    | Whether the sniper should change skin on a successful snipe |
| snipe_reqs | number    | How many requests per account to send when sniping |
| auth_delay | number    | Time in milliseconds to login to accounts before they release |
| max_accs | number    | Maximum number of accounts to use when sniping |

Optional features:

| Key | Possible Values| Explanation|
| ------------- |:-------------:| -----:|
| custom_announce | token    | Your token for the Discord server's custom announcer |
| wh | webhook | Discord Webhook URL  |

To get a custom_announce token, join the Discord server and type `>generate` in the `#bot-commands` channel and follow the instructions that the bot DM's you. Make sure your DM's are open.

## Delays

A delay is the time in milliseconds that the sniper starts to send requests before the name drop time. If a name drops at `10:00:59` and you tell the sniper to use a delay of `1000`, the sniper will start sending the requests at `10:00:58` because 1000 milliseconds = 1 second.

Delays are useful for 2 reasons — ping and server lag.

If you have high ping to Mojang's APIs (api.minecraftservices.com, not api.mojang.com - they're seperate servers) then using a higher ping is recommended, vice versa goes for lower pings. Note that MinecraftServices is hosted in Ashburn, Virginia. 

If a lot of people are going for a username (you can usually determine this by the amount of views it has on NameMC) then Mojang's servers can lag. It's generally advised to use a higher delay when going for a name with high views.

Other people's delays in most cases won't work on your machine. Delays can depend on many things, including ping, network routes and even CPU speed. 

A good way to find a delay that works for you is to attempt to snipe usernames with a delay of `400`, then adjusting the delay based off of the timestamp you receieve. If the snipe is early, your delay is too high.

If you need help with your delays, and have followed the suggested method above then you can ask for help in the `#support` channel in McSniperPY's Discord server.

## Running the sniper

To run the sniper you want to open a command prompt window where McSniperPY is located.

You can do that like so:

<img src="https://i.imgur.com/qWfwXIL.png">


Once the window is open, you want to type the following command:

`py snipe.py`

Assuming nothing went wrong, the sniper should now be running;

<img src="https://i.imgur.com/3YZ0pP3.png">

You can now follow the onscreen instructions.

## Understanding the logs

When you attempt to snipe a name, you are given information about the requests that McSniperPY sends to Mojang's API. This information is in the following format: 

`[fail/success] [http status code] @ [timestamp]`

The timestamp is the time that you got a response from mojang about your request

### HTTP Status Codes

When the sniper sends requests to a server, it returns a HTTP Status Code. Mojang's API returns a status code based on what we requested, in terms of name sniping, the status codes and their meanings can be seen below:

| Status Code| Meaning|
| ----------- | ----------- |
| 200| Sniped name successfully|
| 403 | Failed to snipe name|
| 429 | Account or IP is rate limited|
| 500| Minecraft API issue|


> Thanks to [sneakers](https://github.com/sneakers) for writing these docs!
