"""
Class Node:
    - state: current game state including all player attributes
    - parent: pointer to parent node
    - children: list of child nodes
    - wins: number of wins from this node
    - visits: number of visits to this node
    - untried_actions: actions that haven't been tried from node
"""

"""
Function MCTS(root_state, iterations):
    - root_node = Node(state=root_state)
    - for i in range(iterations):
        node = root_node
        state = copy of root_state
        
        // Selection
        while node has no untried actions and node has children:
            node = node with highest UCB1 score based on wins/visits
            state = apply action to state based on node's action
            
        // Expansion
        if node has untried actions:
            action = select an untried action
            new_state = apply action to state
            node = add a new child node to node with new_state, parent=node, action leading to new_state
            
        // Simulation
        while state is not terminal:
            state = simulate random action from state
            
        // Backpropagation
        while node is not None:
            node.visits += 1
            if node's player wins in state:
                node.wins += 1
            node = node.parent
            
    - return action of the child of root_node with the highest win ratio

Function simulate_action(state, action):
    - Apply action to state, considering all player attributes and rules
    - return new_state

Function is_terminal(state):
    - Check if a player's HP <= 0 or if game duration reached
    - return True if game ended, else False

Function UCB1(node):
    - Calculate and return (estimated mean reward + exploration bonus) score based on node wins, visits, and parent visits
"""