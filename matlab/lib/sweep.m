%sr = scan rate
%vmax = maximum voltage
%vmin = minimum voltage
function sweep(f,sr,vmax,vmin)
freq = sr/((vmax - vmin)*2000);
vmax = -vmax;
vmin = -vmin;

    fprintf(f,'SOUR1:FUNC:SHAP USER0');
    fprintf(f,'SOUR1:FREQ %f',freq);
    fprintf(f,'SOUR1:VOLT:LEV:IMM:OFFS %f Vpp',((vmax + vmin)/2));
    fprintf(f,'SOUR1:VOLT:LEV:IMM:AMPL %f Vpp',(vmin - vmax));
end