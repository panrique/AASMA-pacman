from typing import List, Tuple
import numpy as np
import random
from BoardGame import *
from abc import ABC, abstractmethod

N_AGENTS = 4 # number of ghosts
ACTIONS = 4
GO_NORTH, GO_SOUTH, GO_WEST, GO_EAST = range(ACTIONS)
MOVEMENTS = 4 # number of directions
DOWN, LEFT, UP, RIGHT = range(MOVEMENTS)
N_UNITS = 4
ROLES = [GO_NORTH, GO_SOUTH, GO_WEST, GO_EAST]
CONVENTIONS = [[0, 1, 2, 3], ROLES]

class Agent(ABC):

    """
    Base agent class.
    Represents the concept of an autonomous agent.

    Attributes
    ----------
    name: str
        Name for identification purposes.

    observation: np.ndarray
       The most recent observation of the environment


    Methods
    -------
    see(observation)
        Collects an observation

    action(): int
        Abstract method.
        Returns an action, represented by an integer
        May take into account the observation (numpy.ndarray).

    References
    ----------
    ..[1] Michael Wooldridge "An Introduction to MultiAgent Systems - Second
    Edition", John Wiley & Sons, p 44.


    """

    def __init__(self, board_manager, name: str):
        self.board_manager = board_manager
        self.name = name
        self.observation = None
        self.current_action = None

    def see(self, observation: np.ndarray):
        # an observation is [a_i_row, a_i_col, target.row, target.col, pacman.row, 
        # pacman.col, self.board_manager.board.num, self.dead, self.attacked, self.ghostSpeed]
        self.observation = observation

    @abstractmethod
    def action(self, check) -> List[int]:
        raise NotImplementedError()

    """ return whether or not Pacman is on the line of sight of the agent """
    def seesPacman(self) -> bool:
        if self.observation == None:
            return False
        pacman_position = (self.observation[N_AGENTS * 2 + 2], self.observation[N_AGENTS * 2 + 3])
        return pacman_position != (-1, -1)

class RandomAgent(Agent):
    """
    Represents an agents that moves randomly.
    """

    def __init__(self, board_manager, agent_id):
        super(RandomAgent, self).__init__(board_manager, "Random Agent")
        #self.n_actions = N_ACTIONS
        self.agent_id = agent_id

    def action(self, check) -> List[int]:
        if self.observation == None:
            return GetRandomTarget()

        row, col = self.observation[self.agent_id * 2], self.observation[self.agent_id * 2 + 1]
        target = (self.observation[N_AGENTS * 2], self.observation[N_AGENTS * 2 + 1])
        dead = self.observation[N_AGENTS * 2 + 5] == 1

        # specific game constraints
        if not check or target == (-1, -1) or (row == target[0] and col == target[1]) or \
            self.board_manager.board[int(row)][int(col)] == 4 or dead:
            return GetRandomTarget()
        return target

class GreedyAgent(Agent):

    """
    The greedy agent finds the nearest prey and moves towards it.
    """

    def __init__(self, board_manager, agent_id):
        super(GreedyAgent, self).__init__(board_manager, "Greedy Agent")
        self.agent_id = agent_id

    def action(self, check) -> List[int]:
        if self.observation == None:
            return GetRandomTarget()

        pacman_position = (self.observation[N_AGENTS * 2 + 2], self.observation[N_AGENTS * 2 + 3])
        row, col = self.observation[self.agent_id * 2], self.observation[self.agent_id * 2 + 1]
        target = (self.observation[N_AGENTS * 2], self.observation[N_AGENTS * 2 + 1])
        dead = self.observation[N_AGENTS * 2 + 5] == 1

        # specific game constraints plus greedy constraint: (pacman_position != (-1, -1))
        if not check or pacman_position != (-1, -1) or target == (-1, -1) or (row == target[0] and col == target[1]) \
            or self.board_manager.board[int(row)][int(col)] == 4 or dead:
            # If agent does not see Pacman, move randomly
            if pacman_position == (-1, -1):
                return GetRandomTarget()
            
            return pacman_position

        return target


class CoordinatedAgent(Agent):

    """
    This type of agents use specific direction (N, S, W, E) conditions to set a target.
    CoordinatedAgent is the superclass of both ConventionAgent (social conventions) and RoleAgent (roles)
    """

    def __init__(self, board_manager, name: str):
        super(CoordinatedAgent, self).__init__(board_manager, name)

    # N, S, W, E
    def get_prey_adj_locs(self, loc: Tuple) -> List[Tuple]:
        prey_x = loc[0]
        prey_y = loc[1]

        # in case pacman is about to go through the middle tunnel
        if (prey_x == 17) and ((prey_y <= N_UNITS - 1) or (prey_y >= (len(self.board_manager.board[0]) - N_UNITS))):
            if prey_y <= N_UNITS - 1:
                return [(prey_x - N_UNITS, prey_y), (prey_x + N_UNITS, prey_y), \
                        (prey_x, len(self.board_manager.board[0]) - N_UNITS), (prey_x, prey_y + N_UNITS)]
            return [(prey_x - N_UNITS, prey_y), (prey_x + N_UNITS, prey_y), \
                    (prey_x, prey_y - N_UNITS), (prey_x, N_UNITS)]

        return [(prey_x - N_UNITS, prey_y), (prey_x + N_UNITS, prey_y), (prey_x, prey_y - N_UNITS), (prey_x, prey_y + N_UNITS)]

    def advance_to_pos(self, agent_pos: Tuple, prey_pos: Tuple, agent_dest: int) -> int:
        """
        Choose movement action to advance agent towards the destination around prey

        :param agent_pos: current agent position
        :param prey_pos: prey position
        :param agent_dest: agent destination in relation to prey (0 for NORTH, 1 for SOUTH,
                            2 for WEST, and 3 for EAST)

        :return: movement index
        """
        # If it is close enough, simply return pacman position
        if self.seesPacman() and calcDistance(prey_pos, agent_pos) <= N_UNITS:
            return prey_pos

        prey_adj_locs = self.get_prey_adj_locs(prey_pos)
        return prey_adj_locs[agent_dest]

class ConventionAgent(CoordinatedAgent):

    def __init__(self, board_manager, agent_id: int, social_conventions: List):
        super(ConventionAgent, self).__init__(board_manager, "Convention Agent")
        self.agent_id = agent_id
        self.n_agents = N_AGENTS
        self.conventions = social_conventions
        self.n_actions = ACTIONS

    def action(self, check) -> List[int]:
        if self.observation == None:
            return GetRandomTarget()

        pacman_position = (self.observation[N_AGENTS * 2 + 2], self.observation[N_AGENTS * 2 + 3])
        row, col = self.observation[self.agent_id * 2], self.observation[self.agent_id * 2 + 1]
        target = (self.observation[N_AGENTS * 2], self.observation[N_AGENTS * 2 + 1])
        dead = self.observation[N_AGENTS * 2 + 5] == 1

        if not check or pacman_position != (-1, -1) or target == (-1, -1) or \
            (row == target[0] and col == target[1]) or self.board_manager.board[int(row)][int(col)] == 4 or dead:
            agent_order = self.conventions[0]
            action_order = self.conventions[1]
            agent_dest = action_order[agent_order.index(self.agent_id)]
            if pacman_position == (-1, -1):
                return GetRandomTarget(agent_dest)

            agent_pos = (row, col)
            return self.advance_to_pos(agent_pos, pacman_position, agent_dest)

        return target


class RoleAgent(CoordinatedAgent):

    def __init__(self, board_manager, agent_id: int, roles: List, role_assign_period: int = 1):
        super(RoleAgent, self).__init__(board_manager, "Role-based Agent")
        self.agent_id = agent_id
        self.n_agents = N_AGENTS
        self.roles = roles
        self.role_assign_period = role_assign_period
        self.curr_role = None
        self.steps_counter = 0

    def potential_function(self, agent_pos: Tuple, prey_pos: Tuple, role: int):
        """
        Calculates the potential function used for role assignment.
        The potential function consists of the negative Manhattan distance between the
        `agent_pos` and the target position of the given `role` (which corresponds
        to a position that is adjacent to the position of pacman).

        :param agent_pos: agent position
        :param prey_pos: pacman position
        :param role: role

        :return: (float) potential value
        """
        prey_adj_locs = self.get_prey_adj_locs(prey_pos)
        role_target_pos = prey_adj_locs[role]

        return -sum(abs(np.array(role_target_pos) - np.array(agent_pos)))

    def role_assignment(self):
        """
        Given the observation vector containing the positions of all ghosts
        and pacman, compute the role-assignment for each of the agents.

        :return: a list with the role assignment for each of the agents
        """
        pacman_position = (self.observation[N_AGENTS * 2 + 2], self.observation[N_AGENTS * 2 + 3])
        if pacman_position == (-1, -1):
            # Default attribution of roles when pacmans location is unknown - agent_i gets role_i,
            return range(ACTIONS)

        # Calculate potentials for all agents and roles.
        potentials = np.zeros((len(self.roles), self.n_agents))
        for (role_idx, role) in enumerate(self.roles):
            for agent in range(self.n_agents):
                agent_pos = (self.observation[agent * 2], self.observation[agent * 2 + 1])
                potentials[role_idx,agent] = self.potential_function(agent_pos, pacman_position, role)

        agents_roles = np.zeros(self.n_agents, dtype=np.int32)
        for (role_idx, role) in enumerate(self.roles):
            agent_id = np.argmax(potentials[role_idx])
            agents_roles[agent_id] = role
            potentials[:,agent_id] = -math.inf

        return agents_roles

    def action(self, check) -> List[int]:
        if self.observation == None:
            return GetRandomTarget()

        pacman_position = (self.observation[N_AGENTS * 2 + 2], self.observation[N_AGENTS * 2 + 3])
        row, col = self.observation[self.agent_id * 2], self.observation[self.agent_id * 2 + 1]
        target = (self.observation[N_AGENTS * 2], self.observation[N_AGENTS * 2 + 1])
        dead = self.observation[N_AGENTS * 2 + 5] == 1

        # specific game constraints plus greedy constraint: (pacman_position != (-1, -1))
        if not check or pacman_position != (-1, -1) or target == (-1, -1) or \
            (row == target[0] and col == target[1]) or self.board_manager.board[int(row)][int(col)] == 4 or dead:

            # Compute potential-based role assignment every `role_assign_period` steps.
            if self.curr_role is None or self.steps_counter % self.role_assign_period == 0:
                role_assignments = self.role_assignment()
                self.curr_role = role_assignments[self.agent_id]

            if pacman_position == (-1, -1):
                # gets random target based on role
                return GetRandomTarget(self.curr_role)

            agent_pos = (row, col)
            self.steps_counter += 1
            #dir, mov = getDir()
            return self.advance_to_pos(agent_pos, pacman_position, self.curr_role)

        return target
