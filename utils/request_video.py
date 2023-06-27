import paramiko

# 文件名和路径
file_name = "people.mp4"
source_path = "."  # 当前工作目录

# 建立SFTP连接
ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("150.158.88.159", username="ubuntu", password="5921wjy!")

# 创建SFTP客户端
sftp = ssh.open_sftp()

# 传输文件
sftp.put(source_path + "/" + file_name, "/var/www/html/videos/" + file_name)

# 关闭SFTP连接和SSH会话
sftp.close()
ssh.close()

print(f"The file {file_name} has been saved to /var/www/html/videos/")