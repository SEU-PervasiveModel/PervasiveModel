function h_track = get_satellite_track(h_satellite, move_time, samp_rate, ue_pos)
%SET_SATELLITE_INFO �˴���ʾ�йش˺�����ժҪ
%   �˴���ʾ��ϸ˵��
time_scale = 0:1/samp_rate:move_time;

%ue_pos=[118,31]; %�Ͼ��ľ�γ�� ��γ������γ�Ǹ�����γ���������������������Ǹ�
if ~exist('ue_pos','var') || isempty( ue_pos )
    ue_pos = [0,0];  %
end

[ xyzU, ~, orientation ] = h_satellite.ue_perspective ( ue_pos, time_scale);
h_track = track([]);
h_track.positions=(xyzU*1e3)';
h_track.move_dir=(orientation*pi/180)'; 
h_track.no_track_segment=1;
h_track.move_direc_azimuth = atan2(h_track.move_dir(2), h_track.move_dir(1)) .* ones(length(time_scale),1);
h_track.move_direc_elevation = atan2(h_track.move_dir(3), h_track.move_dir(1)) .* ones(length(time_scale),1);
h_track.time_scale=time_scale';
h_track.samp_rate=samp_rate;
h_track.move_time=move_time;
h_track.name='satellite';
speed = sqrt(sum((xyzU(:,2)*1e3-xyzU(:,1)*1e3).^2))/(1/samp_rate);  %m/s
h_track.move_speed=ones(length(h_track.move_direc_azimuth),1)*speed;  %����Ϊ�����˶�
h_track.track_length=speed*move_time;
end

