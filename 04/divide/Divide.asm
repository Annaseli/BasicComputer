//Divides 2 positive numbers which are stored at RAM[13] and RAM[14] into RAM[15]. RAM[13] is the numerator and RAM[14] is the //denominator.

    @R13
    D=M
    @n
    M=D                      //n = RAM[13]

    @R14
    D=M
    @m
    M=D                      //m = RAM[14]

    @res
    M=0                      //res = 0

    @power
    M=1                      //power = 1

(LOOP1)                    //find the largest k such that m * (2^k) <= n
    @m
    D=M<< 
    @LOOP2
    D; JLT                    //if m<< less then 0 ( <=> m<< larger then 32767 the largest positive) goto LOOP2

    @n
    D=D-M
    @LOOP2
    D; JGT                   //if last shifted m > n goto LOOP2

    @m
    M=M<<               //shift left m
    @power
    M=M<<               //shift left power
    @LOOP1
    0; JMP                   //goto LOOP1

(LOOP2)
    @power
    D=M
    @END
    D; JLE                   //if power <= 0 goto END

    @m
    D=M
    @n
    D=M-D  
    @SKIP
    D; JLT                   //if n - m < 0 goto SKIP

    @n
    M=D                   //n = n - m

    @power
    D=M    
    @res
    M=M+D             //res = res + power
   
    (SKIP)
        @m
        M=M>>        //shift right m
        @power
        M=M>>       //shift right power
        @LOOP2
        0; JMP

(END)
    @res
    D=M
    @R15
    M=D               //RAM[15] = res
