#Using Genetic Algorithm to search for the optimal variables (dataframe columns) in a dataset for machine learning regression/prediction
#Credits to pygad.readthedocs.io for PyGAD and the example on which this is based


import pygad
from os import getcwd
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from random import seed

last_fitness = None

#Print the latest information for every generation
def on_generation(ga_instance):
	global last_fitness
	print("Generation = {generation}".format(generation=ga_instance.generations_completed))
	print("Fitness    = {fitness}".format(fitness=ga_instance.best_solution(pop_fitness=ga_instance.last_generation_fitness)[1]))
	print("Change     = {change}".format(change=ga_instance.best_solution(pop_fitness=ga_instance.last_generation_fitness)[1] - last_fitness))
	last_fitness = ga_instance.best_solution(pop_fitness=ga_instance.last_generation_fitness)[1]

#Fitness function based on random forest classifier
def fitness_func(solution, solution_idx):
	#Data_df is the master copy of the data
	global data_df
	global label_df
	
	#Create a copy of the data_df
	new_df = data_df.copy()
	score = 0
	total = 0
	
	gene = list(solution)
	
	#Mutations of the gene will drop columns from the dataframe
	zero_indices = [i for i, x in enumerate(gene) if x == 0]
	new_df.drop(new_df.columns[zero_indices],axis=1,inplace=True)
	#If there are no columns left, set fitness to 0 i.e. dropping all columns is definitely not the optimal solution
	if(new_df.shape[1]==0):
		fitness = 0
		return fitness
    data_array = np.array(new_df)
	
	#Split the train and test data at a 90/10 ratio
	X_train, X_test, y_train, y_test = train_test_split(data_array,label_df['label'],test_size=0.10)
	y_test = list(y_test)
	pipe = RandomForestClassifier(n_jobs=-1).fit(X_train, y_train) #n_jobs=-1 enables multithreading speeding up the RF classifier
	predictions = pipe.predict(X_test)
	pred = list(predictions)
	
	#Calculating the fitness
	for _ in range(len(pred)):
		total += 1
		if(pred[_]==y_test[_]):
			score += 1	
	fitness = float(score/total)
	
	#Converting the gene from binary to decimal for display
	gene_dec = np.array2string(solution,separator="")
	gene_dec = gene_dec.replace('[','').replace(']','').replace('\n','').replace(' ','')
	gene_dec = int(gene_dec,2)
	print("%d	%.8f" %(gene_dec,fitness))
	return fitness

#Set seed so that train_test_split will be uniform
seed(0)

#Get the data and assign it to a dataframe
wd = getcwd()
data_file = wd + "\\train.csv"
data_df = pd.read_csv(data_file)
label_df = pd.DataFrame(data_df["label"])
data_df = data_df.drop(data_df.columns[0], axis=1)

#Initialized parameters
num_generations = 100 # Number of generations.
num_parents_mating = 10 # Number of solutions to be selected as parents in the mating pool.
sol_per_pop = 20 # Number of solutions in the population.
num_genes = data_df.shape[1] #Gene length is the number of columns in the dataframe
last_fitness = 0

#Setting the parameters for GA
ga_instance = pygad.GA(num_generations=num_generations,num_parents_mating=num_parents_mating,sol_per_pop=sol_per_pop,num_genes=num_genes,
fitness_func=fitness_func,on_generation=on_generation,init_range_low=1,init_range_high=1,random_mutation_min_val=0,random_mutation_max_val=2,
gene_type=int,mutation_by_replacement=True)

# Running the GA to optimize the parameters of the function.
ga_instance.run()

ga_instance.plot_fitness()

# Returning the details of the best solution.
solution, solution_fitness, solution_idx = ga_instance.best_solution(ga_instance.last_generation_fitness)
print("Parameters of the best solution : {solution}".format(solution=solution))
print("Fitness value of the best solution = {solution_fitness}".format(solution_fitness=solution_fitness))
print("Index of the best solution : {solution_idx}".format(solution_idx=solution_idx))

#prediction = np.sum(np.array(function_inputs)*solution)
#print("Predicted output based on the best solution : {prediction}".format(prediction=prediction))

if ga_instance.best_solution_generation != -1:
	print("Best fitness value reached after {best_solution_generation} generations.".format(best_solution_generation=ga_instance.best_solution_generation))

'''
# Saving the GA instance.
filename = 'genetic' # The filename to which the instance is saved. The name is without extension.
ga_instance.save(filename=filename)

# Loading the saved GA instance.
loaded_ga_instance = pygad.load(filename=filename)
loaded_ga_instance.plot_fitness()
	'''
