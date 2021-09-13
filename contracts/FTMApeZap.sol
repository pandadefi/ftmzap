pragma solidity ^0.8.7;

import "@openzeppelin/contracts/token/ERC20/utils/SafeERC20.sol";
import "@openzeppelin/contracts/token/ERC20/IERC20.sol";

interface Vault is IERC20 {
    function deposit(uint256 amount) external returns (uint256);

    function deposit(uint256 amount, address recipient)
        external
        returns (uint256);

    function withdraw(uint256 maxShares) external returns (uint256);

    function withdraw(uint256 maxShares, address recipient)
        external
        returns (uint256);
}

interface WFTM is IERC20 {
    function deposit() external payable returns (uint256);

    function withdraw(uint256 amount) external returns (uint256);
}

contract FTMApeZap {
    using SafeERC20 for IERC20;
    Vault immutable vault;
    WFTM constant wftm = WFTM(0x21be370D5312f44cB42ce377BC9b8a0cEF1A4C83);

    constructor(Vault _vault) {
        vault = _vault;
    }

    function deposit() public payable {
        require(msg.value != 0, "!value");
        wftm.deposit{value: msg.value}();
        if (wftm.allowance(address(this), address(vault)) < msg.value) {
            SafeERC20.safeApprove(wftm, address(vault), 0);
            SafeERC20.safeApprove(wftm, address(vault), type(uint256).max);
        }
        vault.deposit(msg.value, msg.sender);
    }

    function withdraw(uint256 amount) public {
        SafeERC20.safeTransferFrom(vault, msg.sender, address(this), amount);
        uint256 wftmAmount = vault.withdraw(amount);
        require(wftmAmount != 0, "!amount");

        wftm.withdraw(wftmAmount);

        (bool success, ) = msg.sender.call{value: wftmAmount}("");
        require(success, "Transfer failed.");
    }

    receive() external payable {}
}
