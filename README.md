
# Spekit Test

A dockerized Django based API that stores “digital documents” in “folders”. Folders or Documents can have one or many associated “Topics”, with short & long-form descriptors.

### Depedencies  
[Docker](https://docs.docker.com/get-docker/)  
[Docker Compose](https://docs.docker.com/compose/install/) 

## Local Setup
`$ git clone https://github.com/codvlpr/spekit.git spekit`  
`$ cd spekit`  
`$ docker-compose build`  
`$ docker-compose up -d `  
`$ docker exec -ti spekit_web_1 python manage.py migrate `  
`$ docker exec -ti spekit_web_1 python manage.py createsuperuser `  
`$ docker exec -ti spekit_web_1 python manage.py populate_example_data`

Development server will be available at `http://localhost:8000/`  
Django admin app will be available at `http://localhost:8000/admin/`
