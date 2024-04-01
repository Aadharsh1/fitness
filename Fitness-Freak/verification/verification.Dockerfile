FROM python:3.12
WORKDIR /usr/src/app
COPY ./req.txt ./verification.py ./
RUN python -m pip install --no-cache-dir -r req.txt
EXPOSE 5006
CMD [ "python", "./verification.py" ]
# docker build -t daniilzam/user:project -f Fitness-Freak/user/user.Dockerfile .
# docker run -p 5006:5006 -e dbURL=mysql+mysqlconnector://is213@host.docker.internal:3306/user daniilzam/user:project