# Project Title: Carpool Matching Platform

## Project Overview
This project is a full-stack carpool matching platform designed to reduce traffic congestion by connecting users with similar travel routes and schedules. The application includes user registration, route-matching algorithms, data visualizations, and a user-friendly interface.

---

## Table of Contents
- [System Requirements](#system-requirements)
- [Dependencies](#dependencies)
- [Running the Application](#running-the-application)
- [Usage Instructions](#usage-instructions)

### System Requirements
- **Operating System**: Compatible with Windows, macOS, and Linux.
- **Python**: Version 3.11.7
- **Node.js** (for front-end dependencies):Version 20.12.2

### Dependencies
- Ensure you have `pip` installed, then install the required Python libraries with:
	pip install -r requirements.txt


- Navigate to the Frontend directory and install dependencies with: 
	cd Frontend
	npm install

### Running the Application
#### Starting the server
1. Navigate to the `Frontend` directory:
	cd Frontend
2. Run the server with:
   	python app.py
3. Access the application at http://127.0.0.1:5000 in your web browser.

### Running the Matching Algorithm
Drive2’s matching algorithm connects users with similar travel routes and preferences, running periodically in the background.

1. Navigate to the `Algorithm` directory:
	cd Algorithm
2. Execute the matching algorithm with:
   	python Matching_v3.py


### Usage Instructions
### Database configuration (if requested by the Tableau server)
https://www.db4free.net/phpMyAdmin/index.php?route=/database/structure&db=drive2_db
- **Access**: Configured on db4free.net, accessible via phpMyAdmin.
- **User**: `steven3397`
- **Password**: `pass123word`

### User configuration
- Please register for an account in the website and login using the chosen credentials.
- In case of issues creating a new account, use the following credential:
 - **User**: `testing123`
- **Password**: `testing123`

### Note
- Use the website in full-screen for best experience, as responsive design hasn't been implemented.
- Access the visualisation interface from 'Admin' button in the landing page.
- The Tableau Cloud visuals are currently inaccessible due to an ongoing migration to Salesforce's Hyperforce platform, which temporarily prevents changes to the embed settings for public view. The visuals will be updated as soon as access to Tableau Cloud is restored (ETA 16th Nov 2024).


