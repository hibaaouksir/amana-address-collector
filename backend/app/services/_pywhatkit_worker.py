"""
Script standalone d envoi WhatsApp via pywhatkit.

Appele en subprocess par PywhatkitSender pour eviter les problemes 
de threading dans FastAPI.

Usage : python _pywhatkit_worker.py <phone> <message_base64>
"""
import sys
import base64


def main():
    if len(sys.argv) != 3:
        print("ERROR: Usage: python _pywhatkit_worker.py <phone> <message_base64>")
        sys.exit(1)

    phone = sys.argv[1]
    message_b64 = sys.argv[2]

    # Decoder le message (encode en base64 pour eviter les problemes de shell)
    try:
        message = base64.b64decode(message_b64).decode("utf-8")
    except Exception as e:
        print(f"ERROR: base64 decode failed: {e}")
        sys.exit(1)

    if not phone.startswith("+"):
        phone = "+" + phone.lstrip("0")

    print(f"[worker] Envoi WhatsApp vers {phone}")

    try:
        import pywhatkit
        pywhatkit.sendwhatmsg_instantly(
            phone_no=phone,
            message=message,
            wait_time=15,
            tab_close=True,
            close_time=5,
        )
        print("[worker] SUCCESS")
        sys.exit(0)
    except Exception as e:
        print(f"[worker] ERROR: {e}")
        sys.exit(2)


if __name__ == "__main__":
    main()