-- Enable the PostGIS extension for geospatial queries
CREATE EXTENSION IF NOT EXISTS postgis;

-- Artists table: storing artist info and language (for your query filter)
CREATE TABLE artists (
    id BIGINT PRIMARY KEY,
    name TEXT NOT NULL,
    language TEXT  -- optional: store the artist's language if available
);

-- Venues table: storing venue details with a geospatial location column
CREATE TABLE venues (
    id BIGINT PRIMARY KEY,
    name TEXT NOT NULL,
    address TEXT,
    zip TEXT,
    location GEOGRAPHY(POINT, 4326),  -- stores (longitude, latitude)
    city TEXT,
    country TEXT
);

-- Create a spatial index on the venues location for fast geospatial queries
CREATE INDEX idx_venues_location ON venues USING GIST(location);

-- Events table: storing event details and linking to a venue
CREATE TABLE events (
    id BIGINT PRIMARY KEY,  -- e.g., Event ID on Songkick
    start_date DATE NOT NULL,
    event_type TEXT,
    start_time TIME,
    average_ticket_price NUMERIC,
    fans_interested INTEGER,
    fans_going INTEGER,
    venue_id BIGINT REFERENCES venues(id)
);

-- Performances table: linking an artist with an event (for events with multiple artists)
CREATE TABLE performances (
    id BIGINT PRIMARY KEY,  -- performance_id from your CSV
    event_id BIGINT REFERENCES events(id),
    artist_id BIGINT REFERENCES artists(id)
);

-- Genres table: storing distinct genre names
CREATE TABLE genres (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL
);

-- Join table to allow a performance to have multiple genres
CREATE TABLE performance_genres (
    performance_id BIGINT REFERENCES performances(id),
    genre_id INT REFERENCES genres(id),
    PRIMARY KEY (performance_id, genre_id)
);

-- Optional: index on language in the artists table for faster filtering
CREATE INDEX idx_artists_language ON artists(language);
