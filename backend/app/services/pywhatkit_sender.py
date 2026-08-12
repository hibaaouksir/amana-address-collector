"""
Implementation WhatsAppSender utilisant pywhatkit dans un processus separe.

Pywhatkit ne fonctionne pas de facon fiable dans un thread FastAPI a cause de
problemes de permissions pyautogui. On l isole donc dans un subprocess dedie.
"""
import base64
import subprocess
import sys
from datetime import datetime
from pathlib import Path

from app.services.whatsapp_sender import WhatsAppSender


class PywhatkitSender(WhatsAppSender):
    """Envoi WhatsApp via pywhatkit lance en subprocess."""

    def __init__(self):
        # Chemin absolu du script worker
        self.worker_path = Path(__file__).parent / "_pywhatkit_worker.py"
        if not self.worker_path.exists():
            raise RuntimeError(f"Worker introuvable : {self.worker_path}")

    def send_message(self, to_phone: str, message: str) -> dict:
        """Lance le script worker en subprocess pour envoyer le message."""
        try:
            # Encoder le message en base64 pour eviter les problemes de shell
            message_b64 = base64.b64encode(message.encode("utf-8")).decode("ascii")

            # Lancer le subprocess avec le meme Python que le backend
            result = subprocess.run(
                [sys.executable, str(self.worker_path), to_phone, message_b64],
                capture_output=True,
                text=True,
                timeout=60,  # Timeout de securite
            )

            if result.returncode == 0:
                return {
                    "success": True,
                    "message_id": f"pywhatkit-{datetime.now().isoformat()}",
                    "provider": "pywhatkit",
                    "worker_output": result.stdout,
                }
            else:
                return {
                    "success": False,
                    "error": f"Worker returncode={result.returncode} | stdout={result.stdout} | stderr={result.stderr}",
                    "provider": "pywhatkit",
                }

        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "error": "Worker timeout apres 60 secondes",
                "provider": "pywhatkit",
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "provider": "pywhatkit",
            }