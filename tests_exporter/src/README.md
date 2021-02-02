# Docker commands (building individual containers)

```bash
docker build -f path/to/dockerfile -t repo/tag .
```


## Running with mounted volume
In order to give multiple containers dynamic access to either a GCS bucket or local drive, the mount must be specified.

This must be configured at instantiation for the most part.

```bash
docker run --mount type=bind,source=/path/to/source,target=/path/to/target
```

## Examples

PostgreSQL
* Mounted Volume
* Username, Password, DatabaseName configured in dockerfile
```bash
docker run -d -it -p 5432:5432\
--name testdb \
--mount type=bind,source="$(pwd)"/data,target=/data \
vbrandon/postgres:v0
```


### Ports
* MySQL         3306:3306
* PostgreSQL    5432:5432


### Required Run Flags
* MySQL         --local-infile=1


#### Run Statements
* MySQL         docker run -it -p 3306:3306 --name testmsql --mount type=bind,source=/path/to/data/folder,targer=/data repo/mysql:tag --local-infile=1
* PostgreSQL    