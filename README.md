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

All endpoints require authentication and are prefixed with `/api`:

- `GET/POST /games` - List/create games
- `GET/PUT/DELETE /games/<id>` - Get/update/delete specific game
- `GET/POST /saved-game-meta` - List/create saved game metadata
- `GET/PUT/DELETE /saved-game-meta/<id>` - Manage saved game metadata
- `GET/POST /game-hole-data` - List/create hole data
- `GET/PUT/DELETE /game-hole-data/<id>` - Manage hole data
- `GET/POST /game-players` - List/create players
- `GET/PUT/DELETE /game-players/<id>` - Manage players
- `GET/POST /player-hole-scores` - List/create scores
- `GET/PUT/DELETE /player-hole-scores/<id>` - Manage scores

## Authentication

- **Login**: `/login`
- **Register**: `/register` (development only)
- **Logout**: `/logout`
- **Admin Panel**: `/admin` (authenticated users only)

## Setup

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Set environment variables:
   ```bash
   export SECRET_KEY=your-secret-key
   export SECURITY_PASSWORD_SALT=your-salt
   export DATABASE_URL=your-database-url
   ```

3. Initialize database:
   ```bash
   flask db upgrade
   ```

4. Run the application:
   ```bash
   python app.py
   ```

## Environment Configuration

**Development**: Debug enabled, registration open, emails suppressed
**Production**: Debug disabled, registration closed, emails enabled, confirmations required

## Database

Uses SQLite by default with support for PostgreSQL via environment variables. All tables include proper foreign key relationships and constraints.