ABDULLAH BUTT


Enchanted Forest Treasure Hunt
Overview
The Enchanted Forest Treasure Hunt is a Python simulation that challenges players to navigate through a dangerous forest in search of hidden treasure. Utilizing the power of Pygame for graphics and animations, the game represents the forest as a dynamically generated grid where players must avoid wild animals, overcome obstacles, and ultimately find the treasure to win. This implementation includes both the Uniform Cost Search (UCS) and A* Search algorithms to provide two strategies for pathfinding through the forest.

Features
Dynamic Grid Generation: The forest is represented as an 8x8 grid, with elements randomly placed to ensure a unique experience every playthrough.
Pathfinding Algorithms: Implements UCS and A* Search algorithms to find the optimal path to the treasure.
Interactive Visuals: Utilizes Pygame for drawing the grid, obstacles, animals, and the player on the screen, providing an immersive experience.
Obstacles and Animals: Simulates the challenge of navigating through a forest filled with wild animals and physical obstacles.
Dependencies
Python 3.x
Pygame

Ensure you have Python installed on your system. Pygame is required to run the simulation and can be installed via pip:

#Bash
pip install pygame

How to Run
Clone or download this repository to your local machine.
Navigate to the folder containing the script.
Run the script using Python:
bash
python enchanted_forest_treasure_hunt.py
The game window will open. 
You can choose between the UCS and A* Search algorithms to start the simulation.
The player's path through the forest will be visualized, demonstrating the chosen algorithm's approach to finding the treasure.

Gameplay Instructions
Upon launching the game, you will see two buttons: "A*" and "UCS". 
Click on either to start the simulation with the corresponding pathfinding algorithm.
The grid represents the forest. Each tile may contain an obstacle, an animal, or be a safe path.
The simulation will automatically navigate the player through the forest based on the chosen pathfinding algorithm.
Watch as the player moves through the forest, avoiding dangers and seeking the treasure.

Implementation Details
Player Movement: The player can move left, right, up, or down to adjacent grids, with each movement incurring a cost.
Dynamic Elements Handling: Wild animals and obstacles are randomly placed in the forest. The game dynamically adjusts the player's path based on these elements.
Pathfinding Algorithms:

UCS: Explores paths with the lowest cumulative cost, ignoring the distance to the goal.

A Search*: Combines the cost to reach a node and an estimate of the cost to the goal, prioritizing paths that appear to lead closer to the treasure.

Optimizations
This implementation prioritizes efficient pathfinding through dynamic grid generation and adaptive path adjustment based on encountered obstacles and animals. The use of Pygame ensures smooth rendering and interaction.

Test Cases
Various grid configurations with different placements of animals and obstacles.
Scenarios where the player must backtrack due to encountering an impenetrable barrier.
Cases with high density of obstacles and animals to test the algorithms' ability to find a path.
Contribution
This project was developed as a collaborative effort. The responsibilities were divided as follows:

Algorithm Implementation: Member 1 focused on implementing the UCS and A* Search algorithms.
Pygame Visualization: Member 2 was responsible for creating the graphical representation of the game using Pygame.
Testing and Optimization: Both members contributed to testing and optimizing the code for better performance and reliability.

This README provides a comprehensive guide to your Enchanted Forest Treasure Hunt game, outlining the purpose, features, instructions, and implementation details to help users understand and run the simulation successfully.
