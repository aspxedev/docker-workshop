# docker-workshop

## Contenedores Docker

### Listar
```bash
# Solo los activos
docker ps

# Todos (incluye detenidos)
docker ps -a
```

### Crear
```bash
# Básico
docker run ubuntu

# Interactivo con terminal
docker run -it ubuntu bash

# Con nombre personalizado
docker run -it --name mi_contenedor ubuntu bash
```

### Ejecutar contenedor existente
```bash
# Iniciar un contenedor detenido
docker start <nombre_o_id>

# Iniciar y conectarse a él
docker start -ai <nombre_o_id>

# Conectarse a uno ya corriendo
docker exec -it <nombre_o_id> bash
```

### Eliminar
```bash
# Uno específico
docker rm <nombre_o_id>

# Todos los detenidos
docker container prune

# Forzar eliminación (aunque esté corriendo)
docker rm -f <nombre_o_id>
```

# Tomar un punto de entrada para el contenedor
```bash
docker run -it --entrypoint=bash -v $(pwd)/test:/app/test python:3.13.11-slim
```

# Crear contenedor con base de datos de postgresql
```bash
docker run -it --rm \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v ny_taxi_postgres_data:/var/lib/postgresql \
  -p 5432:5432 \
  postgres:18
```

# Conectarse a la base de datos corriendo en el contenedor
```bash
uv run pgcli -h localhost -p 5432 -u root -d ny_taxi
```

# Ejecutar el contenedor con el pipeline. Esto va a fallar porque tenemos que configurar la red del contenedor, que busque conexión al contenedor de postgresql
```bash
docker run -it --rm \
  taxi_ingest:v001 \
  --pg-user=root \
  --pg-pass=root \
  --pg-host=localhost \
  --pg-port=5432 \
  --pg-db=ny_taxi \
  --target-table=yellow_taxi_trips \
  --year=2021 \
  --month=1 \
  --chunksize=100000
```  

# Crear la red 
```bash
docker network create pg-network
```

# Es necesario ejecutar el contenedor de la base de datos con estos argumentos
```bash
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v ny_taxi_postgres_data:/var/lib/postgresql \
  -p 5432:5432 \
  --network=pg-network \
  --name pgdatabase \
  postgres:18
```

# Ejecutar el contenedor con el pipeline, versión que se ejecuta en la red creada
```bash
docker run -it \
  --network=pg-network \
  taxi_ingest:v001 \
    --pg-user=root \
    --pg-pass=root \
    --pg-host=pgdatabase \
    --pg-port=5432 \
    --pg-db=ny_taxi \
    --target-table=yellow_taxi_trips_2021_2 \
    --year=2021 \
    --month=2 \
    --chunksize=100000
```

# Para ejecutar un contenedor con pgAdmin
```bash
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -v pgadmin_data:/var/lib/pgadmin \
  -p 8085:80 \
  --network=pg-network \
  --name pgadmin \
  dpage/pgadmin4
```

# Ejecutar los contenedores con docker-compose
```bash
docker-compose up -d
```

# Detener contenedores
```bash
docker-compose down
```

# Ver logs
```bash
docker-compose logs
```

# Para contenedores y remover volumenes
```bash
docker-compose down -v
```