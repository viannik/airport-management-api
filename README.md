# Airport Management API

A comprehensive Django REST API for managing airport operations, flights, bookings, and crew assignments. This API provides a complete solution for airport management systems with JWT authentication, admin panel, and extensive filtering capabilities.

## Features

- **JWT authenticated** - Secure authentication using JSON Web Tokens
- **Admin panel** - Full Django admin interface at `/admin/`
- **API Documentation** (not realized) - Interactive API documentation (when configured)
- **Airport Management** - Create and manage airports with location details
- **Airplane Management** - Manage airplane types and individual aircraft with seating configurations
- **Flight Operations** - Create flight routes and schedule flights with crew assignments
- **Crew Management** - Manage flight crew members and their assignments
- **Booking System** - Handle customer orders and ticket reservations
- **Seat Management** - Track seat availability and reservations
- **Filtering & Search** (not realized) - Advanced filtering for flights and other resources
- **PostgreSQL Database** - Robust database backend with Docker support
- **Rate Limiting** - API throttling for security and performance

## Technology Stack

- **Backend**: Django 5.2.6 + Django REST Framework
- **Database**: PostgreSQL with psycopg driver
- **Authentication**: JWT (djangorestframework-simplejwt)
- **Containerization**: Docker & Docker Compose
- **Environment Management**: python-dotenv

## Quick Start

### Prerequisites

- Python 3.11+
- PostgreSQL 13+
- Docker & Docker Compose (optional)

### Docker Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/viannik/airport-management-api
   cd airport-management-api
   ```

2. **Create environment file**
   ```bash
   cp .env.sample .env
   ```

3. **Configure environment variables in `.env`**
   ```env
    # database
    POSTGRES_DB=<db_name>
    POSTGRES_DB_PORT=<db_port>
    POSTGRES_USER=<db_user>
    POSTGRES_PASSWORD=<db_password>
    POSTGRES_HOST=<db_host>
    PGDATA=<pg_data_path>
    # django settings
    SECRET_KEY=<secret_key>
   ```

4. **Start the application**
   ```bash
   docker-compose up --build
   ```

5. **Load sample data (optional)**
   ```bash
   docker-compose exec airport python manage.py loaddata fixtures/sample_data.json
   ```

6. **Create superuser**
   ```bash
   docker-compose exec airport python manage.py createsuperuser
   ```

The API will be available at `http://localhost:8001`

## API Endpoints

### Authentication Endpoints

Based on the JWT configuration, the following authentication endpoints should be available:

- `POST /api/user/register/` - Create new user account
- `POST /api/user/token/` - Login and obtain JWT tokens
- `POST /api/user/token/refresh/` - Refresh JWT access token
- `POST /api/user/token/verify/` - Verify JWT token validity
- `GET /api/user/me/` - Get current user profile
- `PUT /api/user/me/` - Update current user profile

### Core API Endpoints

All endpoints are prefixed with `/api/apps/`

- **Airports**: `/api/apps/airports/`
  - List all airports
  - Create new airports
  - Retrieve, update, delete specific airports

- **Airplane Types**: `/api/apps/airplane-types/`
  - Manage different aircraft models

- **Airplanes**: `/api/apps/airplanes/`
  - Manage individual aircraft with seating configurations
  - Track airplane capacity and specifications

- **Routes**: `/api/apps/routes/`
  - Define flight routes between airports
  - Manage route distances and connections

- **Flights**: `/api/apps/flights/`
  - Schedule flights on routes
  - Assign aircraft and crew
  - Track seat availability
  - Filter flights by various criteria

- **Crew**: `/api/apps/crews/`
  - Manage flight crew members
  - Assign crew to flights

- **Orders**: `/api/apps/orders/`
  - Customer booking orders
  - User-specific order management
  - Admin can view all orders

- **Tickets**: `/api/apps/tickets/`
  - Individual seat reservations
  - Linked to orders and flights
  - Seat validation and management

### Admin Panel

Access the Django admin interface at `/admin/` to:
- Manage all data models through a web interface
- View and edit airports, flights, bookings, and crew
- Perform bulk operations
- Generate reports

## Authentication & Permissions

The API uses JWT (JSON Web Tokens) for authentication with the following configuration:

- **Access Token Lifetime**: 60 minutes
- **Refresh Token Lifetime**: 7 days
- **Token Rotation**: Enabled for enhanced security

### Permission Levels

- **Anonymous Users**: Limited read access (10 requests/day)
- **Authenticated Users**: Read access to most resources (30 requests/day)
- **Staff/Admin Users**: Full CRUD access to all resources
- **Order Management**: Users can only see their own orders; admins see all

## API Features

### Filtering & Search (not realized)

The API supports advanced filtering on various endpoints:

- **Flights**: Filter by route, departure time, airplane type, availability
- **Orders**: Filter by user, date range, status
- **Airports**: Search by name or city
- **Crew**: Filter by availability and assignments

### Data Validation

- **Flight Validation**: Ensures arrival time is after departure time
- **Route Validation**: Prevents routes with same source and destination
- **Seat Validation**: Validates seat numbers against airplane capacity
- **Unique Constraints**: Prevents duplicate bookings and conflicts

### Performance Optimizations

- **Database Optimization**: (not realized) Uses select_related and prefetch_related for efficient queries 
- **Pagination**: All list endpoints are paginated (10 items per page)
- **Caching**: Optimized queries for seat availability calculations

## Sample Data

The project includes sample data with:
- 5 major international airports
- Multiple airplane types (Boeing 737, Airbus A320, etc.)
- Sample flights and routes
- Crew members and assignments

Load sample data with:
```bash
python manage.py loaddata fixtures/sample_data.json
```

## Development

### Running Tests

```bash
python manage.py test
```

### Code Structure

```
airport-management-api/
├── apps/
│   ├── airports/          # Airport management
│   ├── airplanes/         # Aircraft and types
│   ├── crews/            # Flight crew management
│   ├── flights/          # Flights and routes
│   ├── orders/           # Customer orders
│   ├── tickets/          # Seat reservations
│   └── permissions.py    # Custom permissions
├── config/               # Django settings
├── fixtures/             # Sample data
└── requirements.txt      # Dependencies
```