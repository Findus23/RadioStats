from dataclasses import dataclass


@dataclass
class ChannelData:
    shortname: str
    stationname: str
    has_data: bool
    primary_color: str
    secondary_color: str


channels = {
    "oe1": ChannelData(
        shortname="oe1",
        stationname="Radio Ö1",
        has_data=True,
        primary_color="#b11a1a",
        secondary_color="#ffffff"
    ),
    "oe3": ChannelData(
        shortname="oe3",
        has_data=True,
        primary_color="#002350",
        secondary_color="#E10032",
        stationname="Hitradio Ö3"

    ),
    "fm4": ChannelData(
        shortname="fm4",
        stationname="Radio FM4",
        has_data=True,
        primary_color="#FFE500",
        secondary_color="#000000",
    ),
    "bgl": ChannelData(
        shortname="bgl",
        stationname="Radio Burgenland",
        has_data=True,
        primary_color="#ffa60f",
        secondary_color="#d32824"
    ),
    "ktn": ChannelData(
        shortname="ktn",
        stationname="Radio Kärnten",
        has_data=True,
        primary_color="#bc1716",
        secondary_color="#ffcd00"
    ),
    "noe": ChannelData(
        shortname="noe",
        stationname="Radio Niederösterreich",
        has_data=True,
        primary_color="#002777",
        secondary_color="#ffcd00"
    ),
    "ooe": ChannelData(
        shortname="ooe",
        stationname="Radio Oberösterreich",
        has_data=True,
        primary_color="#bc1716",
        secondary_color="#ffffff"
    ),
    "sbg": ChannelData(
        shortname="sbg",
        stationname="Radio Salzburg",
        has_data=True,
        primary_color="#bc1716",
        secondary_color="#ffffff"
    ),
    "stm": ChannelData(
        shortname="stm",
        stationname="Radio Steiermark",
        has_data=True,
        primary_color="#006843",
        secondary_color="#ffffff"
    ),
    "tir": ChannelData(
        shortname="tir",
        stationname="Radio Tirol",
        has_data=True,
        primary_color="#bc1716",
        secondary_color="#ffffff"
    ),
    "vbg": ChannelData(
        shortname="vbg",
        stationname="Radio Vorarlberg",
        has_data=True,
        primary_color="#bc1716",
        secondary_color="#ffffff"
    ),
    "wie": ChannelData(
        shortname="wie",
        stationname="Radio Wien",
        has_data=True,
        primary_color="#ee7e01",
        secondary_color="#552382"
    ),
    "kht": ChannelData(
        shortname="kht",
        stationname="Kronehit",
        has_data=True,
        primary_color="#000000",
        secondary_color="#b89c4f"
    ),
    "886": ChannelData(
        shortname="886",
        stationname="Radio 88.6",
        has_data=True,
        primary_color="#123e6b",
        secondary_color="#ffe116"
    ),
    "ara": ChannelData(
        shortname="ara",
        stationname="Radio Arabella",
        has_data=True,
        primary_color="#003e88",
        secondary_color="#e6007e"
    ),
    "eng": ChannelData(
        shortname="eng",
        stationname="Engergy Wien/Nö/Bgld",
        has_data=True,
        primary_color="#000000",
        secondary_color="#E2001A"
    ),
    "all": ChannelData(
        shortname="all",
        stationname="Alle",
        has_data=True,
        primary_color="black",
        secondary_color="white"
    ),
}
