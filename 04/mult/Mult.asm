// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Mult.asm

// Multiplies R0 and R1 and stores the result in R2.
// (R0, R1, R2 refer to RAM[0], RAM[1], and RAM[2], respectively.)

     @R2
     M=0                       // RAM[2]= 0

     @R0
     D=M
     @n1
     M=D                       //n1 = RAM[0]

     @R1
     D=M
     @n2
     M=D                       //n2 = RAM[1]

     @counter
     M=1                       //counter = 1

     @sum
     M=0                       //sum = 0

(OPTION1)
     @n2
     D=M
     @n1
     D=M-D                  //n1 - n2
     @OPTION2
     D;JGT                     //if n1 > n2 goto OPTION2

     @n1            
     D=M
     @n                 
     M=D                       //n = n1
     @n2
     D=M
     @i
     M=D                       //i = n2
     @LOOP
     0;JMP                     // goto LOOP

(OPTION2)
     @n2
     D=M
     @n
     M=D                     //n = n2
     @n1
     D=M
     @i
     M=D                     //i = n1

(LOOP)
     @n
     D=M
     @counter
     D=M-D                 //counter - n
     @STOP
     D;JGT                    //if counter > n goto STOP

     @i
     D=M
     @sum
     M=M+D              //sum = sum + i
     @counter
     M=M+1              //counter = counter + 1
     @LOOP
     0;JMP

(STOP)
     @sum
     D=M
     @R2
     M=D                   //RAM[2] = sum
