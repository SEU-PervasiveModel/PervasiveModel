function [encryptedData] = encryptData(data)

    key = [0.6948   0.3171    0.9502    0.0344    0.4387    0.3816    0.7655    0.7952    0.1869    0.4898    0.4456    0.6463    0.7094    0.7547    0.2760    0.6797];
   
    key = uint8(key); % 将密钥转换为字节数组

    % 创建AES加密对象
    cipher = javax.crypto.Cipher.getInstance('AES');
    secretKey = javax.crypto.spec.SecretKeySpec(key, 'AES');

    % 初始化加密
    cipher.init(javax.crypto.Cipher.ENCRYPT_MODE, secretKey);

    % 将字符串转换为UTF-8编码的字节数组
    utf8Bytes = unicode2native(data, 'UTF-8');

    % 加密数据
    encryptedBytes = cipher.doFinal(utf8Bytes);

    % 将加密后的字节数组转换为十六进制字符串
    encryptedData = dec2hex(encryptedBytes');
    encryptedData = reshape(encryptedData, 1, []);


end