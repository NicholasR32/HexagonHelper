## Have you heard of [Super Hexagon](https://store.steampowered.com/app/221640/Super_Hexagon/)?
It's an awesome, minimalist, fast-paced game where you move around a hexagon, surviving an onslaught of walls that try to crush you.

Before beating the game, I thought it would be cool to have a simple tool to record and list my attempts, calculate some basic stats, and bundle it in a nice little app. And I called it:

## Hexagon Helper.
- How it works: Play any of the game's 6 levels until you hit a wall.

- Then, survival times for each attempt are scraped from the game screen using [pyautogui's screenshot functions](https://pyautogui.readthedocs.io/en/latest/screenshot.html).

- The GUI was made using [tkinter](https://tkdocs.com/tutorial/index.html). The app also features the [Bump IT UP font](https://fontstruct.com/fontstructions/show/155156/bump_it_up) used in the game. Bump IT UP is designed by Aaron Amar and licensed under Creative Commons BY-SA 3.0.

![](/imgs/demo.png)