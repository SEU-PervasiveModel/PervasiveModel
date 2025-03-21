function [sat,sc] = view_satellite(app)
% YanP 星历方式得到卫星信息 24.12.28
if isempty(app.year.Value)||isempty(app.month.Value)||isempty(app.day.Value)||isempty(app.hour.Value)||isempty(app.minute.Value)||isempty(app.second.Value)
    warning('The current input parameters are insufficient, and the current time parameters will be used.');
    startTime= datetime;
    stopTime = datetime+seconds(app.runtime.Value);
else
    startTime= datetime(app.year.Value,app.month.Value,app.day.Value,app.hour.Value,app.minute.Value,app.second.Value);
    stopTime = datetime+seconds(app.runtime.Value);
end
sampleTime = 60;
sc = satelliteScenario(startTime,stopTime,sampleTime);
switch app.DropDown_satellitetype.Value
    case '设置参数 (Set parameters)'
        satname = 'Tx';
        semiMajorAxis = (app.satHeight.Value+6378)*1000;
        eccentricity = app.BinEditField.Value;
        inclination = app.CinEditField.Value;
        rightAscensionOfAscendingNode = app.DinEditField.Value;
        argumentOfPeriapsis = app.EinEditField.Value;
        trueAnomaly = app.FinEditField.Value;
        sat = satellite(sc,semiMajorAxis,eccentricity,inclination,rightAscensionOfAscendingNode,...
            argumentOfPeriapsis,trueAnomaly,"OrbitPropagator","two-body-keplerian","Name",satname);
    case '选择卫星 (Choose satellite)'
        name = app.DropDown_satellitename.Value;
        satname = '';
        for i = 1:length(name)
            if name(i) ~= ' '
                satname = strcat(satname,name(i));
            else
                satname = strcat(satname,'%20');
            end
        end
        url = 'https://celestrak.org/';
        url1 = strcat(url,'satcat/table-satcat.php?NAME=',satname,'&PAYLOAD=1&MAX=500');
        data = webread(url1);
        expr = 'href="/NORAD/elements/gp.php.*?\"';
        result = regexpi(data,expr,'match');
        index = cell2mat(result(2));
        pattern = '\d+';
        matches = regexp(index, pattern, 'match');
        numbers = cell2mat(matches);
        url2 = strcat(url,'NORAD/elements/gp.php?CATNR=',numbers);
        ephemeris = webread(url2);

        fp=fopen('ephemeris.txt','w');
        fprintf(fp,ephemeris);
        fclose(fp);

        sc = satelliteScenario(startTime,stopTime,sampleTime);
        sat = satellite(sc,"ephemeris.txt",'Name',name);
    case '导入星历 (Import ephemeris)'
        if isempty(app.Ephemeris.Value)
            error('Please import ephemeris file first.')
        else
            [filepath,filename,ext] = fileparts(app.Ephemeris.Value);
            addpath(filepath);
            sc = satelliteScenario(startTime,stopTime,sampleTime);
            sat = satellite(sc,strcat(filename,ext),'Name','Tx');
        end
end
end
