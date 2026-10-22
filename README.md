# SmartMatch Commerce - AI Product Recommendation System

A modern full-stack application built for the **AI Engineer Assessment**:
- **Frontend**: React (Vite), clean minimalist white design, fast search, zero jitter/animations.
- **Backend**: Python FastAPI with automatic Swagger docs (`/docs`).
- **Database**: MySQL / Amazon RDS (with automatic fallback to SQLite for local development).
- **AI Engine**: OpenAI GPT (Structured outputs for product recommendations and human explanations).

---

## 📁 Project Structure

```
web/
├── backend/
│   ├── main.py              # FastAPI endpoints & CORS configuration
│   ├── models.py            # SQLAlchemy Product schema
│   ├── database.py          # MySQL & SQLite connection setup
│   ├── config.py            # Environment configuration & OpenAI keys
│   ├── seed_data.py         # Catalog seeder (12 realistic products)
│   ├── ai_service.py        # OpenAI GPT integration & fallback logic
│   ├── requirements.txt     # Python backend dependencies
│   └── Dockerfile           # Backend containerization for AWS
├── frontend/
│   ├── src/
│   │   ├── components/      # ProductCard, SearchSection
│   │   ├── services/api.js  # API client
│   │   ├── App.jsx          # Root component
│   │   └── index.css        # Pure white, crisp typography & clean UX
│   ├── package.json
│   └── Dockerfile           # Nginx container for AWS
├── docker-compose.yml       # 1-command startup for Full-Stack + MySQL
└── README.md
```

---

## 🚀 Running Locally

### 1. Run the Backend
```bash
cd backend
pip install -r requirements.txt
python -m uvicorn main:app --reload --port 8000
```
*API will run at:* `http://localhost:8000`  
*Swagger Documentation:* `http://localhost:8000/docs`

### 2. Run the Frontend
```bash
cd frontend
npm install
npm run dev
```
*Frontend will run at:* `http://localhost:5173`

---

## ☁️ AWS Deployment Guide

### Option A: Using AWS EC2 (Docker Compose - Recommended & Quickest)
1. Launch an **Ubuntu EC2 instance** (t3.small or t2.micro) and open inbound ports **80**, **8000**, and **22** in your Security Group.
2. SSH into your instance:
   ```bash
   ssh -i your-key.pem ubuntu@your-ec2-public-ip
   ```
3. Install Docker & Docker Compose:
   ```bash
   sudo apt update && sudo apt install -y docker.io docker-compose
   ```
4. Clone or copy this project to your EC2 instance and run:
   ```bash
   sudo docker-compose up -d --build
   ```
5. Your application will be live at `http://<your-ec2-ip>` and the API at `http://<your-ec2-ip>:8000`.

### Option B: AWS RDS (MySQL) + AWS ECS / App Runner + S3/CloudFront
- **Database**: Create an AWS RDS MySQL database (`db.t3.micro`). Pass the RDS endpoint into `MYSQL_HOST`, `MYSQL_USER`, `MYSQL_PASSWORD`, and `MYSQL_DB`.
- **Backend**: Deploy the backend container to **AWS App Runner** or **AWS Elastic Beanstalk**.
- **Frontend**: Build the static frontend (`npm run build`) and upload the `dist/` directory to an **Amazon S3** bucket configured with **CloudFront** (or Vercel).
