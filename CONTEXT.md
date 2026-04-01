# Backend Security Context

## Project Overview
This project implements a backend system with authentication, RBAC, and audit logging.

## My Responsibility
- Backend security implementation
- JWT authentication
- Role-based access control (RBAC)
- Resource ownership validation
- Audit logging

## Tech Stack
- FastAPI
- JWT
- bcrypt
# AI_CONTEXT.md

## 1. Project Overview

This project is a **MarketStall Inventory Management System** that supports:
- Inventory tracking and updates
- Stock transfer requests and approvals
- Promotions and notifications
- Customer–vendor messaging
- Multi-role access (Customer, Stall Owner, Manager, Admin)

The system follows a **frontend–backend architecture**:
- Frontend communicates with backend via REST APIs (HTTPS)
- Backend handles all business logic, validation, and security
- Database is accessed only by backend services

---

## 2. My Role (Backend Security Developer)

I am responsible for implementing **backend security**, including:

### Core Responsibilities
- JWT-based authentication
- Role-Based Access Control (RBAC)
- Resource ownership validation
- API protection (secured endpoints)
- Audit logging for critical actions
- Input validation and secure error handling

### Security Scope
I do NOT implement business logic (inventory, transfer, etc.), but:
- I enforce **who can access what**
- I integrate security into all API endpoints
- I ensure system protection against unauthorized access

---

## 3. System Security Requirements (Refined)

### Authentication
- Email + password login
- Passwords hashed using bcrypt
- JWT issued upon successful login
- Token contains: user_id, role, stall_id

### Authorization
- RBAC model:
  - Customer
  - Stall Owner
  - Manager
  - Admin
- Users can only access resources they own (ownership validation)

### Secure Communication
- HTTPS enforced for all client–server communication
- No direct database access from client

### Data Protection
- No plaintext passwords
- Sensitive data excluded from logs and API responses

### Session Management
- JWT tokens with expiration (no inactivity tracking)

### Audit Logging (Simplified)
Logs must include:
- Login success / failure
- Inventory updates
- Transfer approvals / rejections
- Authorization failures

---

## 4. Simplifications Applied (Important)

To ensure feasibility, the following were removed or reduced:

### Removed
- Encrypted MySQL database (infrastructure-level)
- WebSocket secure chat (future enhancement)
- 15-minute inactivity logout
- Full compliance (OWASP / PDPA certification)
- Monitoring systems (Prometheus / Grafana)
- Automated recovery SLA (e.g., RTO ≤ 30 min)

### Reduced
- Fine-grained access control → simplified to RBAC + ownership
- Audit logging → only key security events (no chat logging, no 180-day requirement)

---

## 5. Backend Architecture (Security Layer)

### Core Structure

app/
  core/
  schemas/
  services/
  dependencies/
  routers/
  models/

---

## 6. File Structure (Security Module Only)

app/
├── core/
│   ├── security.py
│   ├── exceptions.py
│   └── constants.py
│
├── schemas/
│   ├── auth.py
│   └── audit_log.py
│
├── services/
│   ├── auth_service.py
│   ├── permission_service.py
│   └── audit_service.py
│
├── dependencies/
│   ├── auth.py
│   └── permissions.py
│
├── routers/
│   └── auth.py
│
└── models/
    └── audit_log.py

---

## 7. Key Components

### 7.1 Authentication
- hash_password()
- verify_password()
- create_access_token()
- decode_access_token()

### 7.2 User Context
- get_current_user()

### 7.3 Authorization
- require_roles()
- enforce_role()
- enforce_stall_ownership()

### 7.4 Audit Logging
- log_login_success()
- log_login_failed()
- log_permission_denied()
- log_inventory_update()
- log_transfer_action()

---

## 8. Security Rules (Critical)

- All protected APIs must require authentication
- All write operations must validate user role
- All resource access must validate ownership
- No sensitive data returned in responses
- All critical actions must be logged

---

## 9. Integration with API Team

### Required Alignment

1. Authentication
- Use: Authorization: Bearer <token>

2. Permission Matrix
Each API must define required roles

Example:
- GET /products → all roles
- POST /inventory → stall_owner
- POST /transfer → stall_owner
- POST /approve → manager/admin

3. Dependency Usage
APIs must use:
- get_current_user
- require_roles

---

## 10. Integration with Database Team

### Required Fields (User)
- id
- email
- password_hash
- role
- stall_id

### Required Fields (Ownership)
- inventory.stall_id
- transfer.from_stall_id
- message.sender_id

### Audit Log Table
- user_id
- action
- target_type
- target_id
- status
- message
- created_at

---

## 11. Development Workflow (Security Module)

1. Implement core utilities (JWT + hashing)
2. Implement authentication service
3. Implement current user dependency
4. Implement RBAC
5. Implement ownership validation
6. Integrate with API endpoints
7. Add audit logging
8. Perform security testing

---

## 12. Security Test Cases

- Access protected API without token → 401
- Access with invalid token → 401
- Access with insufficient role → 403
- Access another user’s resource → 403
- Token expired → 401
- Invalid input → 422

---

## 13. Development Priority

### Phase 1 (Foundation)
- security.py
- auth_service.py
- get_current_user()

### Phase 2 (Access Control)
- permission_service.py
- require_roles()

### Phase 3 (Integration)
- connect to inventory / transfer APIs

### Phase 4 (Logging)
- audit_service.py

---

## 14. Coding Guidelines for AI Agents

When generating code:

DO:
- Use JWT authentication
- Enforce RBAC
- Validate ownership
- Use dependency injection
- Keep logic modular

DO NOT:
- Skip permission checks
- Return sensitive data
- Implement unnecessary complexity
- Add infrastructure-level features

---

## 15. Summary

This backend security module ensures:
- Controlled access to all system features
- Protection against unauthorized operations
- Clear traceability of critical actions
- Maintainable and scalable security design

The implementation prioritizes **practicality, correctness, and integration readiness** over unnecessary complexity.
