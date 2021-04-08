------------
Run keycloak
------------

* `make run` in /auth-enki folder
* Go to localhost:8080
* log in: admin, pwd: Pa55w0rd
* Go to administration console
* Click import & "select file"
* auth-enki/realm-export.json

If you modify .ftl files or properties, don't forget to restart docker containers: 
* `docker ps` to see all instances of docker
* `docker restart [container_id]` to restart a container

See more at https://jira.nexsis18-112.fr/confluence/display/ENKI/Installation+de+ENKI+pour+dev

---------------------------
Work on keycloak design CSS
---------------------------

* Run the command `sass --watch scss/main.scss css/main.css` in the folder enki-theme/login/resources