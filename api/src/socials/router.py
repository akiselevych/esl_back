from fastapi import APIRouter

router = APIRouter(
    prefix="/socials",
    tags=["Socials"],
)

socials_fake_data = {
    "discord": "https://discord.gg/WePlay",
    "twitch": "https://www.twitch.tv/weplayesport_en",
    "youtube": "https://www.youtube.com/channel/UCGVIeADMjqejmpvHGmfENvw",
}


@router.get("")
async def socials():
    return socials_fake_data
