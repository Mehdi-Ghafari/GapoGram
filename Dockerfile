FROM oraclelinux:7-slim

ARG release=19
ARG update=3
# define the directory to work in
WORKDIR /code
# copy the requirements.txt file to the work directory
COPY requirements.txt .

RUN  yum -y install oracle-release-el7 && yum-config-manager --enable ol7_oracle_instantclient && \
     yum -y install oracle-instantclient${release}.${update}-basic oracle-instantclient${release}.${update}-devel oracle-instantclient${release}.${update}-sqlplus && \
     rm -rf /var/cache/yum && \
     yum -y install oracle-epel-release-el7 && \
     yum -y install python36 && \
     yum -y install vim sudo && \
     ln -fs /usr/bin/python3 /usr/bin/python && \
     python3 -m pip install --no-cache-dir -r requirements.txt

# Optional Oracle Network or Oracle client configuration files can be
# copied to the default configuration file directory.  These files
# include tnsnames.ora, sqlnet.ora, oraaccess.xml and cwallet.sso.
# For example:
# COPY wallet/* /usr/lib/oracle/${release}.${update}/client64/lib/network/admin

# Uncomment if the tools package is added
# ENV PATH=$PATH:/usr/lib/oracle/${release}.${update}/client64/bin

# Copy rest of the source code
COPY src/ src/
# EXPOSE the needed ports, for example 8080
EXPOSE 8080
# Running Command or Entry Point
CMD python src/app.py
CMD tail -f /dev/null
