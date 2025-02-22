# Backend for Frontend API

## Pre-requisites

1. To test the lambda function locally you will need to install the [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)

## Getting Started

## Request - Response Structure

### Frontend API

```sh
curl GET /generated-ads?lat={lat}&lon={lon}&genre={genre} # => MP3
```

### Ad Generator API

```sh
curl POST /ads
```

### Body
```json
{
    "relevant-events": [
        {
            "performance_id": 79508641,
            "artist_id": 746698,
            "artist_name": "I See Stars",
            "event_id_on_songkick": 41997727,
            "event_start_date": "2025-06-06",
            "event_type": "FestivalInstance",
            "venue_id_on_songkick": 66455,
            "venue_name": "Zeppelinfeld Nürnberg",
            "venue_address": "Hermann-Böhm Str.",
            "venue_zip_code": 90471,
            "venue_latitude": 49.429609,
            "venue_longitude": 11.1197342,
            "city": "Nuremberg",
            "country": "Germany",
            "average_ticket_price": 213,
            "genres": [
                "metal",
                "rock",
                "trance"
            ],
            "fans_marked_interested": 545,
            "fans_marked_going": 87,
            "event_start_time": "20:00"
        }
    ],
    "context": {
        "lat": 52.5159,
        "lon": 13.4546,
        "genre": ["metal"]
    }
}
```
