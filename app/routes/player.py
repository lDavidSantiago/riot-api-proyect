from fastapi import APIRouter
from app.services.cache import get_or_set
from app.services.riot_client import get_account_by_riot_id
from app.services.riot_client import get_matches_by_riot_puuid
from app.core.enums import MatchType
router = APIRouter()

@router.get("/player/{name}/{tag}")
async def get_player(name: str, tag: str):
    name = name.lower()
    tag = tag.lower()
    key = f"riot:account:{name}:{tag}"
    async def fetch():
        
        return await get_account_by_riot_id(name, tag)

    return await get_or_set(key, 86400, fetch)
@router.get("/{name}/{tag}/matches")
async def get_player_matches(
    name: str,
    tag: str,
    count: int = 20,
    type: MatchType = MatchType.RANKED,
):
    name = name.lower()
    tag = tag.lower()
    # 1. Account (cache largo)
    account_cache_key = f"riot:account:{name}:{tag}"

    account = await get_or_set(
        key=account_cache_key,
        ttl=60 * 60 * 6,  # 6 horas
        fetch_fn=lambda: get_account_by_riot_id(name, tag),
    )

    puuid = account["puuid"]

    # 2. Matches (cache corto)
    matches_cache_key = f"riot:matches:{puuid}:{type.value}:{count}"

    matches = await get_or_set(
        key=matches_cache_key,
        ttl=60 * 15,  # 15 minutos
        fetch_fn=lambda: get_matches_by_riot_puuid(
            puuid=puuid,
            max_matches=count,
            match_type=type,
        ),
    )

    return {
        "name": name,
        "tag": tag,
        "type": type.value,
        "count": len(matches),
        "matches": matches,
    }
