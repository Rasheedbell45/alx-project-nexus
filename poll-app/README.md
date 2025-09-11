# 🗳️ Redux Polling App

## 🚀 Features
- Create new polls with custom questions and options
- Vote on options with real-time updates
- View results as an interactive **chart** (Recharts)
- State management with **Redux Toolkit**

# Polling API

## Auth
POST /api/auth/register
POST /api/auth/login -> returns JWT access_token

## Polls
GET /api/polls/                  # list polls
POST /api/polls/                 # create poll (auth required)
GET /api/polls/{id}              # poll detail

## Votes
POST /api/votes/ { poll_id, option_id }  # cast vote (auth required)

## Results
GET /api/results/{poll_id}       # get real-time results (cached)

## Swagger UI
Open: /api/docs/
