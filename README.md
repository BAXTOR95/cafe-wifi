# Cafe Wifi

## Introduction

Cafe Wifi is an application designed to help freelancers, students, and remote workers find cafes equipped with essential amenities like Wi-Fi, power outlets, and a conducive working environment. Users can search for cafes based on their location, view details about the amenities offered, and contribute to the community by adding new cafes to the database.

## Live Version

A live version of Cafe Wifi is available at the following link: [https://cafe-wifi-i2va.onrender.com](https://cafe-wifi-i2va.onrender.com).

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.12.0 or higher installed on your machine.
- pip for installing Python packages.

## Table of Contents

- [Installation](#installation)
- [Setting up Google Maps API Key](#setting-up-google-maps-api-key)
- [Running the Project](#running-the-project)
- [Usage](#usage)
- [Features](#features)
- [Dependencies](#dependencies)
- [Configuration](#configuration)
- [Examples](#examples)
- [Contributors](#contributors)
- [License](#license)

## Installation

To set up the Cafe Wifi project locally:

1. Clone the repository:

   ```bash
   git clone https://github.com/BAXTOR95/cafe-wifi.git
   ```

2. Navigate to the project directory:

   ```bash
   cd cafe-wifi
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

4. Create an administrative user:

   ```bash
   flask --app run.py create-admin admin@example.com "strongpassword" "Admin Name"
   ```

5. Set up the environment variables by creating a `.env` file in the root directory with the following content:

   ```plaintext
   MAPS_API_KEY=your_google_maps_api_key
   CSRF_KEY=your_custom_csrf_key
   SQLALCHEMY_DATABASE_URI='sqlite:///cafes.db'
   PROD=False
   ```

## Setting up Google Maps API Key

To fully utilize the map functionalities within the Cafe Wifi application, you'll need a Google Maps API key. Here's how to obtain and set up your API key:

1. **Create a Google Cloud Project**:

   - Visit the [Google Cloud Console](https://console.cloud.google.com/).
   - If you do not have a Google Cloud account, you will need to create one and sign in.
   - Click on "Create Project", give your project a name, and click "Create".

2. **Enable Google Maps APIs**:

   - Once the project is created, navigate to the "APIs & Services > Dashboard" panel.
   - Click on "+ ENABLE APIS AND SERVICES" at the top of the page.
   - Search for "Maps JavaScript API" and enable it.
   - Repeat this process to also enable "Places API" and any other APIs you plan to use (e.g., "Geocoding API" if needed).

3. **Create API Key**:

   - Go to the "Credentials" tab on the left sidebar.
   - Click on "+ CREATE CREDENTIALS" and select "API key".
   - Once the API key is created, you can restrict it to improve security:
     - Click on the name of the key.
     - Under "Application restrictions", select "HTTP referrers (websites)".
     - Add the URLs where your application is hosted (e.g., `https://yourwebsite.com/*`).
     - Under "API restrictions", select "Restrict key" and choose the APIs you enabled.

4. **Add the API Key to Your Project**:

   - Copy the created API key.
   - Open your `.env` file in the root directory of your project.
   - Add or update the `MAPS_API_KEY` variable with your new key:

     ```plaintext
     MAPS_API_KEY=your_new_google_maps_api_key
     ```

5. **Test the API Key**:
   - Run your application.
   - Access a feature that uses Google Maps to ensure the API key is working correctly. If there are any errors, they will typically be logged in the browser's console, indicating what might be wrong.

By following these steps, you should have a functional Google Maps API key integrated into your Cafe Wifi project, enabling full map capabilities.

## Running the Project

To run Cafe Wifi on your local machine, use the following command:

```bash
flask --app run.py run
```

This will start a development server, and you can access the blog at `http://localhost:5000`.

## Usage

Users can create an account to suggest new cafe locations. The application features a visual map where cafes are displayed, allowing users to see all listings or filter them based on their preferences like Wi-Fi availability, power outlets, and more.

## Features

- **Listing Cafes**: View all cafes or a random selection that meets specific criteria.
- **Filtering Cafes**: Filter cafes based on amenities like Wi-Fi, outlets, and toilets.
- **Adding and Suggesting New Cafes**: Users can add new cafes to the database.
- **Google Maps Integration**: Easily add addresses and visualize cafe locations on a map.
- **Admin Features**: Manage cafe entries, including deletion of entries.

## Dependencies

Ensure all dependencies are installed from `requirements.txt`. Additionally, a valid Google Maps API key is required for map functionality.

## Configuration

No additional configuration is needed beyond setting up the `.env` file as described in the [Installation](#installation) section.

## Examples

[Add specific examples demonstrating how to use the application, including any common operations like adding a cafe, filtering the cafe list, etc.]

## Contributors

We welcome contributions to FlaskBlog! If you have suggestions for improvements or bug fixes, please fork the repository and submit a pull request. For major changes, please open an issue first to discuss what you would like to change.

Ensure to update tests as appropriate.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.md) file for details.
