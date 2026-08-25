import { useEffect, useState, type FormEvent } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import { getColis, simulateWhatsAppReply, type ColisWithAdresse } from "../services/colisService";

export default function DetailColisPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  const [colis, setColis] = useState<ColisWithAdresse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

  // Etats pour le formulaire de simulation
  const [simulatedMessage, setSimulatedMessage] = useState("");
  const [isSimulating, setIsSimulating] = useState(false);
  const [simulationError, setSimulationError] = useState("");
  const [simulationSuccess, setSimulationSuccess] = useState("");

  useEffect(() => {
    if (id) {
      loadColis(parseInt(id));
    }
  }, [id]);

  async function loadColis(colisId: number) {
    try {
      setIsLoading(true);
      const data = await getColis(colisId);
      setColis(data);
    } catch (err: any) {
      if (err.response?.status === 404) {
        setError(`Colis #${colisId} introuvable`);
      } else {
        setError("Erreur lors du chargement du colis");
      }
    } finally {
      setIsLoading(false);
    }
  }

  async function handleSimulate(e: FormEvent) {
    e.preventDefault();
    if (!colis || !simulatedMessage.trim()) return;

    setIsSimulating(true);
    setSimulationError("");
    setSimulationSuccess("");

    try {
      await simulateWhatsAppReply(colis.id, simulatedMessage);
      setSimulationSuccess("Adresse extraite avec succes ! Rechargement en cours...");
      setSimulatedMessage("");

      // Recharger le colis pour afficher la nouvelle adresse
      setTimeout(() => {
        loadColis(colis.id);
      }, 1500);
    } catch (err: any) {
      if (err.response?.status === 404) {
        setSimulationError(`Colis introuvable`);
      } else {
        setSimulationError("Erreur lors de l analyse. Verifie que le backend tourne.");
      }
    } finally {
      setIsSimulating(false);
    }
  }

  function handleLogout() {
    logout();
    navigate("/login");
  }

  function getStatutBadge(statut: string) {
    const styles: Record<string, string> = {
      en_attente: "bg-yellow-100 text-yellow-800 border-yellow-300",
      envoye: "bg-blue-100 text-blue-800 border-blue-300",
      adresse_recue: "bg-green-100 text-green-800 border-green-300",
      relance: "bg-orange-100 text-orange-800 border-orange-300",
      echec_envoi: "bg-red-100 text-red-800 border-red-300",
    };
    const labels: Record<string, string> = {
      en_attente: "En attente",
      envoye: "WhatsApp envoye",
      adresse_recue: "Adresse recue",
      relance: "Relance envoyee",
      echec_envoi: "Echec envoi",
    };

    const style = styles[statut] || "bg-gray-100 text-gray-800 border-gray-300";
    const label = labels[statut] || statut;

    return (
      <span className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium border ${style}`}>
        {label}
      </span>
    );
  }

  function formatDate(iso: string | null): string {
    if (!iso) return "-";
    const d = new Date(iso);
    return d.toLocaleString("fr-FR", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit",
    });
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <header className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-xl font-bold text-blue-600">Amana Address Collector</h1>
            <p className="text-xs text-gray-500 mt-0.5">Barid Al-Maghrib</p>
          </div>
          <div className="flex items-center gap-4">
            <div className="text-right">
              <p className="text-sm font-medium text-gray-900">{user?.name}</p>
              <p className="text-xs text-gray-500">{user?.email}</p>
            </div>
            <button
              onClick={handleLogout}
              className="text-sm text-gray-600 hover:text-red-600 border border-gray-300 hover:border-red-300 px-3 py-1.5 rounded-lg transition-colors"
            >
              Deconnexion
            </button>
          </div>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-6 py-8">
        <div className="mb-6">
          <Link
            to="/"
            className="text-sm text-gray-600 hover:text-blue-600 flex items-center gap-1"
          >
            &larr; Retour au tableau de bord
          </Link>
        </div>

        {isLoading && (
          <div className="bg-white rounded-lg shadow-sm p-12 text-center">
            <p className="text-gray-500">Chargement du colis...</p>
          </div>
        )}

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
            {error}
          </div>
        )}

        {colis && !isLoading && (
          <div className="space-y-6">
            {/* En-tete du colis */}
            <div className="bg-white rounded-lg shadow-sm p-6">
              <div className="flex items-start justify-between">
                <div>
                  <p className="text-sm text-gray-500 mb-1">Colis</p>
                  <h2 className="text-3xl font-bold text-gray-900 font-mono">
                    {colis.code_barres}
                  </h2>
                </div>
                <div>{getStatutBadge(colis.statut)}</div>
              </div>
            </div>

            {/* Informations */}
            <div className="bg-white rounded-lg shadow-sm overflow-hidden">
              <div className="border-b border-gray-200 px-6 py-4">
                <h3 className="text-lg font-semibold text-gray-900">Informations</h3>
              </div>
              <div className="p-6 grid grid-cols-2 gap-4">
                <div>
                  <p className="text-xs text-gray-500 uppercase tracking-wider mb-1">
                    Telephone destinataire
                  </p>
                  <p className="text-gray-900 font-medium">{colis.telephone}</p>
                </div>
                <div>
                  <p className="text-xs text-gray-500 uppercase tracking-wider mb-1">
                    Cree le
                  </p>
                  <p className="text-gray-900">{formatDate(colis.created_at)}</p>
                </div>
                <div>
                  <p className="text-xs text-gray-500 uppercase tracking-wider mb-1">
                    WhatsApp envoye
                  </p>
                  <p className="text-gray-900">{formatDate(colis.sent_at)}</p>
                </div>
                <div>
                  <p className="text-xs text-gray-500 uppercase tracking-wider mb-1">
                    Relance envoyee
                  </p>
                  <p className="text-gray-900">{formatDate(colis.reminder_sent_at)}</p>
                </div>
              </div>
            </div>

            {/* Adresse extraite - SI DEJA EXISTANTE */}
            {colis.adresse ? (
              <div className="bg-white rounded-lg shadow-sm overflow-hidden">
                <div className="border-b border-gray-200 px-6 py-4 bg-green-50">
                  <div className="flex items-center gap-2">
                    <span className="text-green-600 text-lg font-bold">OK</span>
                    <h3 className="text-lg font-semibold text-gray-900">
                      Adresse collectee par IA
                    </h3>
                  </div>
                  <p className="text-xs text-gray-600 mt-1">
                    Source : {colis.adresse.source === "gps" ? "Position GPS partagee" : "Message texte analyse par Gemini"} - Extraite le {formatDate(colis.adresse.extracted_at)}
                  </p>
                </div>
                <div className="p-6 space-y-4">
                  <div>
                    <p className="text-xs text-gray-500 uppercase tracking-wider mb-1">
                      Adresse principale
                    </p>
                    <p className="text-gray-900 font-medium">
                      {colis.adresse.ligne1 || <span className="text-gray-400 italic">Non renseigne</span>}
                    </p>
                  </div>
                  <div className="grid grid-cols-3 gap-4">
                    <div>
                      <p className="text-xs text-gray-500 uppercase tracking-wider mb-1">
                        Ville
                      </p>
                      <p className="text-gray-900">
                        {colis.adresse.ville || <span className="text-gray-400 italic">-</span>}
                      </p>
                    </div>
                    <div>
                      <p className="text-xs text-gray-500 uppercase tracking-wider mb-1">
                        Code postal
                      </p>
                      <p className="text-gray-900">
                        {colis.adresse.code_postal || <span className="text-gray-400 italic">-</span>}
                      </p>
                    </div>
                    <div>
                      <p className="text-xs text-gray-500 uppercase tracking-wider mb-1">
                        Coordonnees GPS
                      </p>
                      <p className="text-gray-900">
                        {colis.adresse.latitude && colis.adresse.longitude
                          ? `${colis.adresse.latitude}, ${colis.adresse.longitude}`
                          : <span className="text-gray-400 italic">-</span>}
                      </p>
                    </div>
                  </div>
                </div>
              </div>
            ) : (
              <>
                {/* Message "En attente" */}
                <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6 text-center">
                  <p className="text-yellow-800 font-medium mb-1">Adresse non encore recue</p>
                  <p className="text-sm text-yellow-700">
                    Le destinataire n a pas encore repondu au message WhatsApp.
                  </p>
                </div>

                {/* FORMULAIRE DE SIMULATION */}
                <div className="bg-white rounded-lg shadow-sm overflow-hidden">
                  <div className="border-b border-gray-200 px-6 py-4 bg-blue-50">
                    <div className="flex items-center gap-2">
                      <span className="text-blue-600 text-lg">AI</span>
                      <h3 className="text-lg font-semibold text-gray-900">
                        Simuler la reponse du destinataire
                      </h3>
                    </div>
                    <p className="text-xs text-gray-600 mt-1">
                      Copiez ici la reponse recue via WhatsApp Business. L IA analysera le message et extraira l adresse automatiquement.
                    </p>
                  </div>
                  <div className="p-6">
                    <form onSubmit={handleSimulate} className="space-y-4">
                      {simulationError && (
                        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
                          {simulationError}
                        </div>
                      )}

                      {simulationSuccess && (
                        <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg text-sm">
                          {simulationSuccess}
                        </div>
                      )}

                      <div>
                        <label htmlFor="message" className="block text-sm font-medium text-gray-700 mb-2">
                          Reponse du destinataire (texte, adresse, ou position GPS)
                        </label>
                        <textarea
                          id="message"
                          rows={4}
                          value={simulatedMessage}
                          onChange={(e) => setSimulatedMessage(e.target.value)}
                          disabled={isSimulating}
                          placeholder="Exemples : Rue Ibn Sina residence Al Andalous Agdal Rabat 10090&#10;salam ana f hay salam bloc 5&#10;Face a la mosquee verte Casablanca"
                          className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none disabled:bg-gray-100 font-mono text-sm"
                        />
                        <p className="text-xs text-gray-500 mt-1">
                          L IA comprend le francais, l arabe et la darija
                        </p>
                      </div>

                      <div className="flex items-center justify-end gap-3">
                        <button
                          type="submit"
                          disabled={isSimulating || !simulatedMessage.trim()}
                          className="bg-blue-600 hover:bg-blue-700 disabled:bg-blue-300 text-white font-medium px-6 py-2.5 rounded-lg transition-colors"
                        >
                          {isSimulating ? "Analyse IA en cours..." : "Analyser et enregistrer l adresse"}
                        </button>
                      </div>
                    </form>
                  </div>
                </div>
              </>
            )}
          </div>
        )}
      </main>
    </div>
  );
}