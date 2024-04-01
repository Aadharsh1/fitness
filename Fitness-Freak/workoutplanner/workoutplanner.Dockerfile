# Use an official Python runtime as a parent image
FROM python:3.12

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements.txt file into the container at /app
COPY ./req.txt ./workoutplanner.py ./
# ./Fitness-Freak/user/req.txt ./
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r req.txt

# Copy the rest of the application code into the container
# COPY . .

# Run the application when the container launches
CMD ["python", "workoutplanner.py"]
