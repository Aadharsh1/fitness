FROM python:3.12
WORKDIR /usr/src/app
COPY ./Fitness-Freak/fitnessassessment/req.txt ./
RUN python -m pip install --no-cache-dir -r req.txt
COPY ./Fitness-Freak/fitnessassessment/fitness.py .
CMD [ "python", "./fitness.py" ]
# docker build -t daniilzam/fitness:project -f Fitness-Freak/fitnessassessment/fitness.Dockerfile .
# docker run -p 5001:5001 -e dbURL=mysql+mysqlconnector://is213@host.docker.internal:3306/fitness daniilzam/fitness:project
# docker run -p 5001:5001 daniilzam/fitness:project