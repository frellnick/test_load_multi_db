# Docker Tests

Build tests and examples in docker and vm images.

## Load DB

Provide databases with pre-loaded data for testing

### Build with Docker
Containers can be deployed individually or as containers using Dockerfile's in each folder (one for each database).

### Build using Virtual Machine
Follow instructions in load_db/build/install.sh <- script may or may not be executable as a standalone.  

#### Build VM in GCP

**Create a Test Network**
1.  Log into cloud console or cloud SDK
2.  Create VPC network for test resources.  Example: name=test-net, subnet-name=test-net-single-region, subet-region=us-central1, ip-address-range=10.0.0.0/9, private-google-access='On'
3.  Update firewall rules -> ADD RULE: ingress, tcp=22,3389, network=test-net, source-ip=35.235.240.0/20, tags=test-db

**Create a Service Account**
1.  Log into cloud console or cloud SDK
2.  Create a IAM Service Account with storage view.  Example: name=test-data-vm, access_roles='Storage Object Viewer', 'Service Account User', 'Compute Instance Admin (v1)'


**Building the VM**
0. Set bucket name in install script or make note of where test assets are stored.
1. Log into cloud console or cloud SDK
2. Create Virtual Machine Instance (E2 medium or greater recommended for larger test sets).  Set service account and network if created. Remember network tags for test-db (database) ingress.
3. SSH into VM via instances page in cloud console or via sdk
4. Follow instructions in order from load_db/build/install.sh.
6. Start VM.  Note external IP if accessing from outside created project or ensure peering/tunneling in effect.

If firewall rule allow 0.0.0.0/0 or client source ip, databases can be viewed with DBeaver or similar.
