from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
from typing import Optional, Union, List, NamedTuple
import requests
import json

mcp = FastMCP('SimpleMcpServer', version="11.45.14")

@mcp.resource(
    uri="greeting://{name}",
    name='greeting',
    description='A resource protocol for demonstration'
)
def get_greeting(name: str) -> str: 
    # Handle greeting://{name} resource access protocol and return
    # For simplicity, directly return "Hello, balabala"
    return f"Hello, {name}!"

@mcp.prompt(
    name='translate',
    description='Prompt for translation'
)
def translate(message: str) -> str:
    return f'Please translate the following text to Chinese:\n\n{message}'

class PathParams(BaseModel):
    start: str
    end: str

@mcp.tool(name="test", description="Used for testing")
def test(
    params: PathParams,
    test1: str,
    test2: Union[str, List[str]] = Field("", description="Test parameter 2"),
    test3: Optional[str] = Field(None, description="Test parameter 3")
):
    return [test1, test2, test3, params]


class CityWeather(NamedTuple):
    city_name_en: str
    city_name_cn: str
    city_code: str
    temp: str
    wd: str  # wind direction
    ws: str  # wind speed
    sd: str  # humidity
    aqi: str # air quality index
    weather: str

def get_city_weather_by_city_name(city_code: str) -> Optional[CityWeather]:
    """Get weather information by city code"""

    if not city_code:
        print(f"Cannot find city corresponding to {city_code}")
        return None

    try:
        # Construct request URL
        url = f"http://d1.weather.com.cn/sk_2d/{city_code}.html"

        # Set request headers
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36 Edg/115.0.0.0",
            "Host": "d1.weather.com.cn",
            "Referer": "http://www.weather.com.cn/"
        }

        # Send HTTP request
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        # Parse JSON data
        # Handle encoding issues before parsing JSON
        content = response.text.encode('latin1').decode('unicode_escape')
        json_start = content.find("{")
        json_str = content[json_start:]

        weather_data = json.loads(json_str)

        # Construct return object
        return CityWeather(
            city_name_en=weather_data.get("nameen", ""),
            city_name_cn=weather_data.get("cityname", "").encode('latin1').decode('utf-8'),
            city_code=weather_data.get("city", ""),
            temp=weather_data.get("temp", ""),
            wd=weather_data.get("wd", "").encode('latin1').decode('utf-8'),
            ws=weather_data.get("ws", "").encode('latin1').decode('utf-8'),
            sd=weather_data.get("sd", ""),
            aqi=weather_data.get("aqi", ""),
            weather=weather_data.get("weather", "").encode('latin1').decode('utf-8')
        )

    except Exception as e:
        print(f"Failed to get weather information: {str(e)}")
        return None

@mcp.tool(
    name='weather',
    description='Get weather information for a city using its weather forecast city code (int)'
)
def get_weather_by_code(city_code: int) -> str:
    """Simulates weather query protocol, returns formatted string"""
    city_weather = get_city_weather_by_city_name(city_code)
    return str(city_weather)

@mcp.tool(
    name='fixed_string',
    description='Returns a fixed string'
)
def get_fixed_string() -> str:
    """Returns a fixed demonstration string"""
    return "This is a fixed string returned by the MCP tool"