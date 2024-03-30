# FROM python:3.12
# WORKDIR /usr/src/app
# COPY ./req.txt ./
# RUN python -m pip install --no-cache-dir -r req.txt
# COPY ./user.py ./
# CMD [ "python", "./user.py" ]
# docker build -t anshaziq/user:project -f Fitness-Freak/user/user.Dockerfile .
# docker run -p 5003:5003 -e dbURL=mysql+mysqlconnector://is213@host.docker.internal:3306/user daniilzam/user:project

# Use an official Python runtime as a parent image
FROM python:3.12

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements.txt file into the container at /app
COPY ./req.txt ./user.py ./serviceAccountKey.json ./
# ./Fitness-Freak/user/req.txt ./
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r req.txt

# Copy the rest of the application code into the container
# COPY . .

# Expose the port the app runs on
EXPOSE 5003

# ENV SERVICE_ACCOUNT_KEY_PATH ./user/serviceAccountKey.json
# Run the application when the container launches
CMD ["python", "user.py"]