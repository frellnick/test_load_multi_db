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


### Run Statements
* loader        docker run --name pyloader --network host --mount type=bind,source=/path/to/data/folder,target=/data vbrandon/pyloader python app.py --dbtype postgres --uri postgres://docker:dockerpass@127.0.0.1:5432/testdata
* MySQL         docker run -it -p 3306:3306 --network network --name testmsql --mount type=bind,source=/path/to/data/folder,targer=/data repo/mysql:tag --local-infile=1
* PostgreSQL    docker run -it -p 5432:5432 --network network --name testpostgres --mount type=bind,source=/path/to/data/folder,target=/data repo/postgres:tag


### REPL, Jupyter Notebook, and bash interfaces
* loader(Jupyter Notebook)


```bash
# This will create a container in the 'host' network.  Use any network the DB attached to.
docker run -p 8888:8888 --name pyloader vbrandon/pyloader:V0 jupyter notebook --ip 0.0.0.0 --allow-root --no-browser
```


### Testing

### Local Testing (Outside of container network with clean symlink/mount)
 
 ```bash
 # Pass relative path to data directory as well as database connection information
 python app.py --dbtype postgres --uri postgres://docker:dockerpass@127.0.0.1:5432/testdata --datadir ../data
 ```