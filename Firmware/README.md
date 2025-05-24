# Flash OpenMV Firmware into Weact STM32H7

- [Install STM32 Cube Programmer](https://www.st.com/en/development-tools/stm32cubeprog.html)
- download `openmv.bin` from `OpenMV 4.4.1/` folder.
- Connect Weact STM32H7 to computer. 
- Enter into DFU mode, hold BOOT (B0) button, press RESET (NR) then release.
- Use STM32 Cube Programmer to flash `openmv.bin` to address `0x08000000`
- Upload the micropython code to the board.