#!/bin/bash
npm install
npx hardhat compile

sudo cp ctf /etc/xinetd.d/
sudo /etc/init.d/xinetd restart