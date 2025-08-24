# burning_forest
This is a little project created during my studies. 
It is a simple simulation created in Python.
The goal of this project is to represent a cellular automaton of a burning forest.
The rules of the simulation are:
- the tree becomes a burning tree with the possibility of **p** if it has a neighbouring burning tree
- burning tree becomes burned out tree in the next generation
- burned out tree renews itself after **k** iterations
- self ignition of a tree occurs with possibility **ps**(very low)
- include water that works as a barrier against the fire
- include the wind condition that will change the possibility of a fire in different directions. Direction shall be changed after a few iterations

The file includes four classes:
- NodeState - a class that is working as a enumerator to hold the states of a Node
- WindDirerctions - class for storing the wind values
- Node - class representing a tree or a water
- World - the main "board" containing a specific number of nodes

To execute the program you must do the following steps:
- install Python from the official site <a href = "https://www.python.org/">here</a>
- in the catalog with the project you must create a virtual environment by typing `python -m venv venv` in the console
- activate the virtual environment via the command:
  - Windows: `venv/scripts/Activate`
  - MacOS/Linux: source `venv/bin/activate`
- install the numpy library: `pip install numpy`
- execute the simulation via `python simulation.exe`

Feel free to experiment with it.
