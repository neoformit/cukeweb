#!/usr/bin/env bash

# Latex install and setup

sudo apt install xzdec  # compression library
sudo apt install texlive-latex-recommended
tlmgr init-usertree
tlmgr install longtables

