# StudyingIt

*Your reliable assistant for honing the skills of solving algorithmic problems! Simple, intuitive and with a large
collection of tasks, it is the perfect companion for preparing for interviews and programming competitions!*

**Live** - [studyingit.ru](https://studyingit.ru)
___

## :dizzy: Opportunities

- **3 supported languages** for problem-solving (Python, C++, Go)
- **Daily streak counter** to track consistent practice
- *(Coming soon)* Email reminders for inactive users
- *(Coming soon)* Kafka-powered real-time notifications

___

## :computer: Tech Stack

### Core
![Django](https://img.shields.io/badge/Django-5.1.1-green)
![DRF](https://img.shields.io/badge/Django_REST-3.15.2-blue)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-17-blue)
![Redis](https://img.shields.io/badge/Redis-7.4.3-red)
___

## ⚙️ Infrastructure  

![Nginx](https://img.shields.io/badge/Nginx-1.25-269539?logo=nginx)  
![Docker](https://img.shields.io/badge/Docker-24.0-2496ED?logo=docker)  
![Gunicorn](https://img.shields.io/badge/Gunicorn-20.1-499848?logo=gunicorn)  

 ___

## 🔧 Development Tools  

![Git](https://img.shields.io/badge/Git-2.40-F05032?logo=git)  
![GitHub Actions](https://img.shields.io/badge/GitHub_Actions-2088FF?logo=github-actions)


___
## 🤝 How to Contribute

We welcome contributions from everyone! Here's how to get started:

1. **🎯 Fork the Project**  
   Click the 'Fork' button at the top right of this repository

2. **🌿 Create Your Branch**  
   ```bash
   git checkout -b feature/your-awesome-feature

3. ** 💾 Commit Your Changes**
   ```bash
   git checkout -b feature/your-awesome-feature

4. **🚀 Push to GitHub**
   ```bash
   git push origin feature/your-awesome-feature

5. **🔀 Open a Pull Request**
    * Go to your forked repository
    * Click "New Pull Request"
    * Fill in the PR template
 ___

## :space_invader: Installation

#### 1. Set up virtual environment
```bash
python3 -m venv venv
source venv/bin/activate
```
#### 2. Clone repository
```bash
git clone https://github.com/IlyaBudkovoy21/StudyingIt.git
cd StudyingIt/
pip install -r requirements.txt
```
#### 3. Configure environment
Сreate .env file and define:
```ini
# Database configuration
DB_USER=your_username
DB_PASSWORD=your_password
HOST_DB=localhost
PORT_DB=5432

# Service settings
PORT_SERVICE=8000
IP_SERVICE_1=127.0.0.1
DOMAIN_API=yourdomain.com
```
#### 4. Prepare logs structure
```bash
cd src/
mkdir -p logs/{profile,coding,listTasks} && \
touch logs/profile/{views,permissions}.log \
     logs/coding/{views,permissions,s3}.log \
     logs/listTasks/views.log
cd ..
```
#### 5. Launch with Docker
```bash
docker compose -f docker-compose.yml up -d --build
```


  
