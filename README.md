# LibraryBackend

Welcome to the LibraryBackend repository! This project is built using Django and Django Ninja, providing a robust backend for a library management system. Additionally, it includes a custom CLI tool built with Rav Python for efficient management.

## Table of Contents
- [Features](#features)
- [Getting Started](#getting-started)
- [Installation](#installation)
- [Running the Project](#running-the-project)
- [Running the CLI Tool](#running-the-cli-tool)
- [API Documentation](#api-documentation)
- [Folder Structure](#folder-structure)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## Features

- **Book Management**: Add, update, and remove books from the library.
- **User Authentication**: Secure authentication with JWT tokens.
- **Search and Filter**: Search for books by title, author, or genre.
- **Admin Interface**: Django admin interface for managing the backend.
- **CLI Tool**: Custom Rav Python CLI tool for administrative tasks.

## Getting Started

To get a local copy of the project up and running, follow these simple steps.

### Prerequisites

Ensure you have the following installed:
- Python 3.8 or higher
- pip
- virtualenv

### Installation

1. **Clone the repository**:
    ```bash ssh
    git clone git@github.com:CoDedArch/LibraryBackend.git
    ```
    ```bash https
    git clone https://github.com/CoDedArch/LibraryBackend.git
    ```
2. **Navigate to the project directory**:
    ```bash
    cd LibraryBackend
    ```
3. **Create a virtual environment**:
    ```bash
    python -m venv venv
    ```
4. **Activate the virtual environment**:
    - On Windows:
      ```bash
      venv\Scripts\activate
      ```
    - On macOS/Linux:
      ```bash
      source venv/bin/activate
      ```
5. **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
6. **Set up the database**:
7. ```bash
    rav run makemigrations
    ```
    ```bash
    rav run migrate
    ```
8. **Create a superuser**:
    ```bash
    rav run superuser
    ```

## Running the Project

To start the development server, run:
```bash
rav run server

## Contribution
When  you done cloning, switch to a new brach, implement the feature and push it. after wards open a pr on github.
