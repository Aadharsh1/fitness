# Use an official Python runtime as a parent image
FROM python:3.12

# Set the working directory in the container
WORKDIR /app
ADD . /app
# Copy the requirements.txt file into the container at /app
# COPY ./req.txt ./purchaseproduct.py ./
# COPY ./templates/success.html  ./templates/cancel.html /usr/src/app/template/
# ./Fitness-Freak/user/req.txt ./
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r req.txt

# Copy the rest of the application code into the container


# Run the application when the container launches
CMD ["python", "purchaseproduct.py"]
