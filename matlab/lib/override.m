function [] = override()
%OVERRIDE Summary of this function goes here
    delete(instrfindall);
    fg = visa('ni','USB0::0x0699::0x0353::1738559::INSTR');
    fopen(fg);
    fprintf(fg,'OUTput1:STATe OFF');
    fclose(fg);
end

