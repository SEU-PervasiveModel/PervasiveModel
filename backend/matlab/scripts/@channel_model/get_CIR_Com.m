function [result, delay,LSP_f, clusterPos ] = get_CIR_Com(channel_model_forward, channel_model_back, ori_scp, condition, share, SoS)
% result: 1, 1, pos_length * noF 的cell，每个cell的size为 no_txAnt, no_rxAnt, no_clusters, no_raysEachCluster
% delay: 1, 1, pos_length * noF 的cell，每个cell的size为 no_txAnt, no_rxAnt, no_clusters, no_raysEachCluster
% 1, 1 代表收发端都是1个用户
% lsps_f: struct('DS',ds,'SF',sf,'K',kf,'ASA',asA,'ASD',asD,'XPR',xpr,'ESA',esA,'ESD',esD)
% ssps: struct('xT', xT, 'yT', yT, 'zT', zT， 'xR', xR, 'yR', yR, 'zR', zR) 

end