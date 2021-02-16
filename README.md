# Docker Tests

Build tests and examples in docker and vm images.

## Load DB

Provide databases with pre-loaded data for testing

### Build with Docker
Containers can be deployed individually or as containers using Dockerfile's in each folder (one for each database).

### Build using Virtual Machine
Follow instructions in load_db/build/install.sh <- script may or may not be executable as a standalone.  

#### Build VM in GCP
1. Log into cloud console or cloud SDK
2. Create Virtual Machine Instance (E2 standard or greater recommended for larger test sets)
3. SSH into VM via instances page in cloud console or via sdk
4. Follow instructions in order from load_db/build/install.sh
5. Create network firewall rule for TCP 5432, 3306.  Suggest using network tags to only apply to test instance.
6. Start VM.  Note external IP if accessing from outside created project or ensure peering/tunneling in effect.

If firewall rule allow 0.0.0.0/0 or client source ip, databases can be viewed with DBeaver or similar.
