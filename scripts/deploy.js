// We require the Hardhat Runtime Environment explicitly here. This is optional
// but useful for running the script in a standalone fashion through `node <script>`.
//
// You can also run a script with `npx hardhat run <script>`. If you do that, Hardhat
// will compile your contracts, add the Hardhat Runtime Environment's members to the
// global scope, and execute the script.
const hre = require("hardhat");
const toml = require('toml');
const fs = require('fs');
const CryptoJS = require('crypto-js');

async function main() {
  const Challange = await hre.ethers.getContractFactory("Challange");
  const challange = await Challange.deploy();
  await challange.deployed();

  console.log(`Challange: ${challange.address}`);
  
  const tomlFile = fs.readFileSync('./config.toml');
  const config = toml.parse(tomlFile);

  const plaintext = challange.address;
  const key = CryptoJS.enc.Hex.parse(config["key"]);
  const iv = CryptoJS.enc.Hex.parse(config["iv"]);
  const ciphertext = CryptoJS.AES.encrypt(plaintext, key, { iv: iv }).toString();

  console.log(`Your Token: ${ciphertext}`);
}

// We recommend this pattern to be able to use async/await everywhere
// and properly handle errors.
main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});
