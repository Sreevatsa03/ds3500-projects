"""
Created on Sun Nov  1 19:48:48 2020
@author: John Rachlin
@file: evo_v4.py: An evolutionary computing framework (version 4)
Assumes no Solutions class.
"""

import random as rand
import copy
from functools import reduce
import pickle

class Evo:

    def __init__(self):
        """ Population constructor """
        self.pop = {} # The solution population eval -> solution
        self.fitness = {} # Registered fitness functions: name -> objective function
        self.agents = {}  # Registered agents:  name -> (operator, num_solutions_input)

    def size(self):
        """ The size of the current population """
        
        size = len(self.pop)
        return size

    def add_fitness_criteria(self, name, f):
        """ Register a fitness criterion (objective) with the
        environment. Any solution added to the environment is scored 
        according to this objective """
        
        self.fitness[name] = f
        
    def add_agent(self, name, op, k=1):
        """ Register a named agent with the population.
        The operator (op) function defines what the agent does.
        k defines the number of solutions the agent operates on. """
        
        self.agents[name] = (op, k)

    def add_solution(self, sol):
        """ Add a solution to the population """
        
        eval = tuple((name, f(sol)) for name, f in self.fitness.items())
        self.pop[eval] = sol

    def run_agent(self, name):
        """ Invoke an agent against the population """
        
        op, k = self.agents[name]
        picks = self.get_random_solutions(k)
        new_sol = op(picks)
        self.add_solution(new_sol)

    def evolve(self, n=1, dom=100, status=100, sync=1000):
        """ Run n random agents (default=1) 
        dom defines how often we remove dominated (unfit) solutions
        status defines how often we display the current population """
        
        agent_names = list(self.agents.keys())
        for i in range(n):
            pick = rand.choice(agent_names)
            self.run_agent(pick)

            if i % sync == 0:
                # merge the saved solutions into my populations
                try:
                    with open('solutions.dat', 'rb') as file:
                        loaded = pickle.load(file)
                        for eval, sol in loaded.items():
                            self.pop[eval] = sol
                except Exception as e:
                    print(e)

                # remove dominated
                self.remove_dominated()

                # resave the population back to the disk
                with open('solutions.dat', 'wb') as file:
                    pickle.dump(self.pop, file)

            if i % dom == 0:
                self.remove_dominated()

            if i % status == 0:
                self.remove_dominated()
                print("Iteration:", i)
                print("Population size:", self.size())
                print(self)

        # clean up the population
        self.remove_dominated()

    def get_random_solutions(self, k=1):
        """ Pick k random solutions from the population """
        
        if self.size() == 0:
            return []
        else:
            solutions = tuple(self.pop.values())
            rand_sols = [copy.deepcopy(rand.choice(solutions)) for _ in range(k)]
            return rand_sols

    @staticmethod
    def _dominates(p, q):
        """ p = evaluation of solution: ((obj1, score1), (obj2, score2), ... )"""
        
        pscores = [score for _,score in p]
        qscores = [score for _,score in q]
        score_diffs = list(map(lambda x,y: y-x, pscores, qscores))
        min_diff = min(score_diffs)
        max_diff = max(score_diffs)
        return min_diff >= 0.0 and max_diff > 0.0

    @staticmethod
    def _reduce_nds(S, p):
        return S - {q for q in S if Evo._dominates(p, q)}

    def remove_dominated(self):
        """ Remove dominated solutions """
        
        nds = reduce(Evo._reduce_nds, self.pop.keys(), self.pop.keys())
        self.pop = {k: self.pop[k] for k in nds}

    def __str__(self):
        """ Output the solutions in the population """
        rslt = ""
        for eval,sol in self.pop.items():
            rslt += str(dict(eval))+":\t"+str(sol)+"\n"
        return rslt