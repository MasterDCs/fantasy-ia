"""
Cliente para LaLiga Fantasy Marca API
Usa token de sesión capturado del navegador (Google OAuth)
"""
import os
import requests
import json
import urllib3
from typing import Optional, Dict, Any, List
from dotenv import load_dotenv

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
load_dotenv()

BASE_URL = "https://api.laligafantasymarca.com/api/v3"
HEADERS_BASE = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15",
    "Origin": "https://fantasy.laliga.es",
    "Referer": "https://fantasy.laliga.es/",
    "x-app-version": "3.0.0",
}


class LaLigaFantasyClient:
    def __init__(self):
        self.token = os.getenv("FANTASY_TOKEN", "")
        self.user_id = os.getenv("FANTASY_USER_ID", "")
        self.team_id = os.getenv("FANTASY_TEAM_ID", "")
        self.league_id = os.getenv("FANTASY_LEAGUE_ID", "")
        self.session = requests.Session()
        self.session.headers.update(HEADERS_BASE)
        self.session.verify = False
        if self.token:
            self.session.headers.update({"Authorization": f"Bearer {self.token}"})

    def is_authenticated(self) -> bool:
        """Verifica si hay un token válido configurado"""
        return bool(self.token)

    def get_my_team(self) -> Optional[Dict]:
        """Obtiene los datos del equipo del usuario"""
        if not self.token:
            return None
        try:
            endpoints = [
                f"{BASE_URL}/user/{self.user_id}/team",
                f"{BASE_URL}/team/user/{self.user_id}",
                f"{BASE_URL}/user/me/team",
                f"{BASE_URL}/me/team",
            ]
            for url in endpoints:
                try:
                    if "None" in url or not self.user_id:
                        continue
                    response = self.session.get(url, timeout=15)
                    if response.status_code == 200:
                        data = response.json()
                        self.team_id = str(data.get("id") or data.get("teamId", ""))
                        print(f"✅ Equipo obtenido. Team ID: {self.team_id}")
                        return data
                except:
                    continue

            # Intentar sin user_id
            response = self.session.get(f"{BASE_URL}/me/team", timeout=15)
            if response.status_code == 200:
                return response.json()

            print(f"⚠️ No se pudo obtener equipo. Status últimos intentos.")
            return None
        except Exception as e:
            print(f"❌ Error obteniendo equipo: {e}")
            return None

    def get_my_profile(self) -> Optional[Dict]:
        """Obtiene el perfil del usuario autenticado"""
        if not self.token:
            return None
        try:
            endpoints = [
                f"{BASE_URL}/user/me",
                f"{BASE_URL}/me",
                f"{BASE_URL}/auth/me",
            ]
            for url in endpoints:
                try:
                    r = self.session.get(url, timeout=15)
                    if r.status_code == 200:
                        data = r.json()
                        self.user_id = str(data.get("id") or data.get("userId", ""))
                        print(f"✅ Perfil obtenido. User ID: {self.user_id}")
                        return data
                except:
                    continue
            return None
        except Exception as e:
            print(f"❌ Error obteniendo perfil: {e}")
            return None

    def get_my_leagues(self) -> List[Dict]:
        """Obtiene las ligas del usuario"""
        if not self.token:
            return []
        try:
            endpoints = [
                f"{BASE_URL}/user/{self.user_id}/leagues",
                f"{BASE_URL}/me/leagues",
                f"{BASE_URL}/leagues/mine",
            ]
            for url in endpoints:
                try:
                    if "None" in url:
                        continue
                    r = self.session.get(url, timeout=15)
                    if r.status_code == 200:
                        data = r.json()
                        leagues = data if isinstance(data, list) else data.get("leagues", [])
                        if leagues:
                            self.league_id = str(leagues[0].get("id") or "")
                            print(f"✅ Ligas: {len(leagues)}")
                            return leagues
                except:
                    continue
            return []
        except Exception as e:
            print(f"❌ Error ligas: {e}")
            return []

    def get_players_stats(self) -> List[Dict]:
        """Obtiene estadísticas de jugadores del mercado"""
        try:
            urls = [
                f"{BASE_URL}/player/market",
                f"{BASE_URL}/players?limit=500",
                f"{BASE_URL}/players/all",
            ]
            for url in urls:
                try:
                    r = self.session.get(url, timeout=30)
                    if r.status_code == 200:
                        data = r.json()
                        players = data if isinstance(data, list) else data.get("players", [])
                        print(f"✅ Jugadores: {len(players)}")
                        return players
                except:
                    continue
            return []
        except Exception as e:
            print(f"❌ Error jugadores: {e}")
            return []

    def get_market(self) -> Optional[Dict]:
        """Obtiene el mercado de fichajes"""
        if not self.token or not self.league_id:
            return None
        try:
            endpoints = [
                f"{BASE_URL}/league/{self.league_id}/market",
                f"{BASE_URL}/team/{self.team_id}/market",
            ]
            for url in endpoints:
                try:
                    if "None" in url:
                        continue
                    r = self.session.get(url, timeout=15)
                    if r.status_code == 200:
                        print("✅ Mercado obtenido")
                        return r.json()
                except:
                    continue
            return None
        except Exception as e:
            print(f"❌ Error mercado: {e}")
            return None

    def get_current_round(self) -> Optional[Dict]:
        """Obtiene información de la jornada actual"""
        try:
            urls = [f"{BASE_URL}/round/active", f"{BASE_URL}/calendar/current"]
            for url in urls:
                try:
                    r = self.session.get(url, timeout=15)
                    if r.status_code == 200:
                        return r.json()
                except:
                    continue
            return None
        except Exception as e:
            return None

    def get_full_data(self) -> Dict:
        """Obtiene todos los datos para el análisis de IA"""
        print("\n🔄 Obteniendo datos de LaLiga Fantasy...")

        result = {
            "authenticated": False,
            "team": None,
            "leagues": [],
            "market": None,
            "current_round": None,
            "standings": None,
            "players_stats": [],
            "errors": []
        }

        if not self.token:
            result["errors"].append(
                "Token no configurado. Ve a Render → Environment y añade FANTASY_TOKEN."
            )
            return result

        # Verificar token obteniendo perfil
        profile = self.get_my_profile()
        if not profile and not self.user_id:
            result["errors"].append("Token inválido o expirado.")
            return result

        result["authenticated"] = True

        result["leagues"] = self.get_my_leagues()
        result["team"] = self.get_my_team()
        result["market"] = self.get_market()
        result["current_round"] = self.get_current_round()
        result["players_stats"] = self.get_players_stats()[:50]

        print("\n✅ Datos obtenidos")
        return result

    def set_lineup(self, lineup_data: Dict) -> bool:
        if not self.token:
            return False
        try:
            url = f"{BASE_URL}/team/{self.team_id}/lineup"
            r = self.session.post(url, json=lineup_data, timeout=15)
            return r.status_code in [200, 201, 204]
        except:
            return False

    def buy_player(self, player_id: str, price: int) -> bool:
        if not self.token:
            return False
        try:
            r = self.session.post(f"{BASE_URL}/market/buy",
                                  json={"playerId": player_id, "price": price}, timeout=15)
            return r.status_code in [200, 201]
        except:
            return False

    def sell_player(self, player_id: str, price: int) -> bool:
        if not self.token:
            return False
        try:
            r = self.session.post(f"{BASE_URL}/market/sell",
                                  json={"playerId": player_id, "price": price}, timeout=15)
            return r.status_code in [200, 201]
        except:
            return False
