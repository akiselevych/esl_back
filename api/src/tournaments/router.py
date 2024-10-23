from fastapi import APIRouter


router = APIRouter(
    prefix="/tournaments",
    tags=["Tournaments"],
)


tournaments_fake_data = {
    "dota-2": [
        {
            "id": 1,
            "game": "dota-2",
            "cover_image": "https://i.imgur.com/3QXVh9r.png",
            "name": "WePlay Dota 2 Premium Duel SKY #4",
            "date": "Upcoming",
            "mode": "2v2 Single elimination",
            "access": True,
            "participants": "72/128",
            "prizes": "Dota2 skins",
            "bracket_type": "Single elimination",
            "match_for_3rd_place": True,
            "time_voting": "15",
            "bracket_logic": "Follow by",
            "map_pool": [
                {"name": "de_vertigo", "image": "https://i.imgur.com/3QXVh9r.png"},
            ],
            "prime": True,
            "stand_in": "0",
            "desciption": {"prizes": ["1 place - 560 $ Steam card", "2 place - 360 $ Steam card"]},
            "participants_users": [{"image": "https://i.imgur.com/3QXVh9r.png", "name": "KulGM"}],
        },
    ],
    "cs2": [
        {
            "id": 1,
            "game": "cs2",
            "cover_image": "https://i.imgur.com/3QXVh9r.png",
            "name": "WePlay Dota 2 Premium Duel SKY #4",
            "date": "Upcoming",
            "mode": "2v2 Single elimination",
            "access": True,
            "participants": "72/128",
            "prizes": "Dota2 skins",
            "bracket_type": "Single elimination",
            "match_for_3rd_place": True,
            "time_voting": "15",
            "bracket_logic": "Follow by",
            "map_pool": [
                {"name": "de_vertigo", "image": "https://i.imgur.com/3QXVh9r.png"},
            ],
            "prime": True,
            "stand_in": "0",
            "desciption": {"prizes": ["1 place - 560 $ Steam card", "2 place - 360 $ Steam card"]},
            "participants_users": [{"image": "https://i.imgur.com/3QXVh9r.png", "name": "KulGM"}],
        },
    ],
    "dota-underlords": [
        {
            "id": 1,
            "game": "dota-underlords",
            "cover_image": "https://i.imgur.com/3QXVh9r.png",
            "name": "WePlay Dota 2 Premium Duel SKY #4",
            "date": "Upcoming",
            "mode": "2v2 Single elimination",
            "access": True,
            "participants": "72/128",
            "prizes": "Dota2 skins",
            "bracket_type": "Single elimination",
            "match_for_3rd_place": True,
            "time_voting": "15",
            "bracket_logic": "Follow by",
            "map_pool": [
                {"name": "de_vertigo", "image": "https://i.imgur.com/3QXVh9r.png"},
            ],
            "prime": True,
            "stand_in": "0",
            "desciption": {"prizes": ["1 place - 560 $ Steam card", "2 place - 360 $ Steam card"]},
            "participants_users": [{"image": "https://i.imgur.com/3QXVh9r.png", "name": "KulGM"}],
        },
    ],
}


@router.get("/top/{game}")
async def game_top_tournaments(game: str):
    tournaments = tournaments_fake_data[game][:3]
    new_tournaments_lst = []
    for tournament in tournaments:
        new_tournaments_lst.append(
            {
                "id": tournament["id"],
                "cover_image": tournament["cover_image"],
                "name": tournament["name"],
                "prizes": tournament["prizes"],
            }
        )

    return new_tournaments_lst


@router.get("/{game}")
async def game_tournaments(game: str):
    return tournaments_fake_data[game]


@router.get("/{game}/{id}")
async def game_tournament(game: str, id: int):
    for data in tournaments_fake_data[game]:
        if data["id"] == id:
            return data
    return {"error": "Tournament not found"}
