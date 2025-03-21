function sat_track = get_track_satellite(app, move_time, samp_rate, initialPosTx)
switch app.DropDown_satellitetype.Value
    case '设置参数 (Set parameters)'
    Ain = 6378.137 + app.satHeight.Value;  %Semimajor axis in [km]; Default: 42164 km, GEO orbit
    Bin = app.BinEditField.Value;  %Orbital eccentricity [0-1]; Default: 0
    Cin = app.CinEditField.Value;  %Orbital inclination in [degree]; Default: 0 旋转平面的倾斜角度
    Din = app.DinEditField.Value;  %Longitude of the ascending node in [degree]; Default: 0 升交点的经度
    Ein = app.EinEditField.Value;  %Argument of periapsis in [degree]; Default: 0
    Fin = app.FinEditField.Value;  %True anomaly in [degree]; Default: 0 %初始角度
    app.h_satellite = satellite('custom',Ain, Bin, Cin, Din, Ein, Fin);

    if app.satHeight == 35786  % 地球静止卫星
        sat_track = track('static', move_time, 0, 0, initialPosTx, [0 0 0], samp_rate); % 发射端在天上, 速度为0
    else
        % 选接收端第一个坐标来确定卫星的位置
        [~, ue_pos] = tools.get_initialPos_table(app); % 南京的经纬度 经纬度用南纬是负，北纬是正，东经是正，西经是负
        sat_track = app.h_satellite.get_satellite_track(move_time, samp_rate, [ue_pos(1,1), ue_pos(1,2)]);
    end
 % YanP 星历计算 24.12.29
    case '选择卫星 (Choose satellite)'
        [sat,sc] = tools.view_satellite(app);
        gs = groundStation(sc,app.latitude.Value,app.longitude.Value,'Altitude',app.height.Value,'Name','Rx');
        time = 0:1/samp_rate:move_time;
        if isempty(app.year.Value)||isempty(app.month.Value)||isempty(app.day.Value)||isempty(app.hour.Value)||isempty(app.minute.Value)||isempty(app.second.Value)
            warning('The current input parameters are insufficient, and the current time parameters will be used.');
            startTime= datetime;
        else
            startTime= datetime(app.year.Value,app.month.Value,app.day.Value,app.hour.Value,app.minute.Value,app.second.Value);
        end
        for i = 1:length(time)
            TIME(i) = startTime+seconds(time(i));
            [az(i),elev(i),range(i)] = aer(gs,sat,TIME(i));
            [xEast(i),yNorth(i),zUp(i)] = aer2enu(az(i),elev(i),range(i));
            if i ~= 1
                track_length(i-1) = norm([xEast(i)-xEast(i-1),yNorth(i)-yNorth(i-1),zUp(i)-zUp(i-1)]);
            end
        end
        lat0 = app.latitude.Value;
        lon0 = app.longitude.Value;
        h0 = app.height.Value;
        wgs84 = wgs84Ellipsoid('kilometer');
        for i = 1:length(time)
            TIME(i) = startTime+seconds(time(i));
            [~,velocity(:,i)] = states(sat,TIME(i),"CoordinateFrame","ecef");
            [vxEast(i),vyNorth(i),vzUp(i)] = ecef2enu(velocity(1,i),velocity(2,i),velocity(3,i),lat0,lon0,h0,wgs84);
            speed(i) = norm([vxEast(i),vyNorth(i),vzUp(i)]);
            move_dir(:,i) = [vxEast(i);vyNorth(i);vzUp(i)]/speed(i);
            move_azimuth(i) = atan2(move_dir(2,i),move_dir(1,i));
            move_elevation(i) = atan2(move_dir(3,i),sqrt(move_dir(1,i)^2+move_dir(2,i)^2));
        end
        sat_track = track([]);
        sat_track.positions = [xEast',yNorth',zUp'];
        sat_track.move_dir = move_dir;
        sat_track.no_track_segment = 1;
        sat_track.move_direc_azimuth = move_azimuth;
        sat_track.move_direc_elevation = move_elevation;
        sat_track.time_scale = time;
        sat_track.samp_rate = samp_rate;
        sat_track.move_time = move_time;
        sat_track.name='satellite';
        sat_track.move_speed = speed;
        sat_track.track_length = sum(track_length);
    case '导入星历 (Import ephemeris)'
        [sat,sc] = tools.view_satellite(app);
        gs = groundStation(sc,app.latitude.Value,app.longitude.Value,'Altitude',app.height.Value,'Name','Rx');
        time = 0:1/samp_rate:move_time;
        if isempty(app.year.Value)||isempty(app.month.Value)||isempty(app.day.Value)||isempty(app.hour.Value)||isempty(app.minute.Value)||isempty(app.second.Value)
            warning('The current input parameters are insufficient, and the current time parameters will be used.');
            startTime= datetime;
        else
            startTime= datetime(app.year.Value,app.month.Value,app.day.Value,app.hour.Value,app.minute.Value,app.second.Value);
        end
        for i = 1:length(time)
            TIME(i) = startTime+seconds(time(i));
            [az(i),elev(i),range(i)] = aer(gs,sat,TIME(i));
            [xEast(i),yNorth(i),zUp(i)] = aer2enu(az(i),elev(i),range(i));
            if i ~= 1
                track_length(i-1) = norm([xEast(i)-xEast(i-1),yNorth(i)-yNorth(i-1),zUp(i)-zUp(i-1)]);
            end
        end
        lat0 = app.latitude.Value;
        lon0 = app.longitude.Value;
        h0 = app.height.Value;
        wgs84 = wgs84Ellipsoid('kilometer');
        for i = 1:length(time)
            TIME(i) = startTime+seconds(time(i));
            [~,velocity(:,i)] = states(sat,TIME(i),"CoordinateFrame","ecef");
            [vxEast(i),vyNorth(i),vzUp(i)] = ecef2enu(velocity(1,i),velocity(2,i),velocity(3,i),lat0,lon0,h0,wgs84);
            speed(i) = norm([vxEast(i),vyNorth(i),vzUp(i)]);
            move_dir(:,i) = [vxEast(i);vyNorth(i);vzUp(i)]/speed(i);
            move_azimuth(i) = atan2(move_dir(2,i),move_dir(1,i));
            move_elevation(i) = atan2(move_dir(3,i),sqrt(move_dir(1,i)^2+move_dir(2,i)^2));
        end
        sat_track = track([]);
        sat_track.positions = [xEast',yNorth',zUp'];
        sat_track.move_dir = move_dir;
        sat_track.no_track_segment = 1;
        sat_track.move_direc_azimuth = move_azimuth;
        sat_track.move_direc_elevation = move_elevation;
        sat_track.time_scale = time;
        sat_track.samp_rate = samp_rate;
        sat_track.move_time = move_time;
        sat_track.name='satellite';
        sat_track.move_speed = speed;
        sat_track.track_length = sum(track_length);
end
        % 更新表格上的信息
        txInitialPos = ['[',num2str(sat_track.positions(1,1,:)),' ',num2str(sat_track.positions(1,2,:)),' ',num2str(sat_track.positions(1,3,:)),']'];
        txSpeed = num2str(sat_track.move_speed(1));
        txAcceleration = num2str(sat_track.move_accel);
        txTrackOri = '[1 0 0]';
        % 创建新行数据
        team = table2array(app.UITable_tx.Data);
        team{1,3} = txInitialPos;
        team{1,6} = txSpeed;
        team{1,7} = txAcceleration;
        team{1,8} = txTrackOri;
        app.UITable_tx.Data = cell2table(team);
        z = sat_track.positions(:,3)';
        invisible = find(z<0);
        if ~isempty(invisible)
            error('The satellite is invisible to the receiver, please reset.');
        end
end