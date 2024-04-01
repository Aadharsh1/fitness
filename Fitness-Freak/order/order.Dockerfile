# Use an official Python runtime as a parent image
FROM python:3.12

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the requirements.txt file into the container at /app
COPY ./req.txt ./order.py ./ordersdb_serviceAccountKey.json ./
# ./Fitness-Freak/user/req.txt ./
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r req.txt

# Copy the rest of the application code into the container
# COPY . .

# ENV SERVICE_ACCOUNT_KEY_PATH ./user/serviceAccountKey.json
# Run the application when the container launches
CMD ["python", "order.py"]
