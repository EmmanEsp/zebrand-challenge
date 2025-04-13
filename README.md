# Project Setup & Usage Guide

## ✅ Requirements

Before setting up the project, make sure you have the following installed:

- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- `make` command (usually comes pre-installed on macOS/Linux, or via [Make for Windows](http://gnuwin32.sourceforge.net/packages/make.htm))

---

## 📦 How to Set Up the Project

### 1. Set Up the Database

Open your terminal and navigate to the root of the project:

```bash
cd zebrand-database
```

Inside the `zebrand-database` folder, run the following commands one by one:

- `make init`
- `make up`
- `make migration-up`

This will initialize and run the database.

✅ **Note**: An admin user is preloaded with the following credentials:

- **Email**: `string@gmail.com`
- **Password**: `stringstring`

---

### 2. Set Up the Backend Service

Go back to the root directory:
```bash
cd ..
```
Then enter the backend folder:
```bash
cd zebrand-backend
```
Run the initialization command:
```bash
make init
```
This will generate a .env file from .env.dist.

📝 **Important**:

The `update:product` feature may fail unless AWS credentials are properly configured in the `.env` file for sending emails.

If you want to avoid that failure during local development, you can comment out the following line in:

`zebrand-backend/app/product/api/v1/product_controller.py` at line 80:

```python
# background_tasks.add_task(notification_use_case.send_update_product_notification, request, product_changes)
```
Finally, start the backend service:
```python
make start
```

Now you are able to use the project, go to:

http://127.0.0.1:8000/docs

---

## 🚀 How to Use the Project

To use the project, you'll need a token. There are two ways to get one:

### 1. Admin Token

Endpoint:

```endpoint
POST /api/v1/auth/sign-in
```

Credentials:

- Email: `string@gmail.com`
- Password: `stringstring`

### 1. Guest Token

Endpoint:

```endpoint
POST /api/v1/auth/guest
```

---

Once you have a token, head to the Swagger UI and click the "**Authorize**" button at the top right. Paste your token and click **Authorize**.

You can now access endpoints based on your token type:

### ✅ Endpoints Available for Guest Token

- `GET /products`
- `GET /products/sku/{sku}`

### 🔒 Endpoints Available for Admin Token
- All endpoints
