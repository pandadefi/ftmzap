import pytest
from brownie import config
from brownie import Contract


@pytest.fixture
def deployer(accounts):
    yield accounts[0]


@pytest.fixture
def user(accounts):
    yield accounts[1]


@pytest.fixture
def vault():
    yield Contract("0x0dec85e74a92c52b7f708c4b10207d9560cefaf0")


@pytest.fixture
def wftm():
    yield Contract("0x21be370D5312f44cB42ce377BC9b8a0cEF1A4C83")


@pytest.fixture
def ftm_ape_zap(FTMApeZap, vault, deployer):
    yield deployer.deploy(FTMApeZap, vault)
