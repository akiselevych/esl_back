from fastapi import APIRouter


router = APIRouter(
    prefix="/events",
    tags=["Events"],
)

events_fake_data = {
    "dota-2": {
        "id": 1,
        "game": "dota-2",
        "name": "WePlay! Dota 2 Tug of War: Mad Moon",
        "winner_image": "https://i.imgur.com/3QXVh9r.png",
        "winner_name": "Team Nigma",
        "date": "21 Feb-Feb 23, 2020",
        "tags": ["LAN"],
        "location": "Kyiv, Ukraine",
        "prize_pool": "300,000$",
    },
    "cs2": {
        "id": 1,
        "game": "cs2",
        "name": "WePlay! Dota 2 Tug of War: Mad Moon",
        "winner_image": "https://i.imgur.com/3QXVh9r.png",
        "winner_name": "Team Nigma",
        "date": "21 Feb-Feb 23, 2020",
        "tags": ["LAN", "League"],
        "location": "Kyiv, Ukraine",
        "prize_pool": "300,000$",
    },
}


@router.get("")
async def events():
    return events_fake_data
