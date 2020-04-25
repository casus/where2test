##!/usr/bin/python

# Where2Test 
# Date : 25 April 2020

import sys
import pygeoj
import pygmo as pg

class TestOptimizer:
  num_districts = 0
  population = []
  total_population = 0
  num_positive = []
  total_num_positive = 0
  num_deaths = []
  total_num_deaths = 0
  num_recoveries = []
  total_num_recoveries = 0

  # Constructor
  def __init__(self, filename):
    self.readGeoJSON(filename)

  # Fitness function
  def fitness(self, x):
    f = []
    # Local effectiveness function to be defined below
    for i in range(self.num_districts):
      f.append( self.num_positive[i] / self.population[i])
    return f

  # Number of objective functions is same as number of districts
  def get_nobj(self):
    return self.num_districts

  # Define the lower and upper bounds for optimization
  def get_bounds(self):
    return ([0]*self.num_districts, self.population)

  # Human readable information about the class
  def get_name(self):
    return "Covid Test Optimizing function"


  #Read attributes from GeoJSON file
  def readGeoJSON(self, filename):
    jsonfile = pygeoj.load(filepath=filename)
    self.num_districts = len(jsonfile)
    for feature in jsonfile:
      ewz = feature.properties['EWZ']
      cases = feature.properties['cases']
      deaths = feature.properties['deaths']
      recovered = feature.properties['recovered']
      self.total_population += ewz
      self.population.append(ewz)
      self.total_num_positive += cases
      self.num_positive.append(cases)
      self.total_num_deaths += deaths
      self.num_deaths.append(deaths)
      #self.total_num_recoveries += recovered
      #self.num_recoveries.append(recovered)

def main(argv):
  help_message = 'test.py <inputfile> <outputfile>' 
  if len(argv) < 2:
    print(help_message)
    sys.exit(2)
  else:
    inputfile = argv[0]
    outputfile = argv[1]

  print("Reading data from "+inputfile)
  # Setting up the user defined problem in pygmo
  prob = pg.problem(TestOptimizer(inputfile))
  solution_size = 8
  # Start with an initial set of 100 sets
  pop = pg.population(prob, size = solution_size)
  # Set the algorithm to non-dominated sorting GA 
  algo = pg.algorithm(pg.nsga2(gen=40))
  # Optimize
  pop = algo.evolve(pop)

  # This returns a set of optimal vectors and corresponding fitness values
  fits, vectors = pop.get_f(), pop.get_x()
  
  print("Writing output to "+outputfile) 
  jsonfile = pygeoj.load(filepath=inputfile)
  num_districts = len(jsonfile)
  counter = 0
  for feature in jsonfile:
    for sol in range(solution_size):
      feature.properties = {"sol"+str(sol):str(vectors[sol][counter])}
    counter += 1
  # Save output
  jsonfile.save(outputfile);

if __name__ == "__main__":
  main(sys.argv[1:])
