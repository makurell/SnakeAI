# SnakeAI
Feed Forward Neural Networks evolving to play Snake

![](https://i.imgur.com/Eh5OaM4.gif)

- Code for the Neural Networks and Genetic Algorithms is [neuroga](https://github.com/makurell/neuroga).
- [snake.py](snake.py) - internal model of snake game (independent of graphics, etc)
- [engine.py](engine.py) - graphical front-end. Used to actually play snake game (or show a Neural Network playing the game in real time)
- [trainer.py](trainer.py) - run this script to run the Genetic Algorithm to train Neural Networks (will be saved in `model/` directory).
  - NB: trainer will interact with internal snake game model directly for performance reasons so there is no real-time graphics as it trains
  - will show graphs of progress, though (fitness-time and rate of fitness-time graphs)
- [notes.txt](notes.txt) - small notes I took for myself while developing this project

## Usage
You need to have Python 3 installed

Install numpy
```
python3 -m pip install numpy
```

Clone this repository
```
git clone https://github.com/makurell/SnakeAI.git
cd SnakeAI
```

Train
```
python3 train.py
```

Run engine to see Network in action
```
python3 engine.py
```
