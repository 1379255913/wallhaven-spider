# 基础镜像
FROM python:3.9
# 创建一个应用目录
WORKDIR /home/wallhaven

COPY requirements.txt ./
# 使用清华源下载应用依赖
RUN pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple

COPY . .

CMD ["python3", "main.py"]