import numpy as NP
import os
import sys
from sys import exit
import time

###Ask the customer for an input and output file names
infile=raw_input('Enter the input file with the Sudoku puzzle: ')
if not os.path.isfile(infile): #check if input file exists
    print('\n\t****File ' + infile + ' does not exist, Program is teminated.')
    exit(0) #incorrect input file. exit.
print('Input file is ' + infile)
outfile=raw_input('Enter the output file for the solution: ')
if len(outfile) == 0:
    print('\n\t****No name entered for result file. Program is terminated.')
    exit(0) #no name for output file. exit.
print('Output file is ' + outfile)

###starting the execution time clock
start_time = time.time()

###read data in the numpy matrix 9 by 9
dim=9
board = NP.zeros(shape=(dim,dim)) #define board

row=0
with open(infile,'r') as f:   #read data into matrix row by row
    for line in f:
        board[row]=line.strip().split(',')
        row+=1
f.close

###Some Simple Data Verification
#Numbers should be between 0 and 9. No dublicates. More checks can be added.

errflag=False

for i in range(dim): #check numbers for proper range 0:9
    for j in range(dim):
        if board[i,j] not in range (10):
            print('\n\tWrong Input - Value item not in range 0:9')
            errflag=True
for line in range(dim): #check for duplicates in rows
    for i in range(1,10):
        if board.tolist()[line].count(i)>1:
            print('\n\tMultiple '+str(i)+'s in line '+str(line))
            errflag=True
            
if errflag: # need to fix data, exit.
    print('\n\tPLEASE FIX INPUT FILE AND TRY AGAIN\n')
    print(board)
    exit(0)
                  

###converting data to ing & and get them into NP matrix form    
board=[[int(board[j,i]) for i in range(dim)] for j in range(dim)]
board=NP.matrix(board)

init_board=board.copy() #store the initial board for later printing

###Let's define general structures and functions for initial simple steps

#this function creates the list of missing values in row, column or box zone
def missed_vals(zone):
    #what is missing in this zone?
    missed=[]
    for i in range(dim):
        if i+1 not in zone:
            missed.append(i+1)
    return(missed)
    
#create list of lists of values missing in rows
missed_rows=[missed_vals(board[i]) for i in range(dim)]

#create list of lists of values missing in columns
missed_cols=[missed_vals(board[:,j]) for j in range(dim)]

#create list of lists of values missing in boxes (need to make more generic)
missed_boxes = [missed_vals(board[3*i:3*i+3,3*j:3*j+3]) \
    for i in range(3) for j in range(3)]

#create mapping function from matrix cell to box numbered from 0 to 8
ij_to_box={}
[[ij_to_box.update({(i,j):(3*(i/3)+(j/3))}) for j in range(9)] \
    for i in range(9)]    

#Use previously found missed values in rows, columns and boxes to build
#possible values for each empty cell. Uses logical AND on sets
possible_cell_values=[]
for i in range(dim):
    for j in range(dim):
        if board[i,j]==0:
            possible_cell_values.append([i,j, set(missed_rows[i]) & \
            set(missed_cols[j]) & set(missed_boxes[ij_to_box[(i,j)]])])

#function to write results to the output file. Used several times. 
def write_board_to_file(file_name):
    tempstr=''
    for i in range(dim): #combine all cell values in single str for writing
        for j in range(dim):
            tempstr+=str(board[i,j])+','
        tempstr=tempstr[:-1]+'\n' #replace commas with new lines between rows
    tempstr=tempstr[:-1]   #remove last new line
    with open(file_name,'w') as ff:
        ff.write(tempstr)
    ff.close

##############################################################################
# STAGE1: check for cells that have no possible values left (no solution)
# or with single posible value left. We will populate this value into the cell
# and remove the cell from empty cell lists
#############################################################################

# Every time the empty cell is populated with val, this function will remove
# this val from the list of possible values for all empty cells in the same row
# or column or box 
def remove_dependencies(row, col,val):
    #remove value from the list of possible values for dependent cells
    for entry in possible_cell_values:
        i,j=(entry[0],entry[1])
        if (i==row or j==col or ij_to_box[(i,j)]==ij_to_box[(row,col)]) \
        and val in entry[2]:
            entry[2] -= {val} #remove this value
                       
# simple logic (to get simple puzzles solved) populates empty cells with 
# single possible value left, update possible value lists for dependent empty
# cells via remove_dependencies() function

more_work_to_do=1 #flag to indicate that more empty cells are left
while len(possible_cell_values)>0 and more_work_to_do==1:
    more_work_to_do=0
    for entry in possible_cell_values:
        if len(entry[2])==0:  #no values left for empty cell. no solution exist
            print('\n'+'Initial Board'+'\n')
            print(init_board)
            print('\n\tTHERE IS NO SOLUTION TO THIS PUZZLE. DONE\n')
            break;
        elif len(entry[2])==1: #cells with single value left are populated here
            more_work_to_do=1
            i,j=(entry[0],entry[1])
            board[i,j]=list(entry[2])[0]
            xx=possible_cell_values.index(entry)
            del possible_cell_values[xx]
            remove_dependencies(i,j,board[i,j]) #fix vals for dependent cells

#Simple processing (STAGE1) is completed. Results are displayed 
print('\n'+'Initial Board'+'\n')
print(init_board)
print('\n'+'Board after simple STAGE1 processing'+'\n')
print(board)

######################################################################
# STAGE2: Long and hard trying of all possible assignment combinations
######################################################################

#defining and populating structures for the stage2 processing
#list of the empty cells at the beginning of stage2 and list of untried values
#for each empty cell
empty_cell_list=[]
remained_value_dict={}
#xx_cell_values={}
for entry in possible_cell_values:
    i,j=(entry[0],entry[1])
    empty_cell_list.append((i,j))
    remained_value_dict.update({(i,j):[]})
    
# his is the heavy-lifting function that updates possible values for
# remaining empty cells every time empty cell is populated or reset/cleared.
# It may be significantly optimazed, if needed. At the moment it just 
# recalculates possible values values for each empty cell by using logical AND
# on sets for relevant row, column and box.
def rebuild_state():
    missed_rows=[missed_vals(board[i]) for i in range(dim)]
    #print(missed_rows)
    missed_cols=[missed_vals(board[:,j]) for j in range(dim)]
    #print (missed_cols)
    missed_boxes = [missed_vals(board[3*i:3*i+3,3*j:3*j+3]) \
    for i in range(3) for j in range(3)]
    #print(missed_boxes)
        
    temp_dict={}
    for i in range(dim):
        for j in range(dim):
            if board[i,j]==0:
                temp_dict.update({(i,j):(set(missed_rows[i]) & \
                set(missed_cols[j]) & set(missed_boxes[ij_to_box[(i,j)]]))})
                if len(temp_dict[(i,j)])==0:
                    return ('deadend',{})
    return ('ok',temp_dict)
   

#Lets check if empty cells left after STAGE1 processing. If not, we are done!
ret,xx_cell_values=rebuild_state() 
if len(xx_cell_values)==0: 
    print('\n'+'Final Board'+'\n')
    print(board)
    print('\n\nMISSION ACCOMPLISHED!!')
    write_board_to_file(outfile) #write final board to file
    exit(0)   # we are done

# if some cells are still empty start trying different value combinations
cur_entry_num=0
cur_cell=empty_cell_list[cur_entry_num]
remained_value_dict[cur_cell]=list(xx_cell_values[cur_cell])

print('\nStarting Main Loop.....\n')
sys.stdout.flush() #get previous message printed immediately
iterations=0

#### MAIN STAGE2 decision loop. Is it time to fill up next empty cell or 
###  at deadend and forced to try different value for the current empty cell, 
#### or exausted all possible values for the current cell and need to step back 
#### by eptying current cell ang trying next possible value for the previously 
#### populated empty cell

while cur_entry_num < len(empty_cell_list): #do it until no empty cells left
    iterations+=1
    if iterations%20000==0:   #still working message every 20000 iterations 
        print (str(iterations)+ '  iterations completed........')
    i,j=cur_cell
    if len(remained_value_dict[cur_cell]) > 0: #have values to try for cur cell
        cur_value=remained_value_dict[cur_cell][0] #get next value
        remained_value_dict[cur_cell].pop(0)   #remove it from the list of vals
        board[i,j]=cur_value     #assign this value to the cell
        if (i,j)==empty_cell_list[-1]: #if the last cell is filled - DONE!
            break #go to print result
        ret,xx_cell_values=rebuild_state() #check state with new cell value
        if ret == 'ok': # keep current value go to next empty cell-nice
            cur_entry_num+=1
            cur_cell=empty_cell_list[cur_entry_num]
            remained_value_dict[cur_cell]=list(xx_cell_values[cur_cell])
        elif len(remained_value_dict[cur_cell]) == 0: #deadend-back up a cell
            board[i,j]=0 #remove vaue from current cell - it is empty again
            remained_value_dict[cur_cell]=[] # reset list of possible vals
            cur_entry_num-=1 #go to previously filled empty cell
            cur_cell=empty_cell_list[cur_entry_num]
        else: #deadend but can go to next possible value for the same cell
            board[i,j]=0 #empty current cell; will fill later with next value
    else: #no values left for the current cell to try - backup one more cell
        board[i,j]=0 #empty cell
        remained_value_dict[cur_cell]=[] #reset list of possible vals
        if cur_entry_num==0: #no cells left to try - could not find solution
            print('\n\n\tCOULD NOT FIND A SOLUTION - SORRY\n')
            exit(0)
        cur_entry_num-=1 #go try a previously filled cell to try
        cur_cell=empty_cell_list[cur_entry_num] 

#DONE - print and write solution 
write_board_to_file(outfile) #write final board to file        
print('\n'+'Final Board'+'\n')
print(board)
#get an elapsed time measurement
print('\n\nExecution time ' +str(time.time() - start_time) + ' secs')
