## What it does
### Snake Game
The snake game is a simple game, where the snake has to eat as much food as possible without dying. The snake can die by either colliding with the wall, or itself.

### AI
Hard coding a game like this can be difficult because there is not a set path to get to the food each time. The snake has to get to the food while avoiding its body, which is constantly moving as well. To make this easier, we can train a machine learning model to play in this environment.

## Q-Learning
### How it works
The idea behind reinforcement learning, or specifically in this case, q-learning, is that we can guide the agent by giving it a reward, or a punishment for certain actions. When the agent eats food, we can reward it, encourging similar actions in the future. Likewise, when the agent dies, we give it a negative reward, so that it does not repeat this action.

### Specific Details
