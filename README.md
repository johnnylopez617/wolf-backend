# Wolf Scoring Backend

A Flask-based backend application for managing golf scoring games with wolf format gameplay.

## Features

- **Game Management**: Create and manage golf games with wolf scoring
- **Player Tracking**: Support for up to 9 players per game
- **Hole-by-Hole Data**: Track scores, money, and game state for all 18 holes
- **Authentication**: Secure user authentication with Flask-Security
- **Admin Interface**: Web-based admin panel for data management
- **REST API**: Full CRUD API for all game entities

## Models

- **Games**: Main game records with wolf settings and money tracking
- **SavedGameMeta**: Lightweight metadata for saved games
- **GameHoleData**: Per-hole data including toggles and course information
- **GamePlayers**: Player information and wolf points
- **PlayerHoleScores**: Individual scores per player per hole
- **Users/Roles**: Authentication and authorization

## API Endpoints

All API endpoints are prefixed with `/api` and require authentication using Flask-Security.

### Games API

#### GET /api/games
Retrieve all games.

**Response:**
```json
[
  {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "game_name": "New Game",
    "hole": 5,
    "last_saved": "2025-09-01T10:30:00",
    "dollars": 2.0,
    "total_dollars": 10.0,
    "is_continuing_game": true,
    "pressed_button": 0,
    "wolf": 1,
    "wolf_birdie_points": 5,
    "wolf_eagle_points": 2,
    "wolf_non_eagle_points": 3,
    "non_wolf_birdie_points": 4,
    "prox": 2,
    "created_at": "2025-09-01T09:00:00",
    "updated_at": "2025-09-01T10:30:00"
  }
]
```

#### POST /api/games
Create a new game.

**Request Body:**
```json
{
  "game_name": "Sunday Round",
  "hole": 1,
  "dollars": 5.0,
  "total_dollars": 0.0,
  "is_continuing_game": true,
  "wolf": 1
}
```

**Response:**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000"
}
```

#### GET /api/games/{game_id}
Retrieve a specific game by ID.

#### PUT /api/games/{game_id}
Update an existing game. Only include fields to update.

**Request Body:**
```json
{
  "game_name": "Updated Game Name",
  "hole": 6,
  "dollars": 3.0
}
```

#### DELETE /api/games/{game_id}
Delete a game.

**Response:**
```json
{
  "message": "Game deleted successfully"
}
```

### Game Players API

#### GET /api/game-players
Retrieve all game players.

#### POST /api/game-players
Create a new game player.

**Request Body:**
```json
{
  "game_id": "456e7890-e89b-12d3-a456-426614174000",
  "player_number": 1,
  "player_name": "John Doe",
  "is_activated": true,
  "handicap": 12
}
```

#### GET /api/game-players/{player_id}
Retrieve specific game player by ID.

#### PUT /api/game-players/{player_id}
Update an existing game player.

#### DELETE /api/game-players/{player_id}
Delete a game player.

### Game Hole Data API

#### GET /api/game-hole-data
Retrieve all game hole data.

#### POST /api/game-hole-data
Create new game hole data.

**Request Body:**
```json
{
  "game_id": "456e7890-e89b-12d3-a456-426614174000",
  "hole_number": 1,
  "hole_dollars": 2.0,
  "hole_par": 4,
  "pressed_count": false,
  "wolf_hole": 1
}
```

#### GET /api/game-hole-data/{data_id}
Retrieve specific game hole data by ID.

#### PUT /api/game-hole-data/{data_id}
Update existing game hole data.

#### DELETE /api/game-hole-data/{data_id}
Delete game hole data.

### Player Hole Scores API

#### GET /api/player-hole-scores
Retrieve all player hole scores.

#### POST /api/player-hole-scores
Create a new player hole score.

**Request Body:**
```json
{
  "game_id": "456e7890-e89b-12d3-a456-426614174000",
  "player_number": 1,
  "hole_number": 1,
  "player_score": 4,
  "net_score": 3,
  "player_money": 2.0
}
```

#### GET /api/player-hole-scores/{score_id}
Retrieve specific player hole score by ID.

#### PUT /api/player-hole-scores/{score_id}
Update an existing player hole score.

#### DELETE /api/player-hole-scores/{score_id}
Delete a player hole score.

### Saved Game Meta API

#### GET /api/saved-game-meta
Retrieve all saved game metadata.

#### POST /api/saved-game-meta
Create new saved game metadata.

**Request Body:**
```json
{
  "id": "123e4567-e89b-12d3-a456-426614174000",
  "name": "Mid-Round Save",
  "saved_at": "2025-09-01T15:30:00",
  "hole": 9
}
```

#### GET /api/saved-game-meta/{meta_id}
Retrieve specific saved game metadata by ID.

#### PUT /api/saved-game-meta/{meta_id}
Update saved game metadata.

#### DELETE /api/saved-game-meta/{meta_id}
Delete saved game metadata.

### Response Codes
- **200 OK** - Successful GET, PUT operations
- **201 Created** - Successful POST operations
- **404 Not Found** - Resource not found
- **401 Unauthorized** - Authentication required

## Authentication

- **Login**: `/login`
- **Register**: `/register` (development only)
- **Logout**: `/logout`
- **Admin Panel**: `/admin` (authenticated users only)

## Setup

### Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set environment variables:
   ```bash
   export SECRET_KEY=your-secret-key
   export SECURITY_PASSWORD_SALT=your-salt
   export DATABASE_URL=your-database-url
   export FLASK_ENV=development
   ```

3. Initialize database:
   ```bash
   flask db upgrade
   ```

4. Run the application:
   ```bash
   python app.py
   ```

### Heroku Deployment

1. Install Heroku CLI and login:
   ```bash
   heroku login
   ```

2. Create a new Heroku app:
   ```bash
   heroku create your-app-name
   ```

3. Add PostgreSQL addon:
   ```bash
   heroku addons:create heroku-postgresql:mini
   ```

4. Set environment variables:
   ```bash
   heroku config:set SECRET_KEY=your-production-secret-key
   heroku config:set SECURITY_PASSWORD_SALT=your-production-salt
   heroku config:set FLASK_ENV=production
   ```

5. Deploy to Heroku:
   ```bash
   git add .
   git commit -m "Prepare for Heroku deployment"
   git push heroku main
   ```

6. Initialize database:
   ```bash
   heroku run flask db upgrade
   ```

7. View your deployed app:
   ```bash
   heroku open
   ```

## Environment Configuration

**Development**: Debug enabled, registration open, emails suppressed
**Production**: Debug disabled, registration closed, emails enabled, confirmations required

## Database

Uses SQLite by default with support for PostgreSQL via environment variables. All tables include proper foreign key relationships and constraints.