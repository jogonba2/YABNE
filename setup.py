#!/usr/bin/env python
# -*- coding: utf-8 -*-
#  Acceptance.py

from os import system
from sys import argv
from Messages import Messages
import urllib.request


if __name__ == "__main__":

    if len(argv)==2 and argv[1]=="install":
        print(Messages.installing("pip"))
        pip_file, headers = urllib.request.urlretrieve("https://bootstrap.pypa.io/get-pip.py", filename="get-pip.py")
        pip_file = open(pip_file)
        system("python get-pip.py")
        print(Messages.installing("numpy"))
        system("pip install numpy")
        print(Messages.installing("scipy"))
        system("pip install scipy")
        print(Messages.installing("matplotlib"))
        system("pip install matplotlib")
        print(Messages.installing("scikit-learn"))
        system("pip install scikit-learn")
        print(Messages.installing("deap"))
        system("pip install deap")
        print(Messages.installing("hyperopt"))
        system("pip install hyperopt")
        print(Messages.all_installed())
