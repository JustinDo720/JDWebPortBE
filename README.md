# JDWebPortBE 

---

### Django Backend for my Website Portfolio project 

---

## Key Features:

- [RESTAPI]('https://www.django-rest-framework.org/')
- [AWS Elastic Beanstalk Hosting]('https://aws.amazon.com/elasticbeanstalk/') 
- [AWS RDS DB]('https://aws.amazon.com/rds/')
- [AWS S3 Bucket]('https://aws.amazon.com/s3/')
- [SJWT Auth]('https://django-rest-framework-simplejwt.readthedocs.io/en/latest/') 

## Packages & Tools (to be updated):

- [Django]('https://www.djangoproject.com/')
- [Djangorestframework]('https://www.django-rest-framework.org/')
- [Faker]('https://pypi.org/project/django-faker/') 
- [Django Storages]('https://django-storages.readthedocs.io/en/latest/')
- [Postman]('https://www.postman.com/')
- [Lorem Picsum]('https://picsum.photos/')

## Steps (to be updated):
- [x] Initialize Django Application and create a home page 
- [x] Set up some related models to our application
    - Biography
    - Projects (details)
    - Showcase Projects (walkthrough/sample?)
    - Contact me
- [x] Create our admin view and super user 
- [x] Start connecting our django app with Restapi 
- [x] Create API endpoints and fill them with fake data using Faker
     - Pagination
     - API Endpoints
  -[x] Biography (get, post, put, delete)
  -[x] Project (get, post, put, delete)
  -[x] Contact me (get, post, put, delete)
- [x] Create your own permissions for Admin users only
- [x] Add Authentication system before testing endpoints  
     - BE SURE TO DISABLE LINE 19 and ENABLE LINE 18 AFTER AUTH SYS
- [x] Test API endpoints using postman 
     - API Endpoints:
  -[x] Biography (get, post, put, delete)
  -[x] Project (get, post, put, delete)
  -[x] Contact me (get, post, put, delete) 
- [x] Work on images and test them using Lorem Picsum
- [x] Pagination on projects?
- [x] Switch local storages to Django Storages (AWS S3 Bucket or others) 
- [x] ~~Switch database to AWS RDS (relational database service) (Postgresql DB)~~ Changed to ElephantSQL due to Excessive Payments to AWS :C 
- [x] ~~Deploy with AWS Elastic Beanstalk~~ Changed to another Deployment due to Excessive Payments to AWS :C
- [ ] Revamped API version for jdwebportfe
  - [x] About Me API 
    - Short & Long Bio, quote w/ author
  - [ ] Contact Me API 
    - Files and Feedback questions 
  - [ ] Resume API 
    - Info, Skills, Projects, awards and achievements 
  - [ ] Projects API 
    - Current Workings, All Projects, Specific Projects, Notes Model 
  - [ ] Profile API 
    - Socials, Quick Description and Name