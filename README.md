![Python](https://img.shields.io/badge/Python-3670A0?style=for-the-badge&logo=python&logoColor=white)
![Django](https://img.shields.io/badge/Django-092E20?style=for-the-badge&logo=django&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![Bootstrap](https://img.shields.io/badge/Bootstrap-7952B3?style=for-the-badge&logo=bootstrap&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-003B57?style=for-the-badge&logo=sqlite&logoColor=white)
![GitHub](https://img.shields.io/badge/GitHub-181717?style=for-the-badge&logo=github&logoColor=white)


## Project Overview

**GroupPortal** is a collaborative web application built with Django designed to provide:
- Authenticated user profiles
- Forum for discussions
- Electronic gradebook
- Events & calendar
- Polling & voting systems
- Resources, announcements, gallery, portfolio

This README describes project goals, structure, and setup instructions.

## Table of Contents
1. [Features](#features)  
2. [Architecture](#architecture)  
3. [Installation](#installation)  
4. [Usage](#usage)  
5. [Contributing](#contributing)  
6. [License](#license)

## Features

**Authentication**
- Registration, login, roles (user/moderator/admin)

**Forum**
- Topics, posts, moderator controls

**Gradebook**
- View and manage grades

**Events & Calendar**
- Event creation and visualization

**Polls & Voting**
- Multi-step polls
- Voting with single responses

**Announcements & Materials**
- Management of materials and media

**Portfolio & Gallery**
- User portfolios and image/gallery submissions

##  Architecture

The backend is implemented with **Django** using multiple apps:
- `accounts`, `forum`, `grades`, `events`, `polls`, `votes`, `announcements`, `portfolio`
Each handles a separate feature set to support teamwork.

Frontend uses:
- HTML5, CSS3
- Bootstrap for responsive styling
