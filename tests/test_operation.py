import brownie
from brownie import Contract, chain
import pytest


def test_deposit(user, ftm_ape_zap, vault, wftm):

    before = user.balance()
    amount = 10 ** 18
    ftm_ape_zap.deposit({"from": user, "amount": amount})

    assert vault.balanceOf(user) != 0
    assert before == user.balance() + amount


def test_withdraw(user, ftm_ape_zap, vault, wftm):
    amount = 10 ** 18
    ftm_ape_zap.deposit({"from": user, "amount": amount})
    chain.sleep(86400)

    before = user.balance()
    vault.approve(ftm_ape_zap, vault.balanceOf(user), {"from": user})

    ftm_ape_zap.withdraw(vault.balanceOf(user), {"from": user})
    assert user.balance() > before
