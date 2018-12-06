# TekkenBot
AI and tools for playing and understanding Tekken 7.

Created by roguelike2d. Maintained by the community. MAKE SURE YOU ALWAYS HAVE THE LATEST VERSION OF memory_address.ini

This Fork is geared toward creating tools to help players practice and understand the game better

## Tools
Download executable from: https://github.com/compsyguy/TekkenBot/issues/1

If you're using a compiled release version, run TekkenAcademy.exe. If you're running from source with Python 3 installed, run GUI_TekkenAcademy.py

### Punish Practice
Goes through all the punishbale moves for a character. It will tell you the frames and repeat the move 3 times before moving on. If the CPU ends in stance, it might error out currently.
To use go to Practice Mode -> CPU Action: Controller.
Have the CPU use the 2p Keyboard (Hit home on the keyboard).
Works best in a wallless stage.
See 
https://github.com/compsyguy/TekkenBot/issues/2 
for characters that are currently working.

### Punish Test
Like the practice, but it doesn't tell you ahead of time what's coming, and it will only do the move once.
Once you successfully punish a move, it will remove it from the rotation.


## Project details

### Prerequisites
Tekken Bot is developed on Python 3.5 and tries to use only core libraries to improve portability, download size, and, someday, optimization. It targets the 64-bit version of Tekken 7 available through Steam on Windows 7/8/10.

### Updating Memory Addresses with Cheat Engine after patches
When Tekken 7.exe is patched on Steam, it may change the location in memory of the relevant addresses. To find the new addresses, use Cheat Engine or another memory editor to locate the values, then find the new pointer addresses:

Currently, Tekken Bot only needs one value (Tekken7.exe Base + first offset  --> follow that pointer to a second pointer --> follow the second pointer to the base of the player data object in memory).
To find the player data object you can use the following values for player 1 animation ids:
 * Standing: 32769
 * Crouching (holding down, no direction. Hold for a second to avoid the crouching animation id): 32770

Alternately, you can search for move damage which is displayed in training mode and active (usually) for the duration of the move.

Whatever you find, there should be 9 values, eight in addresses located close together and one far away. Find the offset to the pointer to the pointer of any of the first 8 and replace the 'player_data_pointer_offset' value in MemoryAddressEnum.py.