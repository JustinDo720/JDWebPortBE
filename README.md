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
- [x] Revamped API version for jdwebportfe
  - [x] About Me API 
    - Short & Long Bio, quote w/ author
  - [x] Contact Me API 
    - Files and Feedback questions 
  - [x] Resume API 
    - Info, Skills, Projects, awards and achievements 
  - [x] Projects API 
    - Current Workings, All Projects, Specific Projects, Notes Model 
  - [x] Profile API 
    - Socials, Quick Description and Name
- [x] Work on Sub APIs (Creating APIs for requests that build our main Revamped APIs)
  - [x] Resume Projects Sub API 
  - [x] Posting new Resume API --> functional based API to create a new resume info   
  - [x] Resume Awards & Achievements Sub API 
  - [x] Social Profiles Sub API
- [x] Create Faker Scripts for sub API
- [ ] Deploy
  - [x] Before we deploy make sure to update the API viewset route 
    - [x] Profile Viewset (Profile, Socials Profile)
    - [x] Biography Viewset (Biography, BiographySection, BiographySectionImage)
    - [x] Project Viewset (Project, CurrProj, ProjectNotes, ProjectImage)
    - [x] Resume Viewset (Resume, ResumeProjects, ResumeProjectDetails, ResumeAwardsandAchievement)
    - [x] Feedback Viewset (Contact Me, Feedback)
  - [x] Test API endpoints (we need to pass request in context for serializer)
  - [ ] Reconfigure new Database
  - [x] Storage for Pictures (maybe use Google Cloud Storage again) 
  - [ ] I heard we could deploy with Google check that
  