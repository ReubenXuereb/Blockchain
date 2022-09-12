import datetime
import json
import requests
import src.creds


class GNS:
    """
    This class serves as the interface between your program and the Genie Notification System
    """
    @staticmethod
    def send_to_gns(notification_message: str) -> bool:
        """
        Sends the notification message to Genie’s Notification System. This specific implementation will print this to the
        standard output stream.
        :returns: True when successful, False otherwise
        """

        if not notification_message.strip():
            return False

        url = "https://api.eu.opsgenie.com/v2/alerts"
        headers = {"Authorization": src.creds.api_key}
        notification = {
            "source": "Kraken Price Changes",
            "message": notification_message,
            "sent_timestamp": json.dumps(datetime.datetime.now(), indent=4, sort_keys=True, default=str)

        }
        req = requests.post(url, headers=headers, json=notification)
        print(req.json())
        print(notification)

        return True
