# Infrastructure Hire Project 

# Setup

You will need the following:

* A fork of this repository (If you have concerns about this, let us know!)
* An AWS account (Contrast will provide a temporary one)
* Install Docker
* Install Python
* Create a virtual env `venv`
* Install local_requirements.txt (`pip install -r local_requirements.txt`)

# Deploying the current stack

```
aws cloudformation deploy --template-file infrastructure/infrastructure.yml --stack-name ops-hire-project --tags Name=ops-hire-project Environment=dev --capabilities CAPABILITY_NAMED_IAM
```

Caveats - currently relies on several very manual steps to deploy a stack. :(
 * Once the route53 hosted zone is up, take one of NS records and add the delegation to the parent domain (in my case <subdomain>.nls.systems with namecheap). With out this the alias ops-hire-project-<environment>.<subdomain>.nls.systems won't be resolvable.
    * TODO: build a separate cloudformation stack for DNS and or scripting creation of delegation record (or hosting entire domain on route53)
 * Once ACM is up, create the CNAME record. This one caught me out - Terraform can automatically create the validation CNAME in route53.
    * TODO: Google suggests that other people use a lambda to do the CNAME creation
 * Once the ECR is up, push a copy of the container up (via the instructions provided instructions provided in the repositories 'view push commands' button)
    * TODO: create some kind of CodePipeLine to automate this (unclear how it could be 'seeded' on creation of ECR)

# Tasks

- Update the infrastructure to run the container in Fargate
    * Containers running on ECS, via Fargate behind an ALB
- Add monitoring for your service
    * CloudWatch monitoring on various task metrics (number of running tasks, cpu/mem load of service, AWS spend, request rate)
    * CloudWatch Logs, logs from Gunicorn (access / exceptions / errors / startup & shutdown)
- Add an endpoint to `app.py` to return a file from an S3 bucket
    * Application fetches files and returns them as downloads. Non-existent files are handled and 404 returned.

## Things to keep in mind 

- Treat this like a production service - think about concepts such as reliability, principle of least privilege, availability, security, etc.
    * Reliability - Boosted gnuicorn workers, this increased concurrency when load testing (and reliability, because health checks were no longer stalled out by other requests)
    * Availability - Minimum 2 tasks. Autoscale group to increase number of tasks by watching cpu load
    * Security - locked down the private subnets, removed NAT gateways as outbound internet access from the container isn't required. Task uses roles with minimal privileges and or are instances of Amazon managed policies. S3 bucket has public access restrictions enabled. Added a SSL certificate to the 'outside' load balancer (and self signed certs for the inside).
- Break down the work into sizeable chunks (PR per task, commit per task, etc). Show us how you would approach this work.
    * I went with PR per feature, but left the branches behind after the squash+merges to 'show my working'.

# Bonus points!

* DNS record & subdomain (https://ops-hire-project-dev.cs1.nls.systems/ *.cs1.nls.systems)
* ACM SSL certificate (*.cs1.nls.systems)
* Very private, private subnets / VPC endpoints (no NAT GW, VPC Endpoints)
* Load tester (Locust/)
* Autoscaling Fargate (aims for 50% cpu load on service)
* Cloudwatch Logs

# Feedback

We love feedback. PR or create issues on this repository with feedback on what we could do better!