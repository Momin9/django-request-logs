# Django Request Logs

Django Request Logs is a reusable Django app designed to log and display HTTP requests in your project. This application allows developers to monitor incoming requests, their metadata, and responses for debugging and analysis.

## Features

- Logs HTTP requests (method, path, status code, and duration).
- Provides middleware for lightweight logging.
- Easy-to-use admin interface to view logged requests.
- Flexible views and templates for displaying logs.

## Installation

Follow these steps to install and integrate Django Request Logs into your Django project:

### Step 1: Install the Package
Install the app using pip:

```bash
pip install request-logs
```

### Step 2: Add to `INSTALLED_APPS`

Update your Django settings file (`settings.py`) to include the app:

```python
INSTALLED_APPS = [
    ...,
    'request-logs',
]
```

### Step 3: Add Middleware

Insert the `RequestLoggingMiddleware` into the `MIDDLEWARE` list in your settings file:

```python
MIDDLEWARE = [
    ...,
    'request-logs.middleware.RequestLoggingMiddleware',
]
```

### Step 4: Run Migrations

Apply database migrations to create necessary tables:

```bash
python manage.py migrate
```

## Usage

### Admin Panel
Logged requests can be viewed and managed through the Django admin interface:

1. Navigate to `/admin/`.
2. Look for the `Request Logs` section.

### Fetch Logs via API
Retrieve the latest logs using the provided API endpoint:

```bash
GET /fetch-latest-logs/
```

Example response:

```json
{
  "logs": [
    {
      "id": 1,
      "method": "GET",
      "path": "/some-path/",
      "status_code": 200,
      "timestamp": "2024-11-29T12:00:00Z"
    }
  ]
}
```

### Customizing Templates

The app includes default templates for displaying logs. These can be overridden by placing templates with the same name in your project's `templates/` directory:

- `request_logs.html`
- `request_log_detail.html`

## Development

### Running Tests

Ensure the app works as expected by running the test suite:

```bash
python manage.py test request-logs
```

### Contributing

1. Fork the repository.
2. Create a feature branch:
   ```bash
   git checkout -b feature-name
   ```
3. Commit your changes and push them:
   ```bash
   git commit -m "Add feature-name"
   git push origin feature-name
   ```
4. Submit a pull request.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Support

For questions or support, please contact: [mominalikhoker589@gmail.com](mailto:mominalikhoker589@gmail.com).
