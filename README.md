# roguelikedev2019
This repository holds my work on [r/roguelikedev](https://www.reddit.com/r/roguelikedev/) summer dev-along following [The Complete Roguelike Tutorial](http://rogueliketutorials.com/tutorials/tcod/)

![RoguelikeDev Does the Complete Roguelike Tutorial Event Logo](https://i.imgur.com/3MAzEp1.png)

I am definitely not the target audience for this event. It's been over a decade since I wrote a game and I've never even played an ASCII roguelike before. I grew up with MUDs and text adventures then transitioned directly to Diablo clones and later Rogue Legacy. However, I really like the structured nature of this project, having a step-by-step guide to important features as well as the group sharing and accountability aspects. I think it's a great way to work on and finish a small project to get my feet wet in game development again so that's why I'm here.

In my brief research of Roguelikes I bounced off a bunch of games until I discovered [Dungeon Crawl Stone Soup](https://crawl.develz.org/). It has a fantastic tutorial and feels a bit more accessible for newcomers to the genre. My game is likely to draw a lot of inspiration from it.

## Game Features (Tentative Goals)
My goal is to produce a small but complete roguelike game with a Greek mythological theme drawing some inspiration from Mazes & Minotaurs and Titan Quest.

I will implement character classes: Hero (warrior) and Amazon (ranged/rogue) with Sorcerer/Sorceress (magic user) as a stretch goal. Each class will have some unique feature or ability to distinguish it from the others in addition to stats.

I will implement a basic equipment system (armor, weapons, potions) and loot drops.

The dungeon will feature multiple levels. Each level will be procedurally generated but have some scripted quest/features and a boss (think Diablo acts but smaller).

## Current Progress
* Very basic map and entity rendering is complete.
* Player movement is accomplished by arrow keys or WASD.

## Installing and Running the Game
1. pip install tcod
2. python engine.py from the source directory
