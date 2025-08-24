from typing import List, Tuple
import random
import time
import numpy as np


class NodeState:
    TREE: str = "tree"
    BURNING_TREE: str = "burning_tree"
    BURNED_OUT_TREE: str = "burned_out_tree"
    WATER: str = "water"


class WindDirections:
    NORTH: str = "north ↑"
    SOUTH: str = "south ↓"
    EAST: str = "east →"
    WEST: str = "west ←"


class Node:
    def __init__(self) -> None:
        self.initialize_states: List[str] = [NodeState.TREE, NodeState.WATER]
        self.current_state: str = np.random.choice(self.initialize_states, p=[0.9, 0.1])
        self.rebirth_timer = 0

    def ignite(self) -> None:
        if self.current_state == NodeState.TREE:
            self.current_state = NodeState.BURNING_TREE

    def burn_out(self) -> None:
        if self.current_state == NodeState.BURNING_TREE:
            self.current_state = NodeState.BURNED_OUT_TREE

    def increment_rebirth_timer(self, number) -> None:
        self.rebirth_timer += number

    def reset_rebirth_timer(self) -> None:
        self.rebirth_timer = 0

    def rebirth(self) -> None:
        if self.current_state == NodeState.BURNED_OUT_TREE:
            self.current_state = NodeState.TREE
            self.rebirth_timer = 0


class World: 
    def __init__(self, rows: int = 5, cols: int = 5, ignition_probability: float = 1.0, k: int = None, self_ignition_probability: int = 0.05) -> None:
        self.li: List[List[Node]] = []
        self.ignition_probability: float = ignition_probability
        self.rows: int = rows
        self.cols: int = cols
        self.k: int = k
        self.self_ignition_probability = self_ignition_probability
        self.wind_directions = [WindDirections.NORTH, WindDirections.SOUTH, WindDirections.EAST, WindDirections.WEST]
        self.wind_direction = random.choice(self.wind_directions)
        self.wind_effect = {
            WindDirections.NORTH: {"north": 0.5, "south": 1.5, "east": 1.0, "west": 1.0},
            WindDirections.SOUTH: {"north": 1.5, "south": 0.5, "east": 1.0, "west": 1.0},
            WindDirections.EAST: {"north": 1.0, "south": 1.0, "east": 0.5, "west": 1.5},
            WindDirections.WEST: {"north": 1.0, "south": 1.0, "east": 1.5, "west": 0.5},
        }

    def create_world(self) -> None:
        for _ in range(self.rows):
            row: List[Node] = []
            for _ in range(self.cols):
                node = Node()
                row.append(node)
            self.li.append(row)

    def get_node(self, row: int, col: int) -> Node:
        return self.li[row][col]

    def get_new_ignitions(self) -> List[Tuple[int, int]]:
        next_ignitions: List[Tuple[int, int]] = []
        for row in range(len(self.li)):
            for col in range(len(self.li[row])):
                selected_node: Node = self.li[row][col]
                if selected_node.current_state == NodeState.TREE:
                    neighbors: List[Tuple[int, int, float]] = []
                    
                    # Góra
                    if row > 0:
                        neighbors.append((row - 1, col, self.wind_effect[self.wind_direction]["north"]))
                    
                    # Dół
                    if row < self.rows - 1:
                        neighbors.append((row + 1, col, self.wind_effect[self.wind_direction]["south"]))
                    
                    # Lewo
                    if col > 0:
                        neighbors.append((row, col - 1, self.wind_effect[self.wind_direction]["west"]))
                    
                    # Prawo
                    if col < self.cols - 1:
                        neighbors.append((row, col + 1, self.wind_effect[self.wind_direction]["east"]))
                    
                    for neighbor_row, neighbor_col, wind_modifier in neighbors:
                        neighbor = self.li[neighbor_row][neighbor_col]
                        if neighbor.current_state == NodeState.BURNING_TREE:
                            adjusted_probability = min(self.ignition_probability * wind_modifier, 1)
                            if random.random() < adjusted_probability:
                                next_ignitions.append((row, col))
                                break
        return next_ignitions

    def extinguish_old_fire(self) -> None:
        for row in self.li:
            for node in row:
                if node.current_state == NodeState.BURNING_TREE:
                    node.burn_out()

    def burn_new_trees(self, ignition_list: List[Tuple[int, int]]) -> None:
        for row, col in ignition_list:
            node: Node = self.get_node(row, col)
            node.ignite()

    def check_rebirth_timers(self) -> None:
        if self.k is not None:
            for row in range(len(self.li)):
                for col in range(len(self.li[row])):
                    node: Node = self.get_node(row, col)
                    if node.rebirth_timer >= self.k and node.current_state == NodeState.BURNED_OUT_TREE:
                        node.rebirth()

    def increment_rebirth_timers(self) -> None:
        for row in range(len(self.li)):
            for col in range(len(self.li[row])):
                node: Node = self.get_node(row, col)
                if node.current_state == NodeState.BURNED_OUT_TREE:
                    node.increment_rebirth_timer(1)

    def ignite_random_tree(self) -> None:
        while True:
            row: List[Node] = random.choice(self.li)
            node: Node = random.choice(row)
            if node.current_state == NodeState.TREE:
                node.ignite()
                break

    def check_world_still_burning(self) -> bool:
        for row in range(len(self.li)):
            for col in range(len(self.li[row])):
                if self.li[row][col].current_state == NodeState.BURNING_TREE:
                    return True
        return False

    def check_self_ignition(self) -> None:
        if random.random() < self.self_ignition_probability:
            self.ignite_random_tree()

    def change_wind_direction(self) -> None:
        current_wind_direction = self.wind_direction
        avaliable_wind_directions = self.wind_directions.copy()
        avaliable_wind_directions.remove(current_wind_direction)
        self.wind_direction = random.choice(avaliable_wind_directions)
        print(f"Wind direction changed to: {self.wind_direction}")

    def begin_simulation(self) -> None:
        sim_step: int = 0
        self.create_world()
        print("Generated world:\n", self)
        time.sleep(1)
        self.ignite_random_tree()
        print("Beginning first ignition:\n", self)
        time.sleep(1)
        trees_burned_out: bool = False
        while not trees_burned_out:
            new_ignitions: List[Tuple[int, int]] = self.get_new_ignitions()
            self.extinguish_old_fire()
            self.burn_new_trees(new_ignitions)
            self.check_self_ignition()
            self.check_rebirth_timers()

            if sim_step % 10 == 0:
                self.change_wind_direction()

            if not self.check_world_still_burning():
                trees_burned_out = True
            self.increment_rebirth_timers()
            sim_step += 1
            print(f"Step {sim_step}\n Wind direction: {self.wind_direction}\n", self)
            time.sleep(1)
        print("End of simulation")
        
    def __str__(self) -> str:
        state_map: dict = {
            NodeState.TREE: "\033[92mT\033[0m",
            NodeState.BURNING_TREE: "\033[91mB\033[0m",
            NodeState.BURNED_OUT_TREE: "\033[90mD\033[0m",
            NodeState.WATER: "\033[94mW\033[0m"
        }
        result: str = ""
        for row in self.li:
            result += " ".join(state_map[node.current_state] for node in row) + "\n"
        return result


world = World(3, 3, 0.5, 10)
world.begin_simulation()