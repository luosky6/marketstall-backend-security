# MarketStall Backend Security Module 

## 1. Overview

This repository contains the backend security module for the MarketStall Inventory Management System.  
It provides authentication, role-based access control (RBAC), stall ownership validation, and audit logging for business APIs such as inventory, transfer, promotions, notifications, and messaging.


## 2. Scope 

This module is responsible for:
- JWT-based authentication
- Password hashing with bcrypt
- Role checks for protected APIs
- Ownership validation for stall-scoped resources
- Audit logging for critical security events
- Input validation and safe error responses

This module does not implement full inventory or transfer business logic.



## 3. Project Structure 
```text
app/
  core/
    constants.py
    exceptions.py
    security.py
  dependencies/
    auth.py
    permissions.py
  models/
    audit_log.py
  routers/
    auth.py
  schemas/
    auth.py
    audit_log.py
  services/
    auth_service.py
    permission_service.py
    audit_service.py
main.py
tests/
```

## 4. Module Mapping

### [app/core/constants.py](/C:/Users/1/Desktop/backend/app/core/constants.py)
Defines shared role names and audit event keys used across services, routers, and tests.  。

### [app/core/exceptions.py](/C:/Users/1/Desktop/backend/app/core/exceptions.py)
Defines security-specific exception types for authentication, authorization, and ownership errors.  

### [app/core/security.py](/C:/Users/1/Desktop/backend/app/core/security.py)
Implements bcrypt hashing and JWT creation/validation. This is the foundation of authentication.  

### [app/dependencies/auth.py](/C:/Users/1/Desktop/backend/app/dependencies/auth.py)
Extracts the current user from the bearer token and normalizes it into a reusable user context.  

### [app/dependencies/permissions.py](/C:/Users/1/Desktop/backend/app/dependencies/permissions.py)
Exposes dependency helpers for admin, manager/admin, stall-owner, and ownership validation use cases.  

### [app/models/audit_log.py](/C:/Users/1/Desktop/backend/app/models/audit_log.py)
Defines the audit log entity shape before full ORM/database integration.  

### [app/schemas/auth.py](/C:/Users/1/Desktop/backend/app/schemas/auth.py)
Defines request/response validation models for login and current-user responses.  

### [app/schemas/audit_log.py](/C:/Users/1/Desktop/backend/app/schemas/audit_log.py)
Defines request/response schemas for audit log data exchange.  

### [app/services/auth_service.py](/C:/Users/1/Desktop/backend/app/services/auth_service.py)
Handles user lookup, credential verification, token issuance, and user response mapping.  

### [app/services/permission_service.py](/C:/Users/1/Desktop/backend/app/services/permission_service.py)
Implements RBAC and stall ownership checks.  

### [app/services/audit_service.py](/C:/Users/1/Desktop/backend/app/services/audit_service.py)
Records security-related audit events in a thread-safe in-memory store.  

### [app/routers/auth.py](/C:/Users/1/Desktop/backend/app/routers/auth.py)
Exposes authentication and security demo endpoints such as login, current-user lookup, role-gated routes, and ownership checks.  

## 5. API Contract

### Login 
- Method: `POST /auth/login`
- Content-Type: `application/x-www-form-urlencoded`
- Fields:
  - `username`: user email
  - `password`: user password 

Example
```text
username=owner@example.com
password=owner123
```

Response :
```json
{
  "access_token": "<jwt>",
  "token_type": "bearer"
}
```

### Bearer Token Usage / Bearer Token 
All protected APIs must send:
```http
Authorization: Bearer <token>
```

## 6. Current Demo Users 
- `customer@example.com / customer123`
- `owner@example.com / owner123`
- `manager@example.com / manager123`
- `admin@example.com / admin123`

## 7. Permission Rules 

- `customer`: authenticated only, no privileged access
- `stall_owner`: can access own stall resources
- `manager`: can access manager-level routes and bypass stall ownership checks by default
- `admin`: full access in this module


## 8. Audit Events

The module currently records the following events:
- `login_success`
- `login_failed`
- `permission_denied`
- `inventory_updated`
- `transfer_action`


## 9. Database Integration Requirements 

### User table
Required fields:
- `id`
- `email`
- `password_hash`
- `role`
- `stall_id`

### Ownership-related fields 
Required references:
- `inventory.stall_id`
- `transfer.from_stall_id`
- `message.sender_id`

### Audit log table 
Required fields:
- `user_id`
- `action`
- `target_type`
- `target_id`
- `status`
- `message`
- `created_at`

## 11. Local Run 

Install dependencies ：
```powershell
.\.venv\Scripts\pip.exe install fastapi uvicorn python-multipart "pydantic[email]" python-jose bcrypt pytest httpx
```

Start the server ：
```powershell
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

Swagger UI ：
- `http://127.0.0.1:8000/docs`

## 12. Tests 

Run all tests ：
```powershell
.\.venv\Scripts\python.exe -m pytest
```

Run a single file ：
```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_auth_router.py -v
```

## 13. Security Notes 

- Passwords are hashed with bcrypt and never returned in responses.
- JWT tokens include `user_id`, `role`, and `stall_id`.
- Invalid credentials return `401`.
- Invalid login input returns `422`.
- Authorization failures return `403`.

