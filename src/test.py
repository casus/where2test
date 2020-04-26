##!/usr/bin/python

# Where2Test 
# Date : 25 April 2020

import sys
import pygeoj
import pygmo as pg

class TestOptimizer:
  max_kits = 5000
  num_districts = 0
  population = []
  total_population = 0
  density = []
  num_positive = []
  total_num_positive = 0
  num_deaths = []
  total_num_deaths = 0
  num_recoveries = []
  total_num_recoveries = 0
  thuenen_type = []
  mortality_rate = []
  total_mortality_rate = 0
  # NOTE: The following data are not yet retrieved from any dataset
  num_hospitals = []
  total_num_hospitals = 0
  num_tests = []
  total_tests = 0
  area = []
  total_area = 0

  # Constructor
  def __init__(self, filename, maxkits=5000):
    self.readGeoJSON(filename)
    self.max_kits = maxkits

  # Objective function to be optimized
  # Constraint is passed as another objective function
  #def fitness(self, x):
  #  f = []
  #  total_kits = 0
    # Local effectiveness function for each district to be defined below
  #  for i in range(self.num_districts):
  #    #f.append( (self.num_hospitals[i]*self.population[i]*self.num_tests[i]+x[i])*total_area / self.population[i])
  #    f.append( ((self.mortality_rate[i] / self.total_mortality_rate) - (x[i] / self.max_kits))**2)
  #    total_kits += x[i]

    # The constraint on the global number of testing kits
  #  f.append((total_kits - self.max_kits))
  #  return f

  # Single objective function with equality constraint
  def fitness(self, x):
    obj = 0
    total_kits = 0
    for i in range(self.num_districts):
      obj += (((self.mortality_rate[i] / self.total_mortality_rate) - (x[i] / self.max_kits)))*self.population[i]/self.total_population
      total_kits += x[i]      

    # The constraint on the global number of testing kits
    ce1 = (total_kits - self.max_kits)
    return [obj, ce1]

  # Number of objective functions is number of districts + one constraint
  def get_nobj(self):
    #return (self.num_districts)
    return 1

  # Number of inequality constraints
  def get_nic(self):
    return 0

  # Number of equality constraints
  def get_nec(self):
    return 1

  # Define the lower and upper bounds for optimization
  def get_bounds(self):
    return ([0]*self.num_districts, [self.max_kits]*self.num_districts)

  # Human readable information about the class
  def get_name(self):
    return "Covid Test Optimizing function"


  #Read attributes from GeoJSON file
  def readGeoJSON(self, filename):
    jsonfile = pygeoj.load(filepath=filename)
    self.num_districts = len(jsonfile)
    for feature in jsonfile:
      residents = feature.properties['EWZ']
      cases = feature.properties['cases']
      deaths = feature.properties['deaths']
      recovered = feature.properties['recovered']
      area = feature.properties['KFL']                  #in km²
      mortality_rate = feature.properties['death_rate']

      #t_type = feature.properties['Thünen-Typ']         #indicator if the area is rural and has low economy
      self.total_population += residents
      self.population.append(residents)
      self.total_num_positive += cases
      self.num_positive.append(cases)
      self.total_num_deaths += deaths
      self.num_deaths.append(deaths)
      self.total_mortality_rate += mortality_rate
      self.mortality_rate.append(mortality_rate)
      #self.thuenen_type.append(t_type)
      # recovered information currently not available in the dataset
      #self.total_num_recoveries += recovered
      #self.num_recoveries.append(recovered)
      # Area information is not available for all
      #self.total_area += area
      #self.area.append(area)
      #self.density.append((residents/area))

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
  solution_size = 10000
  # Start with an initial set of 100 sets
  pop = pg.population(prob, size = solution_size)
  # Set the algorithm to non-dominated sorting GA 
  algo = pg.algorithm(pg.gaco(gen=40))
  # Optimize
  pop = algo.evolve(pop)

  # This returns a set of optimal vectors and corresponding fitness values
  fits, vectors = pop.get_f(), pop.get_x()
  
  for i in range(len(vectors)):
    print("solution " + str(i))
    total = 0
    for j in range(len(vectors[i])):
      total += int(vectors[i][j])
    print("Total tests = " + str(total))

  print("Writing output to "+outputfile) 
  jsonfile = pygeoj.load(filepath=inputfile)
  num_districts = len(jsonfile)
  counter = 0
  for feature in jsonfile:
    for sol in range(solution_size):
      feature.properties["sol"+str(sol)] = str(int(vectors[sol][counter]));
    counter += 1
  # Save output
  jsonfile.save(outputfile);

  print(vectors)

if __name__ == "__main__":
  main(sys.argv[1:])
