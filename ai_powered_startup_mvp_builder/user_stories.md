# User Stories - EcoRide

This document defines the actionable user requirements and acceptance criteria for the **EcoRide** MVP, translating the core concept defined in [`mvp_concept.md`](./mvp_concept.md) into engineering specifications.

---

## User Story 1
As a new commuter, I want to create an account with my email and password so that I can securely access the platform and manage my rides.

**Acceptance Criteria**:
- User provides a valid email address, password (minimum 8 characters), and full name.
- System validates email uniqueness and rejects already registered emails.
- Password is encrypted using industry-standard hashing (e.g., bcrypt / Argon2) before persistence.
- Upon successful registration, the user receives an active session token (JWT) and is redirected to the dashboard.

**Priority**: MVP

---

## User Story 2
As a registered driver, I want to publish a scheduled commute ride so that nearby passengers can view and book available seats in my vehicle.

**Acceptance Criteria**:
- Driver specifies origin address, destination address, departure date and time, total available passenger seats (1 to 4), and cost contribution per seat.
- System validates that the departure time is scheduled in the future.
- System prevents a driver from publishing overlapping rides for the same vehicle and departure window.
- Published ride is immediately indexed with status `SCHEDULED` and visible in public searches.

**Priority**: MVP

---

## User Story 3
As a passenger, I want to search for upcoming rides by departure city, destination, and travel date so that I can find a commute that matches my daily schedule.

**Acceptance Criteria**:
- Search form accepts origin, destination, and date parameters.
- Search results display matching rides with driver name, departure time, available seat count, and price per seat.
- Only rides with status `SCHEDULED` and `available_seats > 0` are returned.
- If no direct matches exist, the system informs the user and displays alternative rides on the same day.

**Priority**: MVP

---

## User Story 4
As a passenger, I want to view detailed information about a selected ride so that I can evaluate the route, pricing, and driver before booking.

**Acceptance Criteria**:
- Ride detail page displays full origin and destination coordinates/addresses, departure timestamp, remaining seats, cost per seat, and driver profile summary.
- The interface displays the estimated trip distance and calculated CO₂ emission savings for the shared ride.
- Booking action is disabled if the user is the driver of that ride or if no seats remain available.

**Priority**: MVP

---

## User Story 5
As a passenger, I want to book one or more seats on a scheduled ride so that my commute seat is reserved.

**Acceptance Criteria**:
- Passenger selects the desired seat count (up to available capacity) and submits the reservation request.
- System executes an atomic database transaction: creates a booking record with status `CONFIRMED` and decrements `available_seats` on the ride.
- If concurrent requests attempt to overbook the vehicle, the system cleanly rejects the excess request and preserves data consistency.
- Passenger and driver receive immediate in-app booking confirmation with reservation details.

**Priority**: MVP

---

## User Story 6
As a passenger, I want to cancel my confirmed booking so that the driver is notified and my seat is released back to other commuters.

**Acceptance Criteria**:
- Passenger can select a confirmed booking from their dashboard and initiate cancellation.
- System updates booking status to `CANCELLED` and atomically increments the ride's `available_seats`.
- Cancellation is permitted only prior to the scheduled departure time.
- The cancelled booking is logged in the user's booking history for auditing.

**Priority**: MVP

---

## User Story 7
As a driver, I want to calculate a fair, suggested cost-share contribution automatically based on trip distance so that I do not overcharge passengers or violate carpooling cost-sharing regulations.

**Acceptance Criteria**:
- System computes estimated driving distance between origin and destination waypoints.
- System applies a fixed per-kilometer fuel and vehicle wear baseline formula to suggest a maximum per-seat rate.
- Driver can accept the suggested rate or adjust it downward, but cannot exceed the non-profit statutory reimbursement cap.

**Priority**: MVP

---

## User Story 8
As a driver, I want to cancel a scheduled ride if an emergency arises so that booked passengers are immediately alerted and their bookings are released.

**Acceptance Criteria**:
- Driver initiates trip cancellation with an optional reason note from the ride management dashboard.
- System updates the ride status to `CANCELLED` and marks all associated bookings as `CANCELLED`.
- Cancelled trips are immediately removed from search discovery results.
- Booked passengers see an alert status on their personal dashboard indicating the ride was cancelled by the driver.

**Priority**: MVP

---

## User Story 9
As an eco-conscious commuter, I want to track my accumulated carbon footprint savings so that I can see the environmental impact of my shared rides.

**Acceptance Criteria**:
- System calculates CO₂ emissions saved per completed ride using standard baseline vehicle emission factors ($0.12\text{ kg CO}_2/\text{km}$ per passenger).
- User dashboard displays cumulative metrics: total shared kilometers traveled and total kilograms of CO₂ avoided.
- Metrics update automatically when a completed ride status transition occurs.

**Priority**: High

---

## User Story 10
As an authenticated user, I want a unified dashboard showing my upcoming and past trips as both a driver and a passenger so that I can manage my daily transit in one place.

**Acceptance Criteria**:
- Dashboard splits activity into "Upcoming Trips" and "Past Trips".
- Trips are categorized by role: "Driving" (rides published by user) and "Riding" (bookings made by user).
- Each card shows key details: route, departure time, seat status, total cost, and quick actions (view details, cancel booking, or cancel ride).
- Past trips archive automatically once the departure time has passed.

**Priority**: MVP
