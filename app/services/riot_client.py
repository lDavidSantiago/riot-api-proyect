import httpx
from app.core.config import RIOT_API_KEY
from app.core.enums import MatchType

HEADERS = {"X-Riot-Token": RIOT_API_KEY}

ACCOUNT_URL = "https://americas.api.riotgames.com/riot/account/v1"
MATCHES_URL = "https://americas.api.riotgames.com/lol/match/v5/matches/by-puuid"
#/ids?type=ranked&start=0&count=20&api_key=RGAPI-6600f9b8-f8b2-4297-b978-af7bc53f22c5

async def get_account_by_riot_id(name: str, tag: str):
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{ACCOUNT_URL}/accounts/by-riot-id/{name}/{tag}",
            headers=HEADERS
        )
        r.raise_for_status()
        return r.json()
    
def normalize_count(count: int) -> int:
    if count < 1:
        return 1
    if count > 50:
        return 50
    return count

async def get_matches_by_riot_puuid(puuid:str,max_matches: int = 20,match_type: MatchType = MatchType.RANKED):
    max_matches = normalize_count(max_matches)
    async with httpx.AsyncClient() as client:
        r = await client.get(
            f"{MATCHES_URL}/{puuid}/ids?type={match_type.value}&start=0&count={max_matches}",
            headers=HEADERS
        )
        r.raise_for_status()
        return r.json()
        