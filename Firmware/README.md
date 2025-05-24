# Flash OpenMV Firmware into Weact STM32H7

- [Install STM32 Cube Programmer](https://www.st.com/en/development-tools/stm32cubeprog.html)
- download `openmv.bin` from `OpenMV 4.4.1/` folder.
- Connect Weact STM32H7 to computer. 
- Enter into DFU mode, hold BOOT (B0) button, press RESET (NR) then release.
- Use STM32 Cube Programmer to flash `openmv.bin` to address `0x08000000`
- Upload the micropython code to the board.

## Credits

This firmware is based on [OpenMV](https://github.com/openmv/openmv) version 4.4.1 and was originally built by **WeAct Studio**.

All credit for building and adapting the firmware for the WeAct boards goes to **WeAct Studio**. This repository is provided for reference and convenience.

- 🔗 Official WeAct GitHub: [https://github.com/WeActStudio](https://github.com/WeActStudio)
- 📦 Original firmware source: [https://github.com/WeActStudio/MiniSTM32H7xx](https://github.com/WeActStudio/MiniSTM32H7xx)

Please support the original authors and contributors by visiting their repositories and projects.
