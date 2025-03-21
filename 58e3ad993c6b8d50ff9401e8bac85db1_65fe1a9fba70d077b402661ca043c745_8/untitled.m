% carrier_frequency = 5.3e9; % 设置载波频率
% % 天线
% EfieldThetaTx = ones(181,360);
% EfieldPhiTx = ones(181,360); 
% rx_array = antenna_array('linear', 128, carrier_frequency, 0.6, EfieldThetaTx, EfieldPhiTx, 45,0,15);
% tx_array = antenna_array('linear', 8, carrier_frequency, 0.88, EfieldThetaTx, EfieldPhiTx, 45,0,18);
sps = simulation_parameters; % 仿真参数控制类
sps.carrier_frequency = 5.3e9; % 设置载波频率
sps.setScenario('sub-6 GHz_UMa_NLoS'); 
% 设置场景为UMi场景，使用的是大规模MIMO技术，对应着XX.conf文件
cm = channel_model(sps); % 使用上面的设置生成对应的信道
% 天线
EfieldThetaTx = ones(181,360);
EfieldPhiTx = ones(181,360); 
cm.rx_array = antenna_array('linear', 128, sps.carrier_frequency, 0.6, EfieldThetaTx, EfieldPhiTx, 45,0,15);
cm.tx_array = antenna_array('linear', 8, sps.carrier_frequency, 0.88, EfieldThetaTx, EfieldPhiTx, 45,0,18);
cm.clusters.num_clusters = 20;
cm.clusters.num_rays_each_cluster = 5;
% 运动轨迹
len_time = 0.01;
sample = 100;
cm.rx_track = track('static', 3, 0, 0, [0 0 20], [1 1 0], sample);
cm.tx_track = track('linear', 3, 2, 0, [5 -37 1.5], [2 1 0], sample);
[ result, result_delay, lsps, ssps ] = cm.get_CIR(cm.sim_params.scen_para);