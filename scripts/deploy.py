from brownie import accounts, network, FTMApeZap
import click


def main():
    deployer = accounts[0]
    if network.show_active() == "mainnet":
        deployer = accounts.load(
            click.prompt("Account", type=click.Choice(accounts.load()))
        )
    click.echo(f"You are using: 'deployer' [{deployer.address}]")
    vault = "0x0dec85e74a92c52b7f708c4b10207d9560cefaf0"
    deployer.deploy(FTMApeZap, vault)
