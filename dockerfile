# Use uma imagem base do Ubuntu
FROM ubuntu:20.04

# Defina variáveis de ambiente necessárias para a instalação do Oracle
ENV ORACLE_BASE=/opt/oracle \
    ORACLE_HOME=/opt/oracle/product/19c/dbhome_1 \
    ORACLE_SID=ORCLCDB \
    ORACLE_PDB=ORCLPDB1 \
    ORACLE_CHARACTERSET=AL32UTF8 \
    CLIENT_HOME=/opt/oracle/product/19c/client_1

# Atualize o sistema e instale os pacotes necessários
RUN apt-get update && apt-get install -y libaio1 wget unzip

# Crie os diretórios necessários
RUN mkdir -p $ORACLE_BASE/scripts/setup && \
    mkdir $ORACLE_BASE/scripts/startup && \
    ln -s $ORACLE_BASE/scripts /docker-entrypoint-initdb.d && \
    mkdir -p $ORACLE_HOME && \
    mkdir -p $CLIENT_HOME && \
    chown -R oracle:dba $ORACLE_BASE && \
    chmod -R 775 $ORACLE_BASE

# Copie os arquivos de instalação para o contêiner
COPY ./database /opt/oracle/
COPY ./client /opt/oracle/

# Execute o script de instalação
RUN /opt/oracle/runInstaller
RUN /opt/oracle/client/runInstaller

# Exponha a porta padrão do Oracle
EXPOSE 1521

# Defina o diretório de trabalho
WORKDIR /home/oracle

# Execute o script de inicialização do Oracle ao iniciar o contêiner
CMD exec $ORACLE_BASE/scripts/startup/startup.sh
