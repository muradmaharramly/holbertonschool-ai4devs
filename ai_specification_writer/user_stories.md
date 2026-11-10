# User Stories: CarpoolConnect

This document defines the core user stories, acceptance criteria, and delivery priorities for **CarpoolConnect**, aligned with the vision, user personas, and features established in [`product_idea.md`](./product_idea.md).

## Summary by Priority

| Priority | Count | Scope |
| :--- | :---: | :--- |
| **MVP** | 5 | Enterprise SSO, recurring ride publishing, smart route matching, ride booking, cost-sharing |
| **High** | 4 | Live GPS tracking, two-way ratings & safety SOS, priority parking perks, ESG admin dashboard |
| **Medium** | 2 | Guaranteed Ride Home fallback, exportable Scope 3 compliance reports |
| **Low** | 1 | Gamified commuter sustainability leaderboard |

---

### User Story 1
As a corporate employee, I want to authenticate using my company SSO credentials so that I only share rides with verified colleagues from my organization or approved campus partners.

**Acceptance Criteria**:
- User can sign in via corporate SAML/OIDC SSO or a verified corporate email domain.
- Unverified external email domains are blocked from joining organization-scoped ride pools.
- Authenticated user profile displays verified workplace affiliation and department badge.

**Priority**: MVP

---

### User Story 2
As a corporate passenger, I want to search for coworker drivers along my home-to-office commute corridor so that I can book a reliable, affordable ride that fits my work schedule.

**Acceptance Criteria**:
- Passenger enters pickup address, destination office campus, and desired arrival time window.
- System displays matching verified drivers within a configurable detour radius, showing departure time, available seats, and estimated cost share.
- Passenger can submit a booking request in under 2 minutes and receive instant confirmation status.

**Priority**: MVP

---

### User Story 3
As a corporate driver, I want to publish a recurring weekly commute schedule with my vehicle capacity and maximum detour limit so that I can fill empty seats without daily manual re-entry.

**Acceptance Criteria**:
- Driver can specify origin, destination campus, recurring weekdays, departure times, and available seat count.
- System automatically validates driver license and vehicle registration status before listing the schedule.
- Driver can pause, edit, or cancel individual occurrences without deleting the entire recurring template.

**Priority**: MVP

---

### User Story 4
As a corporate driver, I want to review incoming passenger requests with exact pickup detour distance and time impact so that I can accept compatible riders without disrupting my schedule.

**Acceptance Criteria**:
- Driver notification shows passenger name, workplace verification badge, pickup location, and added detour minutes/kilometers.
- Driver can accept or decline a request with one tap and an optional preset message.
- Accepting a request automatically decrements available seats and notifies the passenger.

**Priority**: MVP

---

### User Story 5
As a corporate passenger, I want ride costs to be automatically split and settled through integrated commuter benefits or digital payments so that I never have to handle cash or manual transfers.

**Acceptance Criteria**:
- System calculates transparent per-passenger cost share capped at non-commercial fuel/wear-and-tear reimbursement limits.
- Passenger can link a corporate commuter-benefit card, payroll deduction option, or digital wallet.
- Driver payout and itemized digital receipts are generated automatically upon trip completion.

**Priority**: MVP

---

### User Story 6
As a corporate passenger, I want to track my driver's live GPS location and receive automated arrival notifications so that I am ready at the pickup point on time.

**Acceptance Criteria**:
- Live map displays driver location and dynamic ETA starting 15 minutes before scheduled pickup.
- System sends push notifications when the driver is 5 minutes away and upon arrival at the pickup point.
- In-app encrypted chat allows passenger and driver to coordinate exact curb or gate pickup details.

**Priority**: High

---

### User Story 7
As a driver or passenger, I want to rate my ride partner, set commute preferences, and access an emergency SOS option so that every shared trip feels safe and comfortable.

**Acceptance Criteria**:
- Both parties can submit a 1–5 star rating and optional tags after trip completion.
- User profile supports commute preferences (conversation level, music, non-smoking, accessibility needs) used in match scoring.
- Active trip screen provides a one-tap SOS trigger that shares live GPS location with corporate security and designated emergency contacts.

**Priority**: High

---

### User Story 8
As a corporate driver, I want verified shared commutes to unlock priority campus carpool parking passes so that I have a strong practical incentive to offer rides regularly.

**Acceptance Criteria**:
- System verifies active carpool occupancy (driver plus at least one checked-in colleague) via in-app check-in or campus gate badge scan.
- Qualified trips automatically issue a digital QR/NFC priority carpool parking permit for that workday.
- Facilities system updates available carpool parking spot counts in real time.

**Priority**: High

---

### User Story 9
As a corporate mobility administrator, I want to configure commute subsidies, reimbursement caps, and campus parking rules so that the platform aligns with company HR and sustainability policies.

**Acceptance Criteria**:
- Admin portal allows setting per-kilometer reimbursement ceilings, monthly commuter ride credits, and eligible office campuses.
- Policy changes take effect for new bookings and display updated subsidy amounts to employees before confirmation.
- All configuration updates are recorded with timestamp and administrator identity in an audit log.

**Priority**: High

---

### User Story 10
As a corporate passenger, I want access to a Guaranteed Ride Home voucher if my scheduled return carpool is cancelled last minute so that I am never stranded at the office.

**Acceptance Criteria**:
- If a driver cancels within 2 hours of scheduled departure and no alternate carpool match is available within 15 minutes, the system flags the trip as eligible.
- Passenger receives an automated corporate transit or ride-hailing voucher up to the company-configured allowance.
- Admin dashboard logs voucher redemptions alongside the triggering cancellation for policy oversight.

**Priority**: Medium

---

### User Story 11
As a corporate sustainability manager, I want to view and export verified Scope 3 commute emissions and parking-relief analytics so that I can include accurate data in ESG reports.

**Acceptance Criteria**:
- Analytics dashboard displays total shared trips, average vehicle occupancy, parking spots freed, and estimated CO₂ kilograms avoided by campus and date range.
- Metrics distinguish verified completed trips from scheduled or cancelled trips.
- Manager can export filtered summary and detailed datasets in CSV and PDF formats.

**Priority**: Medium

---

### User Story 12
As a corporate employee, I want to track my personal CO₂ savings, fuel money saved, and team sustainability milestones so that I stay motivated to carpool consistently.

**Acceptance Criteria**:
- Personal impact view shows cumulative CO₂ avoided, estimated money saved, and total shared commutes over weekly, monthly, and all-time periods.
- Employees can opt into anonymized department or campus sustainability challenges and milestone badges.
- Users can disable public leaderboard visibility at any time from privacy settings.

**Priority**: Low
