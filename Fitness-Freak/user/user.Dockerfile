FROM python:3.12
WORKDIR /usr/src/app
COPY ./req.txt ./
RUN python -m pip install --no-cache-dir -r req.txt
COPY ./user.py ./
CMD [ "python", "./user.py" ]
# docker build -t daniilzam/user:project -f Fitness-Freak/user/user.Dockerfile .
# docker run -p 5003:5003 -e dbURL=mysql+mysqlconnector://is213@host.docker.internal:3306/user daniilzam/user:project