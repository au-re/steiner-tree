import numpy
import csv
import sys

'''
Maximal Fitness of an Individual: 1000
Population Size: 100
Crossover Probability: 0.900000
Mutation Probability: 0.050000
Tournament Size: 20.000000
Number of Generations: 100
Component Cost: 50
Mu: 50
Hall of Fame Size: 100
Verbose: False --> NOT USED HERE
Number of runs: 10
Crossover Function: <function twoPointsCrossover at 0x103826c08>
Mutation Function: <function multFlipBit at 0x103826d70>
'''

#Filename, Numerical name, Vertices, edges, solution
attr = {"data/B/b01": [101, 50, 63, 82], "data/B/b02": [102, 50, 63, 83], "data/B/b03": [103, 50,63,138],
"data/B/b04": [104,50,100,59], "data/B/b05": [105,50,100,61], "data/B/b06": [106,50,100,122],
"data/B/b07": [107,75,94,111], "data/B/b08": [108,75,94,104], "data/B/b09": [109,75,94,220],
"data/B/b10": [110,75,150,86], "data/B/b11": [111,75,150,88], "data/B/b12": [112,75,150,174],
"data/B/b13": [113,100,125,165], "data/B/b14": [114,100,125,235], "data/B/b15": [115,100,125,318],
"data/B/b16": [116,100,200,127], "data/B/b17": [117,100,200,131], "data/B/b18": [118,100,200,218],

"data/C/c01": [201,500,625,85], "data/C/c02": [201,500,625,144], "data/C/c03": [203,500,625,754],
"data/C/c04": [204,500,625,1079], "data/C/c05": [205,500,625,1579], "data/C/c06": [206,500,1000,55],
"data/C/c07": [207,500,1000,102], "data/C/c08": [208,500,1000,509], "data/C/c09": [209,500,1000,707],
"data/C/c10": [210,500,1000,1093], "data/C/c11": [211,500,2500,32], "data/C/c12": [212,500,2500,46],
"data/C/c13": [213,500,2500,258], "data/C/c14": [214,500,2500,323], "data/C/c15": [215,500,2500,556],
"data/C/c16": [216,500,12500,11], "data/C/c17": [217,500,12500,18], "data/C/c18": [218,500,12500,113], 
"data/C/c19": [219,500,12500,146], "data/C/c20": [220,500,12500,267]}


#filesD = ["data/D/d01","data/D/d02","data/D/d03","data/D/d04","data/D/d05","data/D/d06","data/D/d07","data/D/d08","data/D/d09",
#"data/D/d10","data/D/d11","data/D/d12","data/D/d13","data/D/d14","data/D/d15","data/D/d16","data/D/d17","data/D/d18", "data/D/d19","data/D/d20"
#}



def parse(files):
	with open('results.csv', 'wb') as csvfile:
		writer = csv.writer(csvfile, delimiter=';',quotechar='|', quoting=csv.QUOTE_MINIMAL)
		writer.writerow(["MaxFitness", "PopSize", "CrossProb", "MutProb", "TournSize", "NumberGen", "CompCost", "Mu", "HOFSize", "NumberRuns", "CrossFunction", "MutationFunction",
			"Problem", "ID", "Vertices", "Edges", "BestWeight", "BestComponents", "WorstWeight", "WorstComponent", "AvgWeights", "AvgComponents", "StdevWeights", "StdevComponents", "AvgTime", "OptSolution"])
		for file in files:
			#print("Parsing file: %s" %(file))
			setting = [0] * 12
			f = open(file, "r")
			for line in f:
				if line.startswith("Maximal Fitness of an Individual:"):
					setting[0] = int(line.split()[5])
				if line.startswith("Population Size:"):
					setting[1] = int(line.split()[2])
				if line.startswith("Crossover Probability:"):
					setting[2] = float(line.split()[2])
				if line.startswith("Mutation Probability:"):
					setting[3] = float(line.split()[2])
				if line.startswith("Tournament Size:"):
					setting[4] = float(line.split()[2])
				if line.startswith("Number of Generations:"):
					setting[5] = int(line.split()[3])
				if line.startswith("Component Cost:"):
					setting[6] = int(line.split()[2])
				if line.startswith("Mu:"):
					setting[7] = int(line.split()[1])
				if line.startswith("Hall of Fame Size:"):
					setting[8] = int(line.split()[4])
				if line.startswith("Number of runs:"):
					setting[9] = int(line.split()[3])
				if line.startswith("Crossover Function:"):
					setting[10] = line.split()[3]
				if line.startswith("Mutation Function:"):
					setting[11] = line.split()[3]

				if line.startswith("data"):
					line = line.split()
					problem = line[0]
					line_to_print = list(setting)
					line_to_print.append(problem)
					line_to_print.append(attr[problem][0])
					line_to_print.append(attr[problem][1])
					line_to_print.append(attr[problem][2])
					for i in range(1, 11):
						line_to_print.append(line[i])
					#print("line: ", line_to_print)
					writer.writerow(line_to_print)

			#print(setting)


'''
files = [
"Results/results_SettingC2_filesC_2016_01_21_13_56_57",
"Results/results_SettingB1_filesB_2016_01_20_20_14_30",
"Results/results_SettingC2_filesC_2016_01_21_13_55_01",
"Results/results_SettingC2_filesC_2016_01_21_13_42_03",
"Results/results_SettingC2_filesC_2016_01_21_13_40_59",
"Results/results_SettingC1_filesC_2016_01_21_01_36_14",
"Results/results_SettingC1_filesC_2016_01_21_01_34_32",
"Results/results_SettingC1_filesC_2016_01_21_01_34_19",
"Results/results_SettingC1_filesC_2016_01_21_01_32_43",
"Results/results_SettingB1_filesB_2016_01_20_21_09_16",
"Result/results_SettingC2_filesC_1_to_1_2016_01_21_22_56_39",
"Result/results_SettingC2_filesC_1_to_1_2016_01_21_22_57_23",
"Result/results_SettingC2_filesC_1_to_1_2016_01_21_22_57_46",
"Result/results_SettingC2_filesC_1_to_1_2016_01_21_22_57_57",
"Result/results_SettingB4_filesB_2016_01_21_19_12_21",
"Result/results_SettingB4_filesB_2016_01_21_19_11_44",
"Result/results_SettingB4_filesB_2016_01_21_17_24_56",
"Result/results_SettingB1_filesB_2016_01_20_20_13_38",
"Result/results_SettingB1_filesB_2016_01_20_21_08_11",
"Result/results_SettingB4_filesB_2016_01_21_17_25_00",
"Result/results_SettingB1_filesB_2016_01_20_18_37_19"]
'''

files = sys.argv[1::]
parse(files)





