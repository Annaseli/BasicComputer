// Sorts an array starts at  the address in R14 with length as specified in R15.

    @R15
    D=M
    @len
    M=D                      //len = RAM[15]

    @i
    M=0                      //i = 0

(LOOP1)
    @i
    D=M 
    @len
    D=D-M
    D=D+1
    @END
    D; JGE                   //if i == len -1 goto END

    @R14
    D=M
    @n
    M=D                      //n = RAM[14] which is an address
    
    @m
    M=D+1                //m=n+1

    @swap
    M=0                      //swap = false

    @j
    M=0                      //j = 0

    (LOOP2)
        @i
        D=M 
        @len
        D=M-D
        D=D-1         
        @j
        D=M-D          
        @STOP
        D; JEQ               //if j == len - i - 1 goto STOP

        @n
        A=M
        D=M
        @m
        A=M
        D=D-M
        @SWAP
        D; JLT               //if RAM[n] < RAM[m] goto SWAP
        @INC
        0; JMP

        (SWAP)
            @n
            A=M
            D=M
            @temp
            M=D              //temp = RAM[n]
            
            @m
            A=M
            D=M
            @n
            A=M
            M=D              //RAM[n] = RAM[m]
            
            @temp
            D=M
            @m
            A=M
            M=D              //RAM[m] = temp
            
            @swap
            M=1              //swap = true

        (INC)
            @m
            D=M
            @n
            M=D              //n = m
            
            @m
            M=M+1            //m = m + 1
            
            @j
            M=M+1            //j = j + 1
            
            @LOOP2
            0; JMP
 
    (STOP)
        @swap
        D=M
        @END
        D; JEQ               //if swap == false goto END

        @i
        M=M+1                // i = i + 1
            
        @LOOP1
        0; JMP

(END)
