# StudyingIt

*Your reliable assistant for honing the skills of solving algorithmic problems! Simple, intuitive and with a large
collection of tasks, it is the perfect companion for preparing for interviews and programming competitions!*

link - https://studyingit.ru
___

## :dizzy:Opportunities

1. There are 3 programming languages available for solving problems;
2. For each registered user, there is a counter for consecutive days in which at least one task has been completed;
3. (soon) A reminder in the mail that the user has not solved the problem for a long time.

___

## :space_invader:Installation

1. python3 -m venv venv;
2. source venv/bin/activate;
3. git clone https://github.com/IlyaBudkovoy21/StudyingIt.git;
4. cd StudyingIt/;
5. pip install -r requirements.txt;
6. create .env file and define:
    - DB_USER;
    - DB_PASSWORD;
    - HOST_DB;
    - PORT_DB;
    - PORT_SERVICE;
    - IP_SERVICE_1;
    - DOMAIN_API;
7. cd src/;
8. mkdir -p logs/{profile,coding,listTasks} && \
touch logs/profile/{views,permissions}.log \
     logs/coding/{views,permissions,s3}.log \
     logs/listTasks/views.log;
9. cd ..;
10. docker compose -f docker-compose.yml up -d --build;

___

