# Setup Instructions for VS Code

## Quick Start

### Option 1: Run Frontend Only (Node.js/Express)

1. **Install Dependencies**
   ```bash
   npm install
   ```

2. **Start Development Server**
   ```bash
   npm run dev
   ```

3. **Access the Application**
   - Open your browser and go to: `http://localhost:3000`

### Option 2: Full Stack (Frontend + Backend)

#### Frontend Setup
```bash
npm install
npm run dev
```
The frontend will be available at `http://localhost:3000`

#### Backend Setup (Python)
In a new terminal:
```bash
pip install -r requirements.txt
python app.py
```
The backend API will run on `http://127.0.0.1:5000`

## File Structure

```
project_semester3/
├── server.js              # Express.js server (Node.js entry point)
├── package.json           # Node.js dependencies
├── index.html             # Main landing page
├── portal.html            # Job/Internship portal page
├── app.py                 # Flask backend
├── database.py            # Database operations
├── recommendation.py      # AI recommendation engine
├── requirements.txt       # Python dependencies
└── .env                   # Environment variables
```

## VS Code Integration

### Auto-Start with VS Code

1. Open the folder in VS Code
2. Press `Ctrl + Shift + P` (or `Cmd + Shift + P` on Mac)
3. Type "Run Task" and select "Tasks: Run Task"
4. Choose the appropriate task to run

### Available npm Commands

- `npm run dev` - Start development server
- `npm start` - Start production server
- `npm test` - Run tests

## Troubleshooting

### Port Already in Use
If port 3000 is already in use:
```bash
# Modify .env file
PORT=3001
npm run dev
```

### Dependencies Not Installing
```bash
# Clear npm cache
npm cache clean --force

# Reinstall
npm install
```

### Python Backend Connection
Make sure Flask is running on port 5000 if you need backend integration:
```bash
python app.py
```

## Notes

- Frontend runs on `http://localhost:3000`
- Backend API runs on `http://127.0.0.1:5000`
- Both can run simultaneously in different terminals
