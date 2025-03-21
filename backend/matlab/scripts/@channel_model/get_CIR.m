function [ result, delay, LSP, clusterPos ] = get_CIR( channel_model, ori_scp, condition, share, SoS)
%GET_CHANNEL_MODEL 此处显示有关此函数的摘要
% result: no_users_tx, no_users_rx, pos_length * noF 的cell，每个cell的size为 no_txAnt, no_rxAnt, no_clusters, no_raysEachCluster
% delay: no_users_tx, no_users_rx, pos_length * noF 的cell，每个cell的size为 no_txAnt, no_rxAnt, no_clusters, no_raysEachCluster
% LSP: struct('DS',ds,'SF',sf,'K',kf,'ASA',asA,'ASD',asD,'XPR',xpr,'ESA',esA,'ESD',esD)
% ssp: struct('xT', xT, 'yT', yT, 'zT', zT， 'xR', xR, 'yR', yR, 'zR', zR)

end