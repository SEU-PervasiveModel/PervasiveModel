function [ result, res_Delays, LSPs_h, clusterPos ] = get_CIR_maritime( channel_model_h, channel_model_l, tx_track, rx_track)
%%
% 海洋通信场景中用到的大尺度参数：K，角度
% 收发端都只支持单用户,只支持单个频率
% result: 1, 1, pos_length * noF 的cell，每个cell的size为 no_txAnt, no_rxAnt, no_clusters_h+no_clusters_l, no_raysEachCluster
% delay: 1, 1, pos_length * noF 的cell，每个cell的size为 no_txAnt, no_rxAnt, no_clusters_h+no_clusters_l, no_raysEachCluster
% 1, 1 代表收发端都是1个用户
% LSP: h层的，struct('DS',ds,'SF',sf,'K',kf,'ASA',asA,'ASD',asD,'XPR',xpr,'ESA',esA,'ESD',esD)
% ssp: struct('xT', xT, 'yT', yT, 'zT', zT， 'xR', xR, 'yR', yR, 'zR', zR)
%%
 
end
