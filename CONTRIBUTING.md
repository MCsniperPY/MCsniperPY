# First Contributions

First of all, thank you for considering contributing to MCsniperPY🎉! If you're looking to contribute features then check out the [contributing code](#contributing-code) section.

Even if you can't code there are things to contribute. For example, you can report bugs, request features, or fix / add documentation.  

If you want some stuff to contribute check out the `TODO.md` file.

## Contributing code

#### If you don't have git on your machine, [install it](https://help.github.com/articles/set-up-git/).

## Fork this repository 
<img align="right" width="300" src="https://firstcontributions.github.io/assets/Readme/fork.png" alt="fork this repository" />
Fork this repository by clicking on the fork button on the top of this page.
This will create a copy of this repository in your account. 

## Clone the repository

<img align="right" width="300" src="https://firstcontributions.github.io/assets/Readme/clone.png" alt="clone this repository" />

Now clone the forked repository to your machine. Go to your GitHub account, open the forked repository, click on the code button and then click the _copy to clipboard_ icon.

Open a terminal and run the following git command:

```
git clone "url you just copied"
```

where "url you just copied" (without the quotation marks) is the url to this repository (your fork of this project). See the previous steps to obtain the url.

<img align="right" width="300" src="https://firstcontributions.github.io/assets/Readme/copy-to-clipboard.png" alt="copy URL to clipboard" />

For example:

```
git clone https://github.com/this-is-you/first-contributions.git
```

where `this-is-you` is your GitHub username. Here you're copying the contents of the first-contributions repository on GitHub to your computer.

## Create a branch

Change to the repository directory on your computer (if you are not already there):

```
cd MCsniperPY
```
Next, checkout to the `recode` branch which is where all the code is.

`git checkout recode` 

Now create a branch using the `git checkout` command:

```
git checkout -b your-new-branch-name
```

For example:

```
git checkout -b add-microsoft-account-support
```

## Make necessary changes and commit those changes

Now do all of the code changes which you would like to. This can include documentation, features, bug fixes, or anything else you think should be included.

<img align="right" width="450" src="https://firstcontributions.github.io/assets/Readme/git-status.png" alt="git status" />

If you go to the project directory and execute the command `git status`, you'll see there are changes.

Add those changes to the branch you just created using the `git add` command:

```
git add .
```

you can add specific changes with `git add <filename>` or all of your changes with `git add .`

Now commit those changes using the `git commit` command:

```
git commit -m "short description of your changes"
```
Now open `README.md` file in a text editor, add your name to the contributors section. Now, save the file.

add the files again (`git add README.md`) and (`git commit -m "Add name to contributors section in README"`)

**Please keep your commits small.** This helps the maintainers find nefarious code more easily. 


## Push changes to GitHub

Push your changes using the command `git push`:

```
git push origin <add-your-branch-name>
```

replacing `<add-your-branch-name>` with the name of the branch you created earlier.

## Submit your changes for review

If you go to your repository on GitHub, you'll see a `Compare & pull request` button. Click on that button.

<img style="float: right;" src="https://firstcontributions.github.io/assets/Readme/compare-and-pull.png" alt="create a pull request" />

Now submit the pull request.

<img style="float: right;" src="https://firstcontributions.github.io/assets/Readme/submit-pull-request.png" alt="submit pull request" />

Soon someone will review your pull request.

> Please do not be offended if one of the maintainers rejects or requests changes to your pull request. There are some features which just aren't necessary from our opinions. If you want to ask if a change is needed check out the `#contributing` channel in the discord.

## Done

You've completed your first contribution! Congrats 🎉! 

If you want to contribute again make sure you follow the instructions starting at [create branch](#Create-branch)
