-- Author: Wenbo Duan
-- Email: pv19120@bristol.ac.uk

################################################
1. Environment used:
- Python 3.8
- pandas   (install command: pip -install pandas)
- numpy    (install command: pip -install numpy)


################################################
2. How to run the program ?
2.1 Network problem:
	- Type number of stages and cost of each route in inputnetwork.txt
	- Open the whole folder in the IDE or open the terminal under the current folder path
	- Run network.py

 2.2 Capital budget problem:
	- Type total budget and subsidiaries' development plan in inputnetwork.txt
	- Open the whole folder in the IDE or open the terminal under the current folder path
	- Run capbud.py


################## important ###################
3. How to input question ?
3.1 Network problem:
	Example of input format (inputnetwork.txt) :
	---------------------------------------------
	Number of stages:
	"5"

	Cost:
	"1,2,2,3,3,2,5,4,2,6,3,2,4,3,3,2,1,5,4,3"
	----------------------------------------------
	Note:
	- All input contents should be placed within quotation marks
	- Inputting the cost of each route from LEFT to RIGHT, BOTTOM to TOP
	- The number of stages is couted start from 1

3.2 Capital budget problem:
	Example of input format (inputcapbud.txt) :
	---------------------------------------------
	Total Capital Budget:
	"14"

	Subsidiary's Development Plans:
	"(2,3), (4,6), (7,10)"
	"(1,2), (3,5)"
	"(3,5), (5,7), (8,13)"
	----------------------------------------------
	Note:
	- All input contents should be placed within quotation marks
	- The subsidiary development plan input format : 
		"(cost, reuturn), (cost, return), ..."
	- Inputting cost&return starts from plan 1 for each subsidiary
	- One subsidiary's plan per line


################################################
4. File Interpretation

- utils.py:
Supplementary codes for recording results into .txt files for both network and capital budget problems

- lognetwork.txt: 
This log file recorded the optimal decisions and associated values of each state, once per stage,
showing the process of  backward recursion

- lognetwork.txt: 
This log file recorded the optimal decisions and associated values of each state, once per stage,
showing the process of forward recursion

- solutionnetwork.txt: 
This file recorded completed the optimal decisions and associated values of each state and each stage.
This  file also recorded the analysis of the final result, including:
	` The total number of optimal routes.
	` The optimal cost 
	` The detailed description of each optimal path

- solutioncapbud.txt: 
This file recorded completed the optimal decisions and associated values of each state and each stage.
This  file also recorded the analysis of the final result, including:
	` The total number of optimal routes.
	` The optimal expected return
	` The detailed description of each optimal path

For more details please refer to the original files

################ Note ##########################
For some reason, contents that auto-generated in text files can not be correctly displayed in windows build-in notepad, 
the display of tables may be misaligned.
The feasible solutions could be opening txt in IDE, notepad++, or in the terminal


---Feel free to ask me for more info if anything happened during implementing---





