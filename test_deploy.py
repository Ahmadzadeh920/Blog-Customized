name: Customized Blog Project Test and Deploy

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:

    Test:
    name: Test
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v3
    - name: Setup Docker-Compose
        run: docker-compose up --build -d
        
    # - name: Run Tests
    #run: docker-compose exec backend sh -c "pytest ."
    # run: docker-compose exec backend sh -c "flake8 && pytest ."
        
        
    Deploy:
        name: Deploy 
        runs-on: ubuntu-latest
        steps:
        - uses: actions/checkout@v3
        - name: Connect and Execute Commands
        uses: appleboy/ssh-action@master
        with:
            username:{{secrets.username}}
            password:{{secrets.password}}
            host:{{secrets.host}}
            port:{{secrets.port}}
            script:

       

   # - name: Run Tests
      #run: docker-compose exec backend sh -c "pytest ."
      # run: docker-compose exec backend sh -c "flake8 && pytest ."