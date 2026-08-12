"""
Cliente para LaLiga Fantasy Marca API
Reverse-engineered de la app oficial
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
}


class LaLigaFantasyClient:
    def __init__(self):
        self.email = os.getenv("FANTASY_EMAIL")
        self.password = os.getenv("FANTASY_PASSWORD")
        self.token: Optional[str] = None
        self.user_id: Optional[str] = None
        self.team_id: Optional[str] = None
        self.league_id: Optional[str] = None
        self.session = requests.Session()
        self.session.headers.update(HEADERS_BASE)
        self.session.verify = False

    def login(self) -> bool:
        """Autenticación en LaLiga Fantasy"""
        try:
            # Intento 1: Login directo con email/password
            url = f"{BASE_URL}/user/login"
            payload = {
                "email": self.email,
                "password": self.password,
                "lang": "es"
            }
            response = self.session.post(url, json=payload, timeout=15, verify=False)

            if response.status_code == 200:
                data = response.json()
                self.token = data.get("token") or data.get("access_token")
                self.user_id = str(data.get("user", {}).get("id") or data.get("id", ""))
                self.session.headers.update({"Authorization": f"Bearer {self.token}"})
                print(f"✅ Login exitoso. Usuario ID: {self.user_id}")
                return True

            # Intento 2: Endpoint alternativo
            url2 = f"{BASE_URL}/auth/login"
            response2 = self.session.post(url2, json=payload, timeout=15, verify=False)
            if response2.status_code == 200:
                data = response2.json()
                self.token = data.get("token") or data.get("access_token")
                self.user_id = str(data.get("user", {}).get("id") or "")
                self.session.headers.update({"Authorization": f"Bearer {self.token}"})
                print(f"✅ Login exitoso (v2). Usuario ID: {self.user_id}")
                return True

            print(f"❌ Login fallido. Status: {response.status_code} - {response.text[:200]}")
            return False

        except Exception as e:
            print(f"❌ Error en login: {e}")
            return False

    def get_my_team(self) -> Optional[Dict]:
        """Obtiene los datos del equipo del usuario"""
        try:
            # Obtener liga activa primero
            leagues = self.get_my_leagues()
            if leagues and len(leagues) > 0:
                self.league_id = str(leagues[0].get("id") or leagues[0].get("leagueId", ""))

            endpoints = [
                f"{BASE_URL}/user/{self.user_id}/team",
                f"{BASE_URL}/team/user/{self.user_id}",
                f"{BASE_URL}/user/{self.user_id}/manager",
            ]

            for url in endpoints:
                try:
                    response = self.session.get(url, timeout=15)
                    if response.status_code == 200:
                        data = response.json()
                        self.team_id = str(data.get("id") or data.get("teamId", ""))
                        print(f"✅ Equipo obtenido. Team ID: {self.team_id}")
                        return data
                except:
                    continue

            print("⚠️ No se pudo obtener el equipo")
            return None
        except Exception as e:
            print(f"❌ Error obteniendo equipo: {e}")
            return None

    def get_my_leagues(self) -> List[Dict]:
        """Obtiene las ligas del usuario"""
        try:
            endpoints = [
                f"{BASE_URL}/user/{self.user_id}/leagues",
                f"{BASE_URL}/leagues/user/{self.user_id}",
            ]
            for url in endpoints:
                try:
                    response = self.session.get(url, timeout=15)
                    if response.status_code == 200:
                        data = response.json()
                        leagues = data if isinstance(data, list) else data.get("leagues", [])
                        print(f"✅ Ligas obtenidas: {len(leagues)} liga(s)")
                        return leagues
                except:
                    continue
            return []
        except Exception as e:
            print(f"❌ Error obteniendo ligas: {e}")
            return []

    def get_players_stats(self) -> List[Dict]:
        """Obtiene estadísticas de todos los jugadores"""
        try:
            url = f"{BASE_URL}/player/market"
            response = self.session.get(url, timeout=30)
            if response.status_code == 200:
                data = response.json()
                players = data if isinstance(data, list) else data.get("players", [])
                print(f"✅ Jugadores obtenidos: {len(players)}")
                return players

            # Alternativa
            url2 = f"{BASE_URL}/players"
            response2 = self.session.get(url2, params={"limit": 500}, timeout=30)
            if response2.status_code == 200:
                data = response2.json()
                return data if isinstance(data, list) else data.get("players", [])

            return []
        except Exception as e:
            print(f"❌ Error obteniendo jugadores: {e}")
            return []

    def get_market(self) -> Optional[Dict]:
        """Obtiene el mercado de fichajes"""
        try:
            endpoints = [
                f"{BASE_URL}/league/{self.league_id}/market",
                f"{BASE_URL}/team/{self.team_id}/market",
                f"{BASE_URL}/market",
            ]
            for url in endpoints:
                try:
                    if "None" in url:
                        continue
                    response = self.session.get(url, timeout=15)
                    if response.status_code == 200:
                        print("✅ Mercado obtenido")
                        return response.json()
                except:
                    continue
            return None
        except Exception as e:
            print(f"❌ Error obteniendo mercado: {e}")
            return None

    def get_current_round(self) -> Optional[Dict]:
        """Obtiene información de la jornada actual"""
        try:
            endpoints = [
                f"{BASE_URL}/round/active",
                f"{BASE_URL}/calendar/current",
                f"{BASE_URL}/fixture/active",
            ]
            for url in endpoints:
                try:
                    response = self.session.get(url, timeout=15)
                    if response.status_code == 200:
                        print("✅ Jornada actual obtenida")
                        return response.json()
                except:
                    continue
            return None
        except Exception as e:
            print(f"❌ Error obteniendo jornada: {e}")
            return None

    def get_league_standings(self) -> Optional[Dict]:
        """Obtiene la clasificación de la liga"""
        try:
            if not self.league_id:
                return None
            url = f"{BASE_URL}/league/{self.league_id}/ranking"
            response = self.session.get(url, timeout=15)
            if response.status_code == 200:
                print("✅ Clasificación obtenida")
                return response.json()
            return None
        except Exception as e:
            print(f"❌ Error obteniendo clasificación: {e}")
            return None

    def set_lineup(self, lineup_data: Dict) -> bool:
        """Establece la alineación"""
        try:
            endpoints = [
                f"{BASE_URL}/team/{self.team_id}/lineup",
                f"{BASE_URL}/lineup",
            ]
            for url in endpoints:
                try:
                    if "None" in url:
                        continue
                    response = self.session.post(url, json=lineup_data, timeout=15)
                    if response.status_code in [200, 201, 204]:
                        print("✅ Alineación guardada")
                        return True
                except:
                    continue
            return False
        except Exception as e:
            print(f"❌ Error guardando alineación: {e}")
            return False

    def buy_player(self, player_id: str, price: int) -> bool:
        """Ficha un jugador del mercado"""
        try:
            url = f"{BASE_URL}/market/buy"
            payload = {"playerId": player_id, "price": price}
            response = self.session.post(url, json=payload, timeout=15)
            return response.status_code in [200, 201]
        except Exception as e:
            print(f"❌ Error fichando jugador: {e}")
            return False

    def sell_player(self, player_id: str, price: int) -> bool:
        """Vende un jugador al mercado"""
        try:
            url = f"{BASE_URL}/market/sell"
            payload = {"playerId": player_id, "price": price}
            response = self.session.post(url, json=payload, timeout=15)
            return response.status_code in [200, 201]
        except Exception as e:
            print(f"❌ Error vendiendo jugador: {e}")
            return False

    def get_full_data(self) -> Dict:
        """Obtiene todos los datos necesarios para el análisis de IA"""
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

        if not self.login():
            result["errors"].append("No se pudo autenticar. Verifica credenciales.")
            return result

        result["authenticated"] = True

        result["team"] = self.get_my_team()
        result["leagues"] = self.get_my_leagues()
        result["market"] = self.get_market()
        result["current_round"] = self.get_current_round()
        result["standings"] = self.get_league_standings()
        result["players_stats"] = self.get_players_stats()[:50]  # Top 50 jugadores

        print("\n✅ Datos obtenidos correctamente")
        return result


if __name__ == "__main__":
    client = LaLigaFantasyClient()
    data = client.get_full_data()
    print(json.dumps(data, indent=2, ensure_ascii=False, default=str)[:2000])
