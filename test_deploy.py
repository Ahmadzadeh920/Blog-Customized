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
        if: ${{always() && contains(join(needs.*.result, ',') , 'success')}}
        needs: Test
        runs-on: ubuntu-latest
        steps:
        - uses: actions/checkout@v3
        - name: Connect and Execute Commands
        uses: appleboy/ssh-action@master
        # to coonect to server and implement some instructions 
        with:
            # to coonect to server
            username:  ${{secrets.Username}}
            password:  ${{secrets.Password}}
            host:   ${{secrets.Host}}
            port:   ${{secrets.Port}}
            # to implement some instructions
            script: |
                cd ${{secrets.Project_Path}} 
                docker-compose -f docker-compose-stage.yml stop 
                git pull 
                docker-compose -f docker-compose-stage.yml restart 
                

       

   # - name: Run Tests
      #run: docker-compose exec backend sh -c "pytest ."
      # run: docker-compose exec backend sh -c "flake8 && pytest ."