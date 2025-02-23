event_by_genre_by_location_query = """
SELECT
    e.id AS event_id,
    e.start_date,
    e.event_type,
    e.start_time,
    e.average_ticket_price,
    e.fans_interested,
    e.fans_going,
    v.id AS venue_id,
    v.name AS venue_name,
    v.address,
    v.city,
    v.country,
    a.id AS artist_id,
    a.name AS artist_name,
    g.name AS genre
FROM events e
JOIN venues v ON e.venue_id = v.id
JOIN performances p ON e.id = p.event_id
JOIN artists a ON p.artist_id = a.id
JOIN performance_genres pg ON p.id = pg.performance_id
JOIN genres g ON pg.genre_id = g.id
WHERE ST_DWithin(v.location, ST_SetSRID(ST_MakePoint(%s, %s), 4326)::geography, 10000)
AND g.name = %s
ORDER BY e.start_date ASC;
"""

test_query = """
SELECT id, name, address, city, country, location FROM venues WHERE ST_DWithin(location, ST_SetSRID(ST_MakePoint(11.1197342, 49.429609), 4326)::geography, 10000);
"""
