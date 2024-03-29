FROM python:3.12
WORKDIR /usr/src/app
COPY ./challenge/req.txt ./
RUN python -m pip install --no-cache-dir -r req.txt
COPY ./challenge/challenge.py .
CMD [ "python", "./challenge.py" ]
# docker build -t daniilzam/challenge:project -f challenge/challenge.Dockerfile .
# docker run -p 5000:5000 -e dbURL=mysql+mysqlconnector://is213@host.docker.internal:3306/challenge daniilzam/challenge:project