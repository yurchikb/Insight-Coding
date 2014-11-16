Insight-Coding
==============
Project for Insight Coding Challenge: Developing a Sudoku puzzle solver

The program reads a Sudoku puzzle from an input file formatted like the following

0,3,5,2,9,0,8,6,4
0,8,2,4,1,0,7,0,3
7,6,4,3,8,0,0,9,0
2,1,8,7,3,9,0,4,0
0,0,0,8,0,4,2,3,0
0,4,3,0,5,2,9,7,0
4,0,6,5,7,1,0,0,9
3,5,9,0,2,8,4,1,7
8,0,0,9,0,0,5,2,6

It solves the puzzle and writes results iinto the output text file formatted like the following

1,3,5,2,9,7,8,6,4
9,8,2,4,1,6,7,5,3
7,6,4,3,8,5,1,9,2
2,1,8,7,3,9,6,4,5
5,9,7,8,6,4,2,3,1
6,4,3,1,5,2,9,7,8
4,2,6,5,7,1,3,8,9
3,5,9,6,2,8,4,1,7
8,7,1,9,4,3,5,2,6

This depository contains Python script (sudoku8.py file), Readme.txt file, 
and several files Sudoku puzzles (datein?.txt files) with the corresponding solutions (dateout?.txt files)

Script Processing Summary

I used Canopy 1.4.1 with Python 2.7 for the coding. I ran the script on HP Envy laptop (eight 
processors with 2.4 GHz with 8 GB of memory). The script is suplemented with many comments and is, hopefully, 
comprehensible. The processing is performed in several steps: 

Step 1. Input and output file names are entered by the user.
Step 2. Several simple tests are performed to check if an input file is properly vonfigured (e.g., contais numbers between 1 & 9,
does not have any duplicates numbers in rows).
Step 3. Simple stage 1 processing is performes by identifying all possible values for each empty board cell and 
by populating all empty fields with a single possible value identified. Stage 1 processing may be repeated until no more empty fields 
with a single possible value are left. Stage 1 processing may be sufficient in solving solve simple puzzles (like the one similar 
presented earlier in the text).
Step 4. If empty board cells are left after Stage 1 processing is completed, then the Stage 2 processing tries every possible combination of values 
until it either finds a solution or fails to find one.

Testing Results

I tested the script with 7 different puzzles of various complexity from 3 different web sites and found solutions
in less than a minute (often in seconds) in all cases except one.

The puzzle in file datin.txt was done instantaneously. Only stage1 processing was required. Solution is 
in file datout.txt. The puzzle in file datina.txt, datinb.txt, datinc.txt, datine.txt, datinf.txt were solved
in less than a minute (often in several seconds). The puzzle in file datind.txt did not have a solution (according 
to my script). It took the script couple of seconds to detect  that there is no solution. The puzzle in the dating.txt,
claimed to be world's hardest Sudoku at 
http://www.telegraph.co.uk/science/science-news/9359579/Worlds-hardest-sudoku-can-you-crack-it.html, was indeed complex
and required more than 4 minutes to get solved.

Below I attached python shell session recorded while solving the complex puzzle in dating.txt.


***********
Welcome to Canopy's interactive data-analysis environment!
 with pylab-backend set to: inline
Type '?' for more information.

In [1]: %run C:/Users/Yury/Desktop/Insight-Coding/sudoku8.py

Enter the input file with the Sudoku puzzle: dating.txt
Input file is dating.txt

Enter the output file for the solution: datoutg.txt
Output file is datoutg.txt

Initial Board

[[8 0 0 0 0 0 0 0 0]
 [0 0 3 6 0 0 0 0 0]
 [0 7 0 0 9 0 2 0 0]
 [0 5 0 0 0 7 0 0 0]
 [0 0 0 0 4 5 7 0 0]
 [0 0 0 1 0 0 0 3 0]
 [0 0 1 0 0 0 0 6 8]
 [0 0 8 5 0 0 0 1 0]
 [0 9 0 0 0 0 4 0 0]]

Board after simple STAGE1 processing

[[8 0 0 0 0 0 0 0 0]
 [0 0 3 6 0 0 0 0 0]
 [0 7 0 0 9 0 2 0 0]
 [0 5 0 0 0 7 0 0 0]
 [0 0 0 0 4 5 7 0 0]
 [0 0 0 1 0 0 0 3 0]
 [0 0 1 0 0 0 0 6 8]
 [0 0 8 5 0 0 0 1 0]
 [0 9 0 0 0 0 4 0 0]]

Starting Main Loop.....

20000  iterations completed........
40000  iterations completed........
60000  iterations completed........
80000  iterations completed........
100000  iterations completed........
120000  iterations completed........
140000  iterations completed........
160000  iterations completed........
180000  iterations completed........
200000  iterations completed........
220000  iterations completed........
240000  iterations completed........

Final Board

[[8 1 2 7 5 3 6 4 9]
 [9 4 3 6 8 2 1 7 5]
 [6 7 5 4 9 1 2 8 3]
 [1 5 4 2 3 7 8 9 6]
 [3 6 9 8 4 5 7 2 1]
 [2 8 7 1 6 9 5 3 4]
 [5 2 1 9 7 4 3 6 8]
 [4 3 8 5 2 6 9 1 7]
 [7 9 6 3 1 8 4 5 2]]


Execution time 249.625 secs

In [2]: 
