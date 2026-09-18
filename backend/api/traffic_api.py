from fastapi import APIRouter
import pandas as pd
import numpy as np


router = APIRouter()


@router.get("/traffic")
def get_traffic_data():

    # LOAD CSV
    df = pd.read_csv("logs/network_traffic.csv")

    # REPLACE NaN VALUES
    df = df.replace({np.nan: None})

    # TOTAL PACKETS
    total_packets = len(df)

    # PROTOCOL STATS
    protocol_counts = (
        df["Protocol"]
        .value_counts()
        .to_dict()
    )

    # AVERAGE PACKET SIZE
    average_packet_size = round(
        df["Packet_Size"].mean(),
        2
    )

    # LAST 10 PACKETS
    latest_packets = (
        df.tail(10)
        .to_dict(orient="records")
    )

    return {

        "total_packets": total_packets,

        "protocol_distribution":
        protocol_counts,

        "average_packet_size":
        average_packet_size,

        "latest_packets":
        latest_packets
    }