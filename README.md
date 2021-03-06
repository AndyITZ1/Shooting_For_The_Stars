# Shooting For The Stars

​	Group Project for CIS4930. Designed, built, and cared for by Luan Tran, Daniel Brodbeck, Jose Lopez, and Calvin Yang.

---

## Description

​	Thank you for your interest in Shooting For The Stars, a 2D rhythm-based vertical platformer. You play as a music major college student looking for a chance to prove their worth. Luckily for you, Starlight Entertainment has given you just the opportunity. Climb the building using your rhythm and platforming skills to impress the company's CEO (indicated by your score) while dodging enemies that wish to see your downfall. Do you have what it takes to shoot for the stars?

Project pitch: https://www.youtube.com/watch?v=5DXMSx98GKI

Project GitHub Repo: https://github.com/Andytr13/Shooting_For_The_Stars

---

## User Installation

​	Your installation process will differ based on your given game distribution. It is important to note that this game is meant to be installed and run on Windows 10 machines only. The game is only stable using Python 3.8. Please note that you have to have the repository setup locally and refer to the Developer's FAQ for files needed in the following sections.

### tar.gz file

​	Receiving this game as a compressed archive (also known as a tar.gz file) might seem intimidating to install, but is rather easy if you have Python installed on your machine. Python's handy built-in pip tool can install the game in one simple terminal command. Navigate to where you placed the tar.gz file and run 

- pip install [file-name].tar.gz

​	in any terminal. Pip will download and install any necessary Python package dependencies to run the game. When it is done, a new command will be created that you can use through any terminal, regardless of the directory, that will run the game:

- SFTS

​	If your system complains that "pip" is not a valid command, then your Python installation did not correctly add the necessary system paths to use pip or the "SFTS" commands. This can be fixed, however, through online tutorials.

### Installer

​	Receiving this game as an installer is even easier for beginners, since it avoids using terminals or even installing Python. The installer will guide you to where you wish to place the game folder and then do the heavy lifting for you. The newly created game folder will contain a <Shooting For The Stars.exe> file that you can run to play the game. You may also wish to keep the installer afterwards to either fix your game or uninstall it.

---

## Game Manual

### Controls

- Left/right arrow keys OR A/D keys: move character left/right.
- Up arrow key OR W key OR space: jump. Hold the jump key to jump higher.
- P or ESC to pause the game during gameplay, press again to unpause.
- Mouse Click and Cursor movement during Rhythm Game Minigame

### Mechanics

- Screen wrapping: If your character goes past the screen's border, you wrap around to the other side of the screen. May prove useful to reach far-away platforms or to dodge enemies.
- Jumping on the beat: If you jump on the music's beat (also indicated when your character either bops their head or if they turn yellow while having the shield powerup), your regular jump becomes empowered. You jump higher and your movement speed is doubled. Helpful when trying to reach far-away platforms.
- Power-ups: two powerups make prove useful to your adventures. Three yellow arrows indicate a boost powerup. This will make your next jump become empowered! The other powerup is a rainbow music symbol. Picking it up will give you a shield that prevents any enemy damage or effects.
- Enemies:
  - Music disc enemies will occasionally be spotted moving back and forth. Touching one of these enemies will set you back in terms of level progress, so make sure to avoid them and to time your jumps correctly. 
  - Starting at level 2 and above, pusher enemies can be seen moving back and forth on random platforms. Touching them will fling your character away, so be careful to not touch them!
  - Each level has a boss that can be encountered roughly half-way in the level. If you choose to engage it, be prepared to do a mouse-clicking minigame. Expect high rewards to be granted for passing the boss battle and heavy punishment for failing the minigame!
- Levels: The game is made up of 3 levels, each harder than the previous, and an endless mode. To unlock harder levels and endless mode, you must first unlock them by beating the previous level. Fear not, because your unlocked levels are saved if you wish to exit the game.
- Minigame: Encountering a boss will let you play a minigame for high risk, high reward. The goal is to click on the buttons just as the outer blue ring touches it. Just as each level is harder than the previous one, each minigame is harder than the previous one.

---

## Developer FAQ

- How do I create a tar.gz file?

  Navigate inside the project directory where setup.py is located. Run the command "python setup.py sdist". The new tar.gz file will be found under the newly created dist directory.

- How do I create an installer?

  An MSI can be created by navigating inside the project directory where msi_setup.py is located, runnning the command "python msi_setup.py bdist_msi", and obtaining the installer within the newly created dist directory. Be warned that you must first pip install "cx_Freeze" to create the MSI.

---
## End User Feedback/Experience from outside demo testers
Controls: Basic controls similar to other games, but easy to pick up on without telling users.

Difficulty: From a new player perspective, the game was difficult and met with frustration between jumps at the beginning. Upon learning about other key features like power-ups and rhythmic jump mechanic without letting the user know the game became less frustrating. 

Pacing of difficulty change upon was not either too fast or slow, since the player had to adapt to key features, but this did not make it quickly easier given other challenges like the rate of power-up spawns and also enemies spawning. 

Overall experience from users was challenging and addictive for enjoyment. 

---

## Acknowledgements

Websites that aided in the development of the game:

- Game Development in Python 3 With PyGame - 16 - Convert to executable, by user sentdex: https://www.youtube.com/watch?v=EY6ZCPxqEtM&list=PLQVvvaa0QuDdLkP8MrOXLe_rKuf6r80KO&index=16&ab_channel=sentdex
- Pygame Platformer – Game Development, by CodersLegacy: https://coderslegacy.com/python/pygame-platformer-game-development/

Assets:

- Game vector icons: https://www.flaticon.com/
- Game music: 8 Bit Retro Funk by David Renda: https://www.fesliyanstudios.com/royalty-free-music/downloads-c/8-bit-music/6
- Game music: Up In My Jam by Kubbi: https://youtu.be/cLX0cyh6_Ro
- Game music: Blip Stream Kevin MacLeod (incompetech.com)
Licensed under Creative Commons: By Attribution 3.0
- Game music: DOVA-SYNDROME HP: https://dova-s.jp/
http://creativecommons.org/licenses/by/3.0/
- Game music: https://www.FesliyanStudios.com
- Game background, by u/ak077: https://www.reddit.com/r/wallpapers/comments/b4eyji/8bit_sunset_2560x1700/
- Two icons made by users Freepik and Iconixor found at www.flaticon.com
- Boss encounter and minigame win SFX made by Tony Parsons at www.dreamstime.com
- Game player, enemy, and boss sprites created by Lighty and Luan Tran.
