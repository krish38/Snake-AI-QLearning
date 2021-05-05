## What it does
### Snake Game
The snake game is a simple game, where the snake has to eat as much food as possible without dying. The snake can die by either colliding with the wall, or itself.

### AI
Hard coding a game like this can be difficult because there is not a set path to get to the food each time. The snake has to get to the food while avoiding its body, which is constantly moving as well. To make this easier, we can train a machine learning model to play in this environment.

## Q-Learning
### How it works
The idea behind reinforcement learning, or specifically in this case, q-learning, is that we can guide the agent by giving it a reward, or a punishment for certain actions. When the agent eats food, we can reward it, encourging similar actions in the future. Likewise, when the agent dies, we give it a negative reward, so that it does not repeat this action. The agent makes its decisions from a table, known as a q-table. The q-table stores every possible state of the board (with the parameters we pass it), along with each action that can be made at that state. Each action at each state, is given a q-value, which is the expected reward for performing set action at set state. This q-table is updated as the agent trains in the environment using this equation:

![Q-learning Equation](https://www.kdnuggets.com/images/reinforcement-learning-fig2-666.jpg)

### Specific Details
The state includes 8 boolean values:
  - Is the food above the snake?
  - Is the food to the right of the snake?
  - Is the food below the snake?
  - Is the food to the left the snake?
  - Is the cell above the snake head dangerous?
  - Is the cell to the right of the snake head dangerous?
  - Is the cell below the snake head dangerous?
  - Is the cell to the left of the snake head dangerous?
