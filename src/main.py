from solver import *
import numpy
import crossover
import mutation
from datetime import datetime
import time
from tabulate import tabulate

'''
Different things to try out: 
Increase number of offsprings of each generation (mu) or tournamen Size
Increase population Size
Increase Number of Generations
Increase population Size
(minor: Change the maxFitness and componentCost)
'''
settingB1 = ParameterSetting(maxFitIndiv = 500, popSize = 10, mateProb = 0.9, 
mutateProb = 0.02, tournSize = 10, numGens = 100, componentCost = 20, mu=10, 
hofSize = 100, number_of_runs = 10, verbose = True, 
crossoverFunction = crossover.onePointCrossover, 
mutationFunction = mutation.multFlipBit)

settingB2 = ParameterSetting(maxFitIndiv = 1000, popSize = 10, mateProb = 0.9, 
mutateProb = 0.02, tournSize = 20, numGens = 10, componentCost = 50, mu=10, 
hofSize = 10, number_of_runs = 2, verbose = False, 
crossoverFunction = crossover.onePointCrossover, 
mutationFunction = mutation.multFlipBit)

settingC1 = ParameterSetting(maxFitIndiv = 10000, popSize = 100, mateProb = 0.9, 
mutateProb = 0.02, tournSize = 10, numGens = 150, componentCost = 50, mu=20, 
hofSize = 150, number_of_runs = 10, verbose = True, 
crossoverFunction = crossover.onePointCrossover, 
mutationFunction = mutation.multFlipBit)

settingD1 = ParameterSetting(maxFitIndiv = 30000, popSize = 200, mateProb = 0.9, 
mutateProb = 0.02, tournSize = 10, numGens = 200, componentCost = 70, mu=30, 
hofSize = 200, number_of_runs = 5, verbose = True, 
crossoverFunction = crossover.onePointCrossover, 
mutationFunction = mutation.multFlipBit)

settingE1 = ParameterSetting(maxFitIndiv = 50000, popSize = 300, mateProb = 0.9, 
mutateProb = 0.02, tournSize = 10, numGens = 300, componentCost = 100, mu=40, 
hofSize = 300, number_of_runs = 2, verbose = True, 
crossoverFunction = crossover.onePointCrossover, 
mutationFunction = mutation.multFlipBit)


settings = [settingB2]
setting_names = ["SettingB2"]

filesB = ["../data/B/b01","../data/B/b02","../data/B/b03","../data/B/b04","../data/B/b05","../data/B/b06","../data/B/b07","../data/B/b08","../data/B/b09",
"../data/B/b10","../data/B/b11","../data/B/b12","../data/B/b13","../data/B/b14","../data/B/b15","../data/B/b16","../data/B/b17","../data/B/b18"]
filesC = ["data/C/c01","data/C/c02","data/C/c03","data/C/c04","data/C/c05","data/C/c06","data/C/c07","data/C/c08","data/C/c09",
"data/C/c10","data/C/c11","data/C/c12","data/C/c13","data/C/c14","data/C/c15","data/C/c16","data/C/c17","data/C/c18", "data/C/c19","data/C/c20"]
filesD = ["data/D/d01","data/D/d02","data/D/d03","data/D/d04","data/D/d05","data/D/d06","data/D/d07","data/D/d08","data/D/d09",
"data/D/d10","data/D/d11","data/D/d12","data/D/d13","data/D/d14","data/D/d15","data/D/d16","data/D/d17","data/D/d18", "data/D/d19","data/D/d20"]
filesE = ["data/E/e01","data/E/e02","data/E/e03","data/E/e04","data/E/e05","data/E/e06","data/E/e07","data/E/e08","data/E/e09",
"data/E/e10","data/E/e11","data/E/e12","data/E/e13","data/E/e14","data/E/e15","data/E/e16","data/E/e17","data/E/e18","data/E/e19","data/E/e20"]

optB = [82,83,138,59,61,122,111,104,220,86,88,174,165,235,318,127,131,218]
optC = [85,144,754,1079,1579,55,102,509,707,1093,32,46,258,323,556,11,18,113,146,267]
optD = [106,220,1565,1935,3250,67,103,1072,1448,2110,29,42,500,667,1116,13,23,223,310,537]
optE = [111,214,4013,5101,8128,73,145,2640,3604,5600,34,67,1280,1732,2784,15,25,564,758,1342]

files = filesB
dataset_name = "filesB"

solutions = optB


#Runs the solver with all setting on all files and saves the best_individuals 

def truncate(f, n):
    '''Truncates/pads a float f to n decimal places without rounding'''
    s = '{}'.format(f)
    if 'e' in s or 'E' in s:
        return '{0:.{1}f}'.format(f, n)
    i, p, d = s.partition('.')
    return '.'.join([i, (d+'0'*n)[:n]])



for setting_counter, setting in enumerate(settings): 
    print(setting.crossoverFunction.__name__)
    solver = SteinerTreeSolver(setting)
    print("Working with the %sth setting..." % (setting_counter + 1))
    
    '''
    For us, the best individual is the one with the the lowest weight among 
    those with only one component. If we don't have any such individual, we 
    take the one with the highest weight among those with two components and so on
    I.e., we virtually set the componentCost to Infinity, since we actually really want 
    to have a tree in the end
    '''
    
    best_individuals = [[[None, 0, 0, 0] for _ in range(setting.number_of_runs)] for __ in range(len(files))]

    '''
    Average of the best individuals among all setting.number_of_runs test runs, including file name, avg of weight, avg of comps, and avg of time
    Stdev includes name of file, stdev of weights and stdev of number of components
    best includes best individual regarding all test runs (first we consider a low number of components, then the weight)
    '''
    avg = [[None, 0, 0, 0]] * len(files)
    stdev = [[None, 0, 0]] * len(files)
    best = [[None, 0, 0]] * len(files)
    worst = [[None, 0, 0]] * len(files)

    
    for file_counter, file in enumerate(files):
    
        graph = SteinerInstance(file + ".stp")
        #print("graph:%s ", graph)
        print("Working on problem %s" % (file))
        
        start_time = time.time()
        
        for run_counter in range(setting.number_of_runs):
            print("\nsolving it for the %sth time..." % (run_counter + 1))
            pop, hof = solver.solve(graph, output_stats = True, output_plot = False, filename = "plots/" + file[-3:] + "_" + setting_names[setting_counter] + "_run=" + str(run_counter + 1) + ".png")    
    
            print("Presenting the %s best individuals of the problem %s:\ni-th.best\tfitness\t\tweight\t\tcomponents\n" % (setting.hofSize, file))
            '''Here, we also calculate the best individual'''
            index_best = 0
            weight_best, cnt_best = mst(graph, solver.reassemble(hof[0], graph.allowed_vertices))
            
            for i in range(setting.hofSize):
                weight, cnt = mst(graph, solver.reassemble(hof[i], graph.allowed_vertices))
                if cnt < cnt_best or (cnt == cnt_best and weight < weight_best):
                    index_best, weight_best, cnt_best = i, weight, cnt
                print("%s\t\t%s\t%s\t\t%s" % ((i+1), hof[i].fitness, weight, cnt))
            
            #print("filecounter=%s, runcounter=%s" %(file_counter, run_counter))
            best_individuals[file_counter][run_counter] = [file, weight_best, cnt_best, hof[index_best]]

        end_time = time.time()
        average_time = (end_time - start_time) / setting.number_of_runs
        print("Average time: ", average_time)

        '''
        Calculating the average and stdev of the best individuals over all test runs
        '''
        best_individuals_weights = [best_individuals[file_counter][run][1] for run in range(setting.number_of_runs)]
        best_individuals_cnts = [best_individuals[file_counter][run][2] for run in range(setting.number_of_runs)]
        avg[file_counter] = [file, numpy.average(best_individuals_weights), numpy.average(best_individuals_cnts), average_time]
        stdev[file_counter] = [file, numpy.std(best_individuals_weights), numpy.std(best_individuals_cnts)]
        
        best_overall_weight, best_overall_cnt = best_individuals_weights[0], best_individuals_cnts[0]
        
        for i in range(setting.number_of_runs):
            if best_individuals_cnts[i] < best_overall_cnt or (best_individuals_cnts[i] == best_overall_cnt and best_individuals_weights[i] < best_overall_weight):
                best_overall_weight, best_overall_cnt = best_individuals_weights[i], best_individuals_cnts[i]

        best[file_counter] = [file, best_overall_weight, best_overall_cnt]
        
        
        worst_overall_weight, worst_overall_cnt = best_individuals_weights[0], best_individuals_cnts[0]
        
        for i in range(setting.number_of_runs):
            if best_individuals_cnts[i] > best_overall_cnt or (best_individuals_cnts[i] == best_overall_cnt and best_individuals_weights[i] > best_overall_weight):
                best_overall_weight, best_overall_cnt = best_individuals_weights[i], best_individuals_cnts[i]

        worst[file_counter] = [file, worst_overall_weight, worst_overall_cnt]
 
        
           
    output_file = open('../results/results_%s_%s_%s.txt' % (setting_names[setting_counter], dataset_name, datetime.now().strftime('%Y_%m_%d_%H_%M_%S')), "w")
    output_file.write("ParameterSetting:\n%s\n\nPresenting the results:\n\nBest Individuals:\n" % (str(setting)))
    for i in range(len(files)):
        output_file.write("\nProblem %s\n" % (files[i]))
        for j in range(setting.number_of_runs):
            output_file.write("Run #%s: Weight: %d, Components: %d\n" %((j+1), best_individuals[i][j][1], best_individuals[i][j][2]))
        output_file.write("")
    
    output_file.write("\nStatistics of the best individuals\n")
    table = [["File","Best (weight)", "Best (components)", "Worst (weight)", "Worst (components)", "Average (weights)","Average (components)","Stdev (weights)","Stdev(components)","Avg. Running Time(s)", "Correct solution"]]
    for (i, file) in enumerate(files):
        table.append([file, truncate(best[i][1], 3), truncate(best[i][2], 3), truncate(worst[i][1], 3), truncate(worst[i][2], 3), truncate(avg[i][1], 3), truncate(avg[i][2], 3), truncate(stdev[i][1], 3), truncate(stdev[i][2], 3), truncate(avg[i][3], 3), solutions[i]])
    output_file.write(tabulate(table))
    output_file.write("\n")


    
    
