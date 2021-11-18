function [] = cv(handles)
%CV Summary of this function goes here
%   Detailed explanation goes here
    disp("do cyclic voltammetry");
    instrreset;
    delete(instrfindall);
    figure(1);
    V_MAX = str2double(handles.v_max.String);
    V_MIN = str2double(handles.v_min.String);
    I_MAX = str2double(handles.i_max.String);
    I_MIN = str2double(handles.i_min.String);
    P_HIGH = str2double(handles.p_high.String);
    P_LOW = str2double(handles.p_low.String); 
    SCAN_RATE = str2double(handles.scan_rate.String);
    N_SCANS = str2double(handles.n_scans.String);
    FILENAME = handles.filename.String;  
    LIMIT = (P_HIGH-P_LOW)*2000*N_SCANS/SCAN_RATE;
    FILENAME = strcat("./log/"+FILENAME+".csv");  
    s = serial('com3');
    s.InputBufferSize = 16;
    s.BaudRate = 9600;
    s.BytesAvailableFcnMode = 'terminator';
    time = 0;

    k = daq.createSession('ni');
    addAnalogInputChannel(k,'cDAQ1Mod1', 0, 'Voltage');
    addAnalogInputChannel(k,'cDAQ1Mod1', 1, 'Voltage');
    k.Rate = 20000;

    fg = visa('ni','USB0::0x0699::0x0353::1738559::INSTR');
    fopen(fg);
    volt = 0;
    curr = 0;
    plotGrid = 'on';
    iMax = I_MAX;
    iMin = I_MIN;

    vMax = V_MAX;
    vMin = V_MIN;


    %-----------------------%
    %Subplot of Voltage-Time

    subplot(2,2,1)
    plotGraph1 = plot(time,volt,'-r');
    hold on;
    title('Voltage-Time');
    xlabel('Time (in sec)');
    ylabel('Voltage (in Volts)');
    axis([0 LIMIT vMin vMax]); %axis ranges for V-T
    grid(plotGrid);
    grid minor;

    subplot(2,2,2)
    %Subplot of Current-Time
    plotGraph2 = plot(time,curr,'-b');
    hold on;
    title('Current-Time');
    xlabel('Time (in sec)');
    ylabel('Current (in µA)');
    axis([0 LIMIT iMin iMax]); %axis ranges for C-T
    grid(plotGrid);
    grid minor;

    subplot(2,2,3)
    %Subplot of Current-Voltage
    plotGraph3 = plot(volt,curr,'-k');
    hold on;
    title('Current-Voltage (Unfiltered)');
    xlabel('Voltage (in Volts)');
    ylabel('Current (in µA)');
    axis([vMin vMax iMin iMax]); %axis ranges for C-V
    grid(plotGrid);
    grid minor;

    subplot(2,2,4)
    %Subplot of Current-Voltage
    plotGraph4 = plot(volt,curr,'-k');
    hold on;
    title('Current-Voltage (Filtered)');
    xlabel('Voltage (in Volts)');
    ylabel('Current (in µA)');
    axis([vMin vMax iMin iMax]); %axis ranges for C-V
    grid(plotGrid);
    grid minor;


    %-----------------------%


    plotGraph1.UserData = 0;
    s.BytesAvailableFcn = {@mycallback,plotGraph1,plotGraph2,plotGraph3,plotGraph4,fg,k,LIMIT,FILENAME};    
    
    %% START SWEEP AND FETCH DATA
    fopen(s);
    tic
    sweep(fg,SCAN_RATE,P_HIGH,P_LOW);%SWEEP SIGNAL
    fprintf(fg,'OUTput1:STATe ON');
    function mycallback(obj,~,plotGraph1,plotGraph2,plotGraph3,plotGraph4,fg,k,limit,filename)
                    count = get(plotGraph1,'UserData');
                    i1 = get(plotGraph2,'UserData');   
                    time = get(plotGraph1,'XData');
                    volt = get(plotGraph1,'YData');
                    curr = get(plotGraph2,'YData');
                    v = get(plotGraph4,'XData');
                    i = get(plotGraph4,'YData');
                    t = get(plotGraph4,'ZData');


                    count = count + 1;
                    data = k.inputSingleScan;
                    volt(count) = data(1)*(-1);
                    curr(count) = data(2)*(-1)*100+20;
                    time(count)= toc;
    %                 disp(time(count));
                    %% PLOT 1st CV SWEEPS Au0
                    if time(count) > 5 && time(count)<limit-1
                        v(count) = volt(count);
                        i(count) = curr(count);
                        i1(count) = curr(count);

                        t(count)= time(count);
                        i = sgolayfilt(i,3,5);                                     
                    end

           %% PLOT IN REAL TIME
           set(plotGraph1,'XData',time,'YData',volt);
           set(plotGraph2,'XData',time,'YData',curr);
           set(plotGraph3,'XData',volt,'YData',curr);
           set(plotGraph4,'XData',v,'YData',i,'ZData',t);
           set(plotGraph1,'UserData',count);
           set(plotGraph2,'UserData',i1);
           pause(0.0001); % pause for plot
     flushinput(obj);

         if time(count)>limit && time(count)<limit + 0.4
             cvdata = [(plotGraph4.ZData)',(plotGraph4.XData)',(plotGraph2.UserData)',(plotGraph4.YData)'];
%              FileName=[datestr(now, 'yyyymmdd'),' 50mVs-1 PANI IDT02 _test_we1','.csv'];
             csvwrite(filename,cvdata);
             flushinput(obj);
             hold off;
             fclose(obj);
             disp('Plot over! Object has been deleted');
             fprintf(fg,'OUTput1:STATe OFF');
             delete(obj);
         end
    end
    return
end

