# TekkenBot
AI and tools for playing and understanding Tekken 7.

Created by roguelike2d. Maintained by the community. MAKE SURE YOU ALWAYS HAVE THE LATEST VERSION OF memory_address.ini

## Tools
Download from https://github.com/WAZAAAAA0/TekkenBot/releases

If you're using a compiled release version, run TekkenBotPrime.exe. If you're running from source with Python 3 installed, run GUI_TekkenBotPrime.py

### FrameDataOverlay
A window that can go over the game to display real time move information read from memory. Requires the game to be in windowed or borderless to work or can be run as a standalone window on a second screen.
![Robot feet and bear paws 1](Screenshots/frame_data.png?raw=true)

### CommandInputOverlay
Display command inputs, similar to the one already in Tekken 7 except it gives frame by frame information and includes cancelable frames.
![Robot feet and bear paws 2](Screenshots/command_input.png?raw=true)

## Bots
Currently in progress.

### Details
Tekken Bot bots are programs that plays Tekken 7 on PC by reading the game's memory, making decisions based on the game state, and then inputting keyboarding commands. Ultimately the goal is to create emergent behavior either through specific coding it or, if possible, a generalized learning algorithm.


### Frame Trap Bot
Pushes jab or a user inputted move when getting out of block stun.

### Punisher Bot
Attempts to punish negative attacks with the best available punish. Punishes are listed in the character's file in the /TekkenData folder.


## Project details

### Prerequisites
Tekken Bot is developed on Python 3.5 and tries to use only core libraries to improve portability, download size, and, someday, optimization. It targets the 64-bit version of Tekken 7 available through Steam on Windows 7/8/10.

### Deployment
Tekken Bot distributable is built using pyinstaller with Python 3.5. On Windows, use the included build_project.bat file.

### Updating Memory Addresses with Cheat Engine after patches
When Tekken 7.exe is patched on Steam, it may change the location in memory of the relevant addresses. To find the new addresses, use Cheat Engine or another memory editor to locate the values, then find the new pointer addresses:

Currently, Tekken Bot only needs one value (Tekken7.exe Base + first offset  --> follow that pointer to a second pointer --> follow the second pointer to the base of the player data object in memory).
To find the player data object you can use the following values for player 1 animation ids:
 * Standing: 32769
 * Crouching (holding down, no direction. Hold for a second to avoid the crouching animation id): 32770

Alternately, you can search for move damage which is displayed in training mode and active (usually) for the duration of the move.

Whatever you find, there should be 9 values, eight in addresses located close together and one far away. Find the offset to the pointer to the pointer of any of the first 8 and replace the 'player_data_pointer_offset' value in MemoryAddressEnum.py.