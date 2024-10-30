# eLearn Platform Management System
This project is a comprehensive learning management system (LMS) built with Django, designed to provide seamless management of courses, trainers, and student progress. It includes modules for users, trainers, and managers to enhance the learning experience and streamline administration.

## Features
- **User Module**: Students can register, enroll in courses, view course materials, and track their progress.
- **Trainer Module**: Trainers can add and manage course content, including videos, materials, and assessments.
- **Manager Module**: Managers can view students’ progress, manage courses, assign trainers, and oversee the platform.

## Tech Stack
- **Backend**: Django (Python), Django REST Framework
- **Frontend**: HTML, CSS, Bootstrap, JavaScript
- **Database**: SQLite3
- **Hosting**: PythonAnywhere

## Getting Started
- **Clone the Repository**: git clone https://github.com/reshmakp91/elearnplatformmanagementsystem.git
- **Navigate to Project Directory**: cd elearnplatformmanagementsystem
- **Install Dependencies**: Ensure you have Python and pip installed. 
- **Install dependencies from requirements.txt**: pip install -r requirements.txt
- **Configure Database**: Update the database settings in settings.py to connect to your SQLite3  instance.
- **Run Migrations**: python manage.py migrate
- **Start the Server**: python manage.py runserver
  
## Credentials for Pre-Created users

- **Super admin**:
	1. username-admin, password -admin123

- **manager**:
	1. username - anand.manager, password - anand@123

- **Trainers**:
	1. username - trainer.reshma, password - reshma@123
	2. username - trainer.arun, password - arun@123
	
- **Students**:
	1. username - vishnu92, password - vishnu92
	2. username - parvathy91, password - parvathy91
	3. username - amal93, password - amal93
	4. username - anil89, password - anil89

## Modules and Functionalities
- **User Module**: Registration, course enrollment, progress tracking.
- **Trainer Module**: Course management, video uploads, and student progress assessment.
- **Manager Module**: User administration, course oversight, and detailed student progress reports.

## License
This project is open-source and available for educational and project development purposes.
