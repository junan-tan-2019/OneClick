# Team 5 One Click
Group Project for CS302 IT Solution Lifecycle Management.

A local version of the OneClick Application (Previously placed in Gitlab based on project requirements).

Application created by:
- Jun An (Github username: junan-tan-2019)
- Derrick Lim (Github username: derrick-lim-2019)
- Keah Keat Tan (Github username: kk-tan-2019)
- Jolene Loh
- See Kexin

### Run the microservices with this command
```
docker compose up -d --build
```
#### Note: In the docker compose yml file, under service 1 there's a command `command : ["./wait-for-it.sh", "-t", "20", "mysql:3306", "--", "node", "app.js"]` to wait for every 20 secs to check if mysql is ready before starting the service 1 container. If you think the docker-compose process is too slow you can change the time (in secs) to no less than 10 secs. This wait-for-it.sh is added to start off service 1 after mysql database is ready for connection. (Due to issues with the service 1 having faster start up than mysql container, we modify the service 1 docker file with the added .sh file. These modifications are not push to gitlab as it is not necessary.)

<br>

### URL links to visit
* localhost:31000/stocks
* localhost:30000/register
* localhost:33000/api/qr/(any number or chars)
    * e.g. /api/qr/ABC123456
* localhost:32000/vending_machine/collection

<br>

### Steps to test the application
1. Visit `/stocks `to view each of the location's stock quantity. Record down the location that you like for easy reference.

2. Go to `/register`. Register with any unique ref number (Can use ABC1234), the location that you have picked, and your actual phone number. You will receive an SMS message to visit the QR code page.
    * Note that AWS only allows approximately 18 messages to be send for each month.

3. You may click the link in the message to visit the QR page (which is hosted in AWS ECS), or the local end version (where you have to type your reference number) which is `localhost:33000/api/qr/(your reference number)`.

4. Visit `/vending_machine/collection`, key in the unique ref number that you have registered. Click submit. You will receive another SMS message stating that you have collected your item.

5. Navigate to `/stocks` again, and you will see the quantity has been deducted by 1 in the location that you have picked.

<br>

### Folder structure

```
.
|--services
|  |--service0
|  |    |--ci
|  |    |--tests
|  |    |--src
|  |    |   |--templates
|  |    |   `--service_0.py
|  |    |--Dockerfile
|  |    |--requirements.txt
|  |   `--.gitlab-ci.yml
|  |--service1
|  |  |--src
|  |  | |--public
|  |  |--views
|  |  |--app.js
|  |  |  |--package-lock.json
|  |  |  |--package.jsom
|  |  |  |--.gitlab-ci.yml
|  |  |  |--Dockerfile
|  |  |  `--wait-for-it.sh
|  |--service2
|  |  |--src
|  |  |  `--app.py
|  |  |--.gitignore
|  |  |--.gitlab-ci.yml
|  |  `--serverless.yml
|  |--service3
|  |  |--src
|  |  |  `--app.py
|  |  |--.gitlab-ci.yml
|  |  |--Dockerfile
|  |  `--requirements.txt
|  `--serivce4
|     |--service
|     |  |--src
|     |  |  |--templates
|     |  |  `--app.py
|     |  |--Dockerfile
|     |  |--.gitlab.yml
|     |   `--requirements.txt
|     `--receiver
|        |--src
|        |   `--receive_order.py
|        |--.gitlab-ci.yml
|        |--Dockerfile
|        `--requirements.txt
|--dev.env
|--docker-compose.yml
|--production.env
|--README.md
|--schemas.sql

```
