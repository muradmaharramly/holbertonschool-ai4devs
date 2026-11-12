# System Architecture - EcoRide

This document outlines the high-level system architecture, component breakdown, communication protocols, and data flow for the **EcoRide** MVP platform.

---

## 1. Architectural Style & Overview

EcoRide adopts a modern, modular **3-Tier Client-Server Architecture** designed for high developer velocity, clear separation of concerns, and low operational overhead during the lean startup MVP phase.

- **Presentation Tier**: Single-Page Application (SPA) built with React / Next.js and Tailwind CSS, delivering responsive user experiences across mobile and desktop browsers.
- **Application Tier**: Stateless RESTful API backend (FastAPI / Express.js) enforcing business rules, request validation, authentication, and transactional seat allocations.
- **Data Tier**: Relational Database Management System (PostgreSQL / SQLite) ensuring ACID compliance, relational integrity, and foreign key cascading.

---

## 2. High-Level System Diagram

```mermaid
graph TD
    subgraph ClientLayer ["Presentation Layer (Client)"]
        UI_Web["Web Application\n(React / Vite / Tailwind CSS)"]
        State_Auth["Auth & Session Store\n(JWT in LocalStorage/HttpOnly Cookie)"]
    end

    subgraph APILayer ["Application Layer (Backend REST API)"]
        Router["API Gateway / Routers\n(FastAPI / Express)"]
        AuthService["Auth & Security Service\n(Bcrypt / JWT Provider)"]
        RideService["Ride Management Service\n(Publish, Search, Distance Calc)"]
        BookingService["Booking Engine\n(Atomic Seat Reservation)"]
        EcoService["Impact Calculator\n(CO2 & Distance Analytics)"]
    end

    subgraph DataLayer ["Persistence Layer (Database)"]
        DB[(Relational DB\nPostgreSQL / SQLite)]
        T_Users[("Users Table")]
        T_Rides[("Rides Table")]
        T_Bookings[("Bookings Table")]
    end

    subgraph ExternalServices ["External / Supporting Services"]
        Geocoding["Mapping & Geocoding Provider\n(OpenStreetMap / Nominatim)"]
    end

    %% Client to API
    UI_Web -->|HTTPS / JSON REST API| Router
    State_Auth -.->|Bearer Token| Router

    %% Routing to Services
    Router --> AuthService
    Router --> RideService
    Router --> BookingService
    Router --> EcoService

    %% Services to Data
    AuthService --> T_Users
    RideService --> T_Rides
    BookingService --> T_Bookings
    BookingService --> T_Rides
    EcoService --> T_Rides

    %% Services to External
    RideService -.->|Distance Estimation| Geocoding
```

---

## 3. Subsystem Breakdown & Responsibilities

### 3.1 Presentation Layer (Frontend)
- **User Interface Components**: Atomic component structure (Buttons, Cards, Inputs, Modals, Navbar, Alert banners).
- **Views / Pages**:
  - `Landing / Search`: Route search bar, hero section, and platform impact counter.
  - `Ride Listing & Details`: Interactive search results and detailed itinerary view.
  - `Ride Publishing`: Multi-step form for drivers to list upcoming trips with automatic cost-share recommendations.
  - `Dashboard`: Consolidated control center for managing active bookings and published trips.
  - `Authentication`: Login, registration, and session recovery views.
- **Client State & API Client**: Centralized Axios/Fetch HTTP client configured with request interceptors for JWT injection and automated error toasts.

### 3.2 Application Layer (Backend API)
- **Authentication & Authorization**:
  - Role-based access control protecting administrative, driver, and passenger endpoints.
  - Cryptographic password hashing (`bcrypt`) and stateless JWT token issuance with expiry.
- **Ride Management Engine**:
  - Geospatial and waypoint-based string matching for route search queries.
  - Automated distance calculation and statutory carpool cost-share ceiling enforcement.
- **Booking & Concurrency Engine**:
  - Thread-safe, atomic database transactions wrapped in isolation blocks to eliminate race conditions and overbooking.
- **Eco-Impact Analytics Service**:
  - Dynamic CO₂ mitigation algorithm calculating net environmental savings ($0.12\text{ kg CO}_2/\text{km}$ per passenger offset).

### 3.3 Persistence Layer (Database)
- **Schema Management**: Automated database migrations with version control (Alembic / Prisma).
- **Integrity Constraints**: Foreign key relationships with cascade protection, unique constraints on user emails, and check constraints (`available_seats >= 0`).

---

## 4. End-to-End Data Flow: Ride Search & Booking

The sequence below illustrates the end-to-end communication lifecycle for a passenger discovering and reserving a seat:

```mermaid
sequenceDiagram
    autonumber
    actor Passenger
    participant Frontend as React Web App
    participant Backend as REST API Backend
    participant Database as Relational DB

    Passenger->>Frontend: Enter Origin, Destination, & Date
    Frontend->>Backend: GET /api/rides?origin=...&destination=...&date=...
    Backend->>Database: SELECT * FROM rides WHERE status='SCHEDULED' AND available_seats > 0
    Database-->>Backend: Return matching ride records
    Backend-->>Frontend: 200 OK (JSON array of rides)
    Frontend-->>Passenger: Render available ride cards

    Passenger->>Frontend: Click 'Book Seat' (Select seat count)
    Frontend->>Backend: POST /api/bookings { ride_id, seats: 1 } (Auth: Bearer JWT)
    
    rect rgb(240, 248, 255)
        note over Backend,Database: Atomic Transaction Block
        Backend->>Database: SELECT available_seats FROM rides WHERE id = :ride_id FOR UPDATE
        alt Seats Available
            Backend->>Database: INSERT INTO bookings (ride_id, passenger_id, seats, status)
            Backend->>Database: UPDATE rides SET available_seats = available_seats - 1 WHERE id = :ride_id
            Backend->>Database: COMMIT
            Backend-->>Frontend: 201 Created { booking_id, status: 'CONFIRMED' }
            Frontend-->>Passenger: Display Booking Confirmation & Itinerary
        else Seats Exhausted
            Backend->>Database: ROLLBACK
            Backend-->>Frontend: 409 Conflict { error: 'No seats available' }
            Frontend-->>Passenger: Show error message: 'Seats no longer available'
        end
    end
```

---

## 5. Security & Reliability Architecture

1. **Authentication & Session Security**:
   - Short-lived JWTs (1 hour expiration) combined with refresh tokens.
   - Passwords salted and hashed with `bcrypt` (work factor 12).
2. **Input Validation & Sanitization**:
   - Strong schema validation on all incoming payload bodies (Pydantic / Zod) to prevent injection and payload corruption.
3. **CORS & Rate Limiting**:
   - Strict CORS policy restricting requests to trusted origin domains.
   - Endpoint rate limiting (e.g., 60 requests/minute per IP) on auth and search routes to prevent abuse.
