import csv


def read_raw_data(file_path):
    csv_data = None
    print(file_path)
    with open(file_path, "r", encoding="utf-8") as file:
        csv_data = file.read()
    return csv_data


def insert_data(connection, csv_text, logger):
    logger.info("Starting data insertion")
    with connection.cursor() as cur:
        reader = csv.DictReader(csv_text.splitlines())
        for row in reader:
            # Extract and clean fields from CSV
            performance_id = row["performance_id"].strip()
            artist_id = row["artist_id"].strip()
            artist_name = row["Artist Name"].strip()
            event_id = row["Event ID on Songkick "].strip()
            event_start_date = row["Event Start Date"].strip()
            event_type = row["Event Type"].strip()
            venue_id = row["Venue ID on Songkick"].strip()
            venue_name = row["Venue Name"].strip()
            venue_address = row["Venue address "].strip()
            venue_zip = row["Venue ZIP Code"].strip()
            try:

                venue_lat = float(row["Venue Latitude"].strip())
            except ValueError:
                logger.error(
                    f"Failed to parse latitude for venue {venue_id}, artist: {artist_id}, event: {event_id}"
                )
                continue
            venue_long = float(row["Venue Longitude"].strip())
            city = row["City"].strip()
            country = row["Country"].strip()
            avg_ticket_price = row["Average Ticket Price"].strip() or None
            if avg_ticket_price:
                avg_ticket_price = float(avg_ticket_price)
            genres = row["Genres"].strip()
            fans_interested = row["Fans Marked ‘Interested’"].strip() or None
            if fans_interested:
                fans_interested = int(fans_interested)
            fans_going = row["Fans Marked ‘Going’"].strip() or None
            if fans_going:
                fans_going = int(fans_going)
            event_start_time = row["Event Start time"].strip() or None

            logger.debug(f"Inserting artist {artist_id}: {artist_name}")
            cur.execute(
                """
                INSERT INTO artists (id, name)
                VALUES (%s, %s)
                ON CONFLICT (id) DO NOTHING;
            """,
                (artist_id, artist_name),
            )

            logger.debug(f"Inserting venue {venue_id}: {venue_name}")
            cur.execute(
                """
                INSERT INTO venues (id, name, address, zip, location, city, country)
                VALUES (%s, %s, %s, %s, ST_SetSRID(ST_MakePoint(%s, %s), 4326), %s, %s)
                ON CONFLICT (id) DO NOTHING;
            """,
                (
                    venue_id,
                    venue_name,
                    venue_address,
                    venue_zip,
                    venue_long,
                    venue_lat,
                    city,
                    country,
                ),
            )

            logger.debug(f"Inserting event {event_id}")
            cur.execute(
                """
                INSERT INTO events (id, start_date, event_type, start_time, average_ticket_price, fans_interested, fans_going, venue_id)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING;
            """,
                (
                    event_id,
                    event_start_date,
                    event_type,
                    event_start_time,
                    avg_ticket_price,
                    fans_interested,
                    fans_going,
                    venue_id,
                ),
            )

            logger.debug(f"Inserting performance {performance_id}")
            cur.execute(
                """
                INSERT INTO performances (id, event_id, artist_id)
                VALUES (%s, %s, %s)
                ON CONFLICT (id) DO NOTHING;
            """,
                (performance_id, event_id, artist_id),
            )

            if genres:
                genre_list = [
                    g.strip() for g in genres.replace('"', "").split(",") if g.strip()
                ]
                for genre in genre_list:
                    logger.debug(f"Inserting genre: {genre}")
                    cur.execute(
                        """
                        INSERT INTO genres (name)
                        VALUES (%s)
                        ON CONFLICT (name) DO NOTHING;
                    """,
                        (genre,),
                    )
                    cur.execute("SELECT id FROM genres WHERE name = %s;", (genre,))
                    result = cur.fetchone()
                    if result:
                        genre_id = result[0]
                        cur.execute(
                            """
                            INSERT INTO performance_genres (performance_id, genre_id)
                            VALUES (%s, %s)
                            ON CONFLICT DO NOTHING;
                        """,
                            (performance_id, genre_id),
                        )
                    else:
                        logger.error(f"Failed to retrieve genre id for {genre}")
            connection.commit()
        logger.info("Data insertion complete")
