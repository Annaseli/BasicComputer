// This file is part of www.nand2tetris.org
// and the book "The Elements of Computing Systems"
// by Nisan and Schocken, MIT Press.
// File name: projects/04/Fill.asm

// Runs an infinite loop that listens to the keyboard input.
// When a key is pressed (any key), the program blackens the screen,
// i.e. writes "black" in every pixel;
// the screen should remain fully black as long as the key is pressed. 
// When no key is pressed, the program clears the screen, i.e. writes
// "white" in every pixel;
// the screen should remain fully clear as long as no key is pressed.

(LOOP1)
     @SCREEN
     D=A
     @addr
     M=D                      //addr = SCREEN
     @i
     M=1                      //i = 1

     @KBD
     D=M
     @LOOP2
     D; JGT                   //if  KBD > 0 goto LOOP2
     @LOOP3
     0; JMP                   //else if  KBD = 0 goto LOOP3

(LOOP2)
     @8192
     D=A
     @i
     D=M-D
     @LOOP1
     D; JGT                   //if  i > 8192 goto LOOP1

     @addr
     A=M
     M=-1                     //RAM[addr]=1111111111111111
     @addr
     M=M+1                //addr = addr + 1  
     @i
     M=M+1                //i = i + 1
     @LOOP2
     0;JMP                    //goto LOOP2

(LOOP3)
     @8192
     D=A
     @i
     D=M-D
     @LOOP1
     D; JGT                   //if  i > 8192 goto LOOP1

     @addr
     A=M
     M=0                      //RAM[addr]=0000000000000000
     @addr
     M=M+1      //addr = addr + 1  
     @i
     M=M+1      //i = i + 1
     @LOOP3
     0;JMP           //goto LOOP3

