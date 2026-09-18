from alerts.alert_manager import create_alert


def detect_anomaly(

    source_ip,
    destination_ip,
    protocol,
    source_port,
    destination_port,
    packet_size
):

    # LARGE PACKET DETECTION
    if packet_size > 1500:

        create_alert(

            "Large Packet Attack",

            "HIGH",

            source_ip,

            f"Suspicious packet size detected: {packet_size}",

            packet_size,

            protocol,

            destination_port
        )

    # PORT SCAN DETECTION
    suspicious_ports = [

        22,
        23,
        3389,
        445
    ]

    if destination_port in suspicious_ports:

        create_alert(

            "Suspicious Port Access",

            "MEDIUM",

            source_ip,

            f"Access attempt on port {destination_port}",

            packet_size,

            protocol,

            destination_port
        )

    # ICMP FLOOD
    if protocol == "ICMP":

        create_alert(

            "ICMP Flood",

            "HIGH",

            source_ip,

            "High ICMP traffic detected",

            packet_size,

            protocol,

            destination_port
        )