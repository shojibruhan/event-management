# Event Management System

## Introduction

This Event Management System is a web application built using Django, following the Model-View-Template (MVT) architectural pattern. It's designed to facilitate the creation, management, and participation in various events. The frontend is styled using Tailwind CSS, ensuring a modern and responsive user interface without relying on JavaScript for core functionality.

## Features

* **Event Creation & Management:** Users (e.g., event organizers, administrators) can create, edit, and delete events.
* **Event Listing:** Browse and view details of available events.
* **User Authentication:** Secure user registration, login, and logout.
* **Event Participation/Registration:** Users can register for events.
* **Responsive Design:** Styled with Tailwind CSS for a consistent experience across various devices.
* **Pure Python & HTML:** Built entirely with Django's Python backend and standard HTML templates, avoiding JavaScript for core interactions.

## Technologies Used

* **Django:** High-level Python web framework.
* **SQLite3:** Default database for development (can be configured for PostgreSQL, MySQL, etc., in production).
* **Tailwind CSS:** A utility-first CSS framework for rapid UI development.

## Getting Started

### Prerequisites

* Python (3.8+)
* pip (Python package installer)
* Virtual environment (highly recommended)

### Installation

1.  **Clone the repository:**

    ```bash
    git clone [https://github.com/shojibruhan/event-management.git](https://github.com/shojibruhan/event-management.git)
    cd event-management
    ```

2.  **Create and activate a virtual environment:**

    ```bash
    python -m venv venv
    # On Windows:
    .\venv\Scripts\activate
    # On macOS/Linux:
    source venv/bin/activate
    ```

3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```

    *If you don't have a `requirements.txt` yet, you might need to install them manually first and then generate it:*
    ```bash
    pip install django tailwindcss # Add other dependencies like pillow if used for images
    pip freeze > requirements.txt
    ```

4.  **Apply database migrations:**

    ```bash
    python manage.py migrate
    ```

5.  **Create a superuser (for administrative access):**

    ```bash
    python manage.py createsuperuser
    ```

6.  **Run the development server:**

    ```bash
    python manage.py runserver
    ```

    The application will be accessible at `http://127.0.0.1:8000/`.

## Usage

* **Admin Panel:** Access the Django admin panel at `http://127.0.0.1:8000/admin/` using your superuser credentials to manage users, events, and other data directly.
* **User Registration:** Users can register for an account through the application's frontend (assuming a registration page is implemented).
* **Event Browse:** Navigate to the home page or an events listing page to see available events.
* **Event Details:** Click on an event to view its detailed information.
* **Event Creation:** Logged-in users with appropriate permissions (e.g., staff, superuser) can create new events through dedicated forms.

*Note: `project_name` and `app_name` are placeholders. Replace them with your actual project and app names.*

## Contributing

Contributions are welcome! If you'd like to contribute, please follow these steps:

1.  Fork the repository.
2.  Create a new branch (`git checkout -b feature/your-feature-name`).
3.  Make your changes.
4.  Commit your changes (`git commit -m 'Add new feature'`).
5.  Push to the branch (`git push origin feature/your-feature-name`).
6.  Create a Pull Request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For any inquiries, please contact [Your Name/Email] or open an issue on GitHub.
