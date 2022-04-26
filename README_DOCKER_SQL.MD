###################################################################################################################
INSTALACIÓ DOCKER MYSQL

1- Descarregar imatge mysql per a docker

sudo docker pull mysql/mysql-server:latest

2-Verificar que l'imatge està llistada a la llista del docker

sudo docker images

3-Desplegar imagte mysql en un contenidor docker 

sudo docker run --name=SQLDocker -d mysql/mysql-server:latest

#SQLDocker es el nom del contenidor i mysql/mysql-server:latest la imatge que desplegarem

4-Verificar que el contenidor estigui corrent

docker ps

5-Obrim el log del contanidor per a agafar el password del root generat

sudo docker logs SQLDocker

6-Busquem la linia on fiqui GENERATED ROOT PASSWORD i copiem la contrasenya en el portapapers

7-Executem el contanidor i introduim el password copiat al pas 6

sudo docker exec -it SQLDocker bash

8- Canviem la contrasenya del root utilitzants la comanda SQL ALTER USER

ALTER USER 'root'@'localhost' IDENTIFIED BY '1234';

###################################################################################################################
CONFIGURACIÓ CONTENIDOR MYSQL

#Per a modificar la configuració inicial nec esitarem crear un directori a la maquina host on guardar la nova 
#configuració i després montar la configuració en el contanidor

1- Creem la carpeta 

sudo mkdir -p /root/docker/SQLDocker/conf.d

2- Creem l'arxiu de configuració

sudo nano /root/docker/SQLDocker/conf.d/my-custom.cnf

3-Entrem la configuració que volguem, fico 1 exemple 

[mysqld]
max_connection=250 #augmenta el maxim de conneccions a 250 en ves dels 151 predefinits

4-Guardem l'arxiu i per a que la nova configuració afecti a la maquina iniciarem amb el següent codic

docker run --detach --name=SQLDocker --env="MYSQL_ROOT_PASSWORD=1234" --publish 6603:3306 --volume=/root/docker/SQLDocker/conf.d:/etc/mysql/conf.d mysql
#6603:3306 són els ports utilitzats

5-Per a saber si corre la configuració nova utilitzarem la següent comanda

mysql -uroot -pmypassword -h127.0.0.1 -P6603 -e 'show global variables like "max_connections"';

###################################################################################################################
CONECTAR HOST AL CONTENIDOR

1- Parem el contenidor

docker stop SQLDocker
docker rm SQLDocker

2-Iniciem el nou contenidor amb el port de la maquina HOST 13306

docker run -p 13306:3306 --name mysql-docker-local -eMYSQL_ROOT_PASSWORD=Password -d mysql:latest

3-Entrem a mysql

mysql --host=127.0.0.1 --port=13306 -u root -p

###################################################################################################################
CREAR VOLUM DE DADES FORA DEL CONTANIDOR

1-Comprovem on guarda les dades el contanidor

sudo docker inspect SQLDocker

2-Com que veiem quie es guarda dintre del contanidor crearem una carpeta en el host on guardarem les dades

sudo mkdir -p /storage/docker/mysql-data

3-Tornem a correr el contanidor pero aquest cop li indiquem que volem que guardi les dades en el directori anterior

docker run --detach --name=SQLDocker --env="MYSQL_ROOT_PASSWORD=1234" --publish 6603:3306 --volume=/root/docker/SQLDocker/conf.d:/etc/mysql/conf.d mysql --volume=/storage/docker/mysql-data:/var/lib/mysql mysql

4-Comprovem un altre cop on es guarden les dades

sudo docker inspect SQLDocker

5- També podem utilitzar el -v per muntar el volum

sudo docker run -v /storage/docker/mysql-data:/var/lib/mysql -e MYSQL ROOT PASSWORD=1234 -d --name SQLDocker mysql:tag 

###################################################################################################################
FUNCIONS BASIQUES

1-Arrancar un contenidor creat

sudo docker start SQLDocker

2-Reiniciar un contenidor

sudo docker restart SQLDocker

3-Parar un contenidor

sudo docker stop SQLDocker

4-Eliminar un contenidor

sudo docker rm SQLDocker

5-Crear Database Dumps

docker exec SQLDocker sh -c 'exec mysqldump --all-databases -uroot -p"$MYSQL_ROOT_PASSWORD"' > /path/all-databases.sql

6-Restaurar Database amb Dumps files

docker exec -i SQLDocker sh -c 'exec mysql -uroot -p"$MYSQL_ROOT_PASSWORD"' < /path/all-databases.sq

