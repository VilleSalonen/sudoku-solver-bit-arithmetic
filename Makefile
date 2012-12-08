sudoku: sudoku.c sudoku.h tests.c
	gcc -Wall -Werror -c sudoku.c
	gcc -Wall -Werror sudoku.o -o tests tests.c