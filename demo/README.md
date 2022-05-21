# Como lanzar la demo:

Se recomiendan tener 5 terminales para que sea mas facil de ver todo:

## Terminal 1
En la terminal 1 tendremos el broker del edge

```bash
docker-compose up --build broker-edge
```

## Terminal 2
En la terminal 2 tendremos el broker del edge

```bash
docker-compose up --build edge-service
```

## Terminal 3
En la terminal 3 tendremos el broker del cloud

```bash
docker-compose up --build broker-cloud
```

## Terminal 4
En la terminal 4 tendremos el cloud-service

```bash
docker-compose up --build broker-edge
```

## Terminal 5
En la terminal 5 tendremos el iot que enviara datos. Deberemos ir a la carpeta IoT i ejecutar:

```bash
docker build -t iot .
docker run -t iot
```
    
