FROM mysql:latest
ENV MYSQL_ROOT_PASSWORD=root
# RUN echo "[mysqld]\ndefault-authentication-plugin=mysql_native_password" >> /etc/mysql/my.cnf
COPY ./create_workoutplans_table.sql /docker-entrypoint-initdb.d/