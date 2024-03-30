FROM python:3.12
WORKDIR /usr/src/app
COPY ./req.txt ./
RUN python -m pip install --no-cache-dir -r req.txt
COPY ./product.py ./
CMD [ "python", "./product.py" ]
# docker build -t daniilzam/product:project -f Fitness-Freak/product/product.Dockerfile .
# docker run -p 5004:5004 -e dbURL=mysql+mysqlconnector://is213@host.docker.internal:3306/product daniilzam/product:project