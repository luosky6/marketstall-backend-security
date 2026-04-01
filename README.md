# MarketStall Backend Security Module / 市场摊位库存系统后端安全模块

## 1. Overview / 项目概览

### English
This repository contains the backend security module for the MarketStall Inventory Management System.  
It provides authentication, role-based access control (RBAC), stall ownership validation, and audit logging for business APIs such as inventory, transfer, promotions, notifications, and messaging.

### 中文
这个仓库实现的是 MarketStall Inventory Management System 的后端安全模块。  
它为库存、调拨、促销、通知、消息等业务接口提供认证、基于角色的访问控制（RBAC）、档口归属校验和审计日志能力。

## 2. Scope / 职责范围

### English
This module is responsible for:
- JWT-based authentication
- Password hashing with bcrypt
- Role checks for protected APIs
- Ownership validation for stall-scoped resources
- Audit logging for critical security events
- Input validation and safe error responses

This module does not implement full inventory or transfer business logic.

### 中文
这个模块负责：
- 基于 JWT 的身份认证
- 使用 bcrypt 的密码哈希
- 受保护接口的角色权限校验
- 档口资源的归属校验
- 关键安全事件的审计日志记录
- 输入校验和安全错误返回

这个模块不负责库存、调拨等完整业务逻辑本身。

## 3. Project Structure / 目录结构

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

## 4. Module Mapping / 模块职责映射

### [app/core/constants.py](/C:/Users/1/Desktop/backend/app/core/constants.py)
English: Defines shared role names and audit event keys used across services, routers, and tests.  
中文：定义全局共享的角色名称和审计事件标识，供服务层、路由层和测试统一复用。

### [app/core/exceptions.py](/C:/Users/1/Desktop/backend/app/core/exceptions.py)
English: Defines security-specific exception types for authentication, authorization, and ownership errors.  
中文：定义认证失败、权限不足、归属权错误等安全异常类型。

### [app/core/security.py](/C:/Users/1/Desktop/backend/app/core/security.py)
English: Implements bcrypt hashing and JWT creation/validation. This is the foundation of authentication.  
中文：实现 bcrypt 密码哈希和 JWT 的生成、校验，是认证体系的底层基础。

### [app/dependencies/auth.py](/C:/Users/1/Desktop/backend/app/dependencies/auth.py)
English: Extracts the current user from the bearer token and normalizes it into a reusable user context.  
中文：从 Bearer Token 中提取当前用户，并封装成统一的用户上下文。

### [app/dependencies/permissions.py](/C:/Users/1/Desktop/backend/app/dependencies/permissions.py)
English: Exposes dependency helpers for admin, manager/admin, stall-owner, and ownership validation use cases.  
中文：向路由层提供 admin、manager/admin、stall_owner 以及归属校验的依赖封装。

### [app/models/audit_log.py](/C:/Users/1/Desktop/backend/app/models/audit_log.py)
English: Defines the audit log entity shape before full ORM/database integration.  
中文：在接入 ORM 或数据库前，定义审计日志实体结构。

### [app/schemas/auth.py](/C:/Users/1/Desktop/backend/app/schemas/auth.py)
English: Defines request/response validation models for login and current-user responses.  
中文：定义登录请求和当前用户返回的输入输出校验模型。

### [app/schemas/audit_log.py](/C:/Users/1/Desktop/backend/app/schemas/audit_log.py)
English: Defines request/response schemas for audit log data exchange.  
中文：定义审计日志数据交互所需的请求/响应结构。

### [app/services/auth_service.py](/C:/Users/1/Desktop/backend/app/services/auth_service.py)
English: Handles user lookup, credential verification, token issuance, and user response mapping.  
中文：处理用户查询、密码校验、令牌签发以及用户响应对象转换。

### [app/services/permission_service.py](/C:/Users/1/Desktop/backend/app/services/permission_service.py)
English: Implements RBAC and stall ownership checks.  
中文：实现基于角色的权限控制和档口归属校验。

### [app/services/audit_service.py](/C:/Users/1/Desktop/backend/app/services/audit_service.py)
English: Records security-related audit events in a thread-safe in-memory store.  
中文：以线程安全的内存方式记录关键安全审计事件。

### [app/routers/auth.py](/C:/Users/1/Desktop/backend/app/routers/auth.py)
English: Exposes authentication and security demo endpoints such as login, current-user lookup, role-gated routes, and ownership checks.  
中文：暴露登录、当前用户、角色权限示例接口和资源归属校验接口。

## 5. API Contract / 接口约定

### Login / 登录
- Method: `POST /auth/login`
- Content-Type: `application/x-www-form-urlencoded`
- Fields:
  - `username`: user email / 用户邮箱
  - `password`: user password / 用户密码

Example / 示例:
```text
username=owner@example.com
password=owner123
```

Response / 返回:
```json
{
  "access_token": "<jwt>",
  "token_type": "bearer"
}
```

### Bearer Token Usage / Bearer Token 用法
All protected APIs must send:
```http
Authorization: Bearer <token>
```

所有受保护接口都必须通过上面的 `Authorization` 请求头传递 token。

## 6. Current Demo Users / 当前演示账号

- `customer@example.com / customer123`
- `owner@example.com / owner123`
- `manager@example.com / manager123`
- `admin@example.com / admin123`

## 7. Permission Rules / 权限规则

### English
- `customer`: authenticated only, no privileged access
- `stall_owner`: can access own stall resources
- `manager`: can access manager-level routes and bypass stall ownership checks by default
- `admin`: full access in this module

### 中文
- `customer`：仅具备基础认证身份，不具备特权访问能力
- `stall_owner`：只能访问自己档口的资源
- `manager`：可以访问 manager 级接口，默认可绕过档口归属限制
- `admin`：在当前模块中拥有最高权限

## 8. Audit Events / 审计事件

The module currently records the following events:
- `login_success`
- `login_failed`
- `permission_denied`
- `inventory_updated`
- `transfer_action`

当前模块会记录以上关键事件，用于安全追踪和问题定位。

## 9. Database Integration Requirements / 数据库集成要求

### User table / 用户表
Required fields:
- `id`
- `email`
- `password_hash`
- `role`
- `stall_id`

### Ownership-related fields / 归属关系字段
Required references:
- `inventory.stall_id`
- `transfer.from_stall_id`
- `message.sender_id`

### Audit log table / 审计日志表
Required fields:
- `user_id`
- `action`
- `target_type`
- `target_id`
- `status`
- `message`
- `created_at`

## 10. How API Teammates Should Use It / API 同事如何接入

### English
For each protected endpoint:
1. Add authentication with `get_current_user` or a role dependency.
2. Define the allowed roles explicitly.
3. Validate ownership for stall-scoped resources.
4. Write audit logs for critical actions.

### 中文
对每个受保护接口：
1. 使用 `get_current_user` 或角色依赖完成认证。
2. 明确声明允许访问的角色。
3. 对档口资源执行归属校验。
4. 对关键操作写入审计日志。

## 11. Local Run / 本地运行

Install dependencies / 安装依赖：
```powershell
.\.venv\Scripts\pip.exe install fastapi uvicorn python-multipart "pydantic[email]" python-jose bcrypt pytest httpx
```

Start the server / 启动服务：
```powershell
.\.venv\Scripts\python.exe -m uvicorn main:app --reload
```

Swagger UI / 接口文档：
- `http://127.0.0.1:8000/docs`

## 12. Tests / 测试

Run all tests / 运行全部测试：
```powershell
.\.venv\Scripts\python.exe -m pytest
```

Run a single file / 运行单个测试文件：
```powershell
.\.venv\Scripts\python.exe -m pytest tests\test_auth_router.py -v
```

## 13. Security Notes / 安全说明

### English
- Passwords are hashed with bcrypt and never returned in responses.
- JWT tokens include `user_id`, `role`, and `stall_id`.
- Invalid credentials return `401`.
- Invalid login input returns `422`.
- Authorization failures return `403`.

### 中文
- 密码使用 bcrypt 哈希，不会出现在返回结果中。
- JWT 中包含 `user_id`、`role`、`stall_id`。
- 无效凭证返回 `401`。
- 非法登录输入返回 `422`。
- 权限不足或归属校验失败返回 `403`。
