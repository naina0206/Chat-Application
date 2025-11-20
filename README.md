# 💬 Real-Time Chat Application

A full-featured real-time chat application built with Django Channels, WebSockets, and PostgreSQL. This application enables users to register, authenticate, and engage in real-time one-on-one messaging with message history persistence.

## 🚀 Features

- **Real-Time Messaging**: WebSocket-based instant messaging using Django Channels
- **User Authentication**: Secure signup and login system with Django's built-in authentication
- **Message Persistence**: All messages are stored in PostgreSQL database with timestamp tracking
- **Message History**: Retrieve and display previous conversations between users
- **Modern UI**: Responsive, gradient-based design with smooth user experience
- **Connection Status**: Visual indicator showing WebSocket connection status
- **Production Ready**: Configured with Nginx, Gunicorn, and Daphne for deployment

## 🛠️ Tech Stack

### Backend
- **Django 5.2.7**: High-level Python web framework
- **Django Channels 4.3.1**: WebSocket and async support for Django
- **PostgreSQL**: Relational database for message storage
- **Redis 6.4.0**: Channel layer backend for WebSocket communication
- **Daphne 4.1.2**: ASGI HTTP/WebSocket server
- **Gunicorn 23.0.0**: WSGI HTTP server for production

### Frontend
- **HTML5/CSS3**: Modern, responsive UI with gradient design
- **JavaScript**: WebSocket client implementation
- **Django Templates**: Server-side templating

### Infrastructure
- **Nginx**: Reverse proxy and load balancer
- **ASGI**: Asynchronous Server Gateway Interface

## 📋 Prerequisites

Before running this application, ensure you have the following installed:

- Python 3.12+
- PostgreSQL 12+
- Redis 6.0+
- pip (Python package manager)

## 🔧 Installation

### 1. Clone the Repository

```bash
git clone <repository-url>
cd ChatApp
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Database

Create a PostgreSQL database:

```sql
CREATE DATABASE chatdb;
CREATE USER new_user WITH PASSWORD 'welcome@123';
GRANT ALL PRIVILEGES ON DATABASE chatdb TO new_user;
```

**Note**: For production, use environment variables for database credentials (see `.env.example`).

### 5. Configure Environment Variables

Copy the example environment file and update with your values:

```bash
cp .env.example .env
```

Edit `.env` with your actual credentials.

### 6. Run Migrations

```bash
cd ChatApplication
python manage.py migrate
```

### 7. Create Superuser (Optional)

```bash
python manage.py createsuperuser
```

## 🚀 Running the Application

### Development Mode

Use the provided startup script:

```bash
./start_dev.sh
```

Or manually:

```bash
# Terminal 1: Start Redis
redis-server

# Terminal 2: Run Django with Daphne
cd ChatApplication
daphne -b 0.0.0.0 -p 8000 ChatApplication.asgi:application
```

The application will be available at `http://localhost:8000`

### Production Mode

1. **Collect Static Files**:
```bash
python manage.py collectstatic
```

2. **Start with Gunicorn** (for HTTP):
```bash
gunicorn ChatApplication.wsgi:application --bind 0.0.0.0:8000
```

3. **Start with Daphne** (for WebSocket):
```bash
daphne -b 0.0.0.0 -p 8001 ChatApplication.asgi:application
```

4. **Configure Nginx** (see `nginx.conf` for reference)

## 📱 Usage

1. **Sign Up**: Navigate to `/signup/` to create a new account
2. **Login**: Use `/login/` to authenticate
3. **Select User**: Choose a user from the dropdown to start chatting
4. **Chat**: Send and receive messages in real-time
5. **View History**: Previous messages are automatically loaded when starting a chat

## 🏗️ Project Structure

```
ChatApp/
├── ChatApplication/
│   ├── chat/                    # Main chat application
│   │   ├── models.py            # Message model
│   │   ├── views.py             # HTTP views (login, signup, chat)
│   │   ├── consumers.py         # WebSocket consumer
│   │   ├── forms.py             # User registration and login forms
│   │   ├── routing.py           # WebSocket URL routing
│   │   └── templates/           # HTML templates
│   ├── ChatApplication/
│   │   ├── settings.py          # Django settings
│   │   ├── urls.py              # URL routing
│   │   └── asgi.py              # ASGI configuration
│   └── manage.py
├── requirements.txt             # Python dependencies
├── nginx.conf                   # Nginx configuration
├── start_dev.sh                 # Development startup script
├── .env.example                 # Environment variables template
└── README.md
```

## 🔐 Security Considerations

**Important**: Before deploying to production:

1. **Environment Variables**: Use `.env` file for sensitive data (see `.env.example`)
2. **Debug Mode**: Set `DEBUG = False` in production
3. **Allowed Hosts**: Configure `ALLOWED_HOSTS` with your domain
4. **HTTPS**: Use SSL/TLS certificates for secure WebSocket connections (WSS)
5. **CSRF Protection**: Already enabled, ensure it's working in production

## 🧪 API Endpoints

- `GET /` - Chat interface (requires authentication)
- `GET /login/` - Login page
- `GET /signup/` - Registration page
- `POST /login/` - Authenticate user
- `POST /signup/` - Create new user
- `GET /logout/` - Logout user
- `GET /api/messages/<username1>/<username2>/` - Get message history between two users
- `WS /ws/chat/<sender_username>/<receiver_username>/` - WebSocket connection for real-time messaging

## 🔄 WebSocket Protocol

### Connection
```
ws://localhost:8000/ws/chat/<sender_username>/<receiver_username>/
```

### Message Format (Client → Server)
```json
{
  "message": "Hello, how are you?"
}
```

### Message Format (Server → Client)
```json
{
  "message": "Hello, how are you?",
  "sender": "username1",
  "receiver": "username2"
}
```

## 🐛 Troubleshooting

### Redis Connection Error
- Ensure Redis is running: `redis-server`
- Check Redis is listening on port 6379

### Database Connection Error
- Verify PostgreSQL is running
- Check database credentials in `.env` file
- Ensure database and user exist

### WebSocket Connection Failed
- Verify Daphne is running (not just Django dev server)
- Check ASGI configuration in `asgi.py`
- Ensure Redis is running for channel layers

## 📈 Future Enhancements

- [ ] Message read receipts
- [ ] Typing indicators
- [ ] File and image sharing
- [ ] Group chat functionality
- [ ] User online/offline status
- [ ] Message search functionality
- [ ] Push notifications
- [ ] End-to-end encryption
- [ ] Unit and integration tests
- [ ] API documentation with DRF

## 📝 License

This project is open source and available under the MIT License.

## 👤 Author

**Naina**

## 🙏 Acknowledgments

- Django Channels documentation
- Django official documentation
- PostgreSQL documentation

