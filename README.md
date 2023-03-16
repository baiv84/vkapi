# Description

`vkapi` is a console tool to publish comics (picture + funny story) to the particular [vk.com](https://vk.com) public group page. 

The comics content is downloaded from the [https://xkcd.com](https://xkcd.com/) resources.

# Project Goals

The code is written for the educational purposes on online-course for the web-developers [dvmn.org](https://dvmn.org/).

# Prerequisites

Firstly, we need to install package `python3-venv` to work with python virtual environment.

Please, update packages on your system `!(it depends on your operating system)`

as for me, I use Ubuntu as a host operating system. 

So I run:
```console
$ sudo apt update
```

and install python virtual environment package:
```console
$ sudo apt install -y python3-venv
```

Then jump to project folder:
```console
$ cd vkapi
```

and create new virtual environment to run the code:
```console
$ python3 -m venv venv
```

Activate new virtual environment:
```console
$ source venv/bin/activate
```

As a result, you will see command line prompt like this:
```console
(venv) vkapi $ 
```

# Install dependencies

In the virtual environment run command:

```console
(venv) vkapi $  pip install -r requirements.txt
```

This command installs all necessary libraries (`requests`, `environs`) into the `venv` environment.

# Setup environment variables

To work with [Vkontakte API](https://dev.vk.com/reference/) we need to create new file with name: `.env` and add there 2 lines:

```
VK_COMICS_GROUP_ID=xxxx
```

where `xxxx` - please, replace with your personal public group ID value.

and

```
VK_ACCESS_TOKEN=yyyy
```

where `yyyy` - please, replace with your personal VK.COM access token value.

Save and close the file, go ahead with running program.

---

# Run program 

To run program, in console jump to the project folder and execute command:

```console
(venv) vkapi $ python main.py
```

# Control results

If program runs successfully, you will see the results like these:

![Alt text](img/1.png?raw=true "vkapi")

In browser open your group page, then you will see the new comics picture on the page:

![Alt text](img/2.png?raw=true "comics picture")

# Final steps

Deactivate virtual environment:

```console
(venv) vkapi $ deactivate
```

Close console:
```console
$ exit
```