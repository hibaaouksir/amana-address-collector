import { useEffect, useState } from "react";
import { useParams, useNavigate, Link } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import { getColis, type ColisWithAdresse } from "../services/colisService";

export default function DetailColisPage() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { user, logout } = useAuth();

  const [colis, setColis] = useState<ColisWithAdresse | null>(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

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

            {colis.adresse ? (
              <div className="bg-white rounded-lg shadow-sm overflow-hidden">
                <div className="border-b border-gray-200 px-6 py-4 bg-green-50">
                  <div className="flex items-center gap-2">
                    <span className="text-green-600 text-lg">OK</span>
                    <h3 className="text-lg font-semibold text-gray-900">
                      Adresse collectee par IA
                    </h3>
                  </div>
                  <p className="text-xs text-gray-600 mt-1">
                    Source : {colis.adresse.source === "gps" ? "Position GPS partagee" : "Message texte analyse"} - Extraite le {formatDate(colis.adresse.extracted_at)}
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
              <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-6 text-center">
                <p className="text-yellow-800 font-medium mb-1">Adresse non encore recue</p>
                <p className="text-sm text-yellow-700">
                  Le destinataire n a pas encore repondu au message WhatsApp.
                </p>
              </div>
            )}
          </div>
        )}
      </main>
    </div>
  );
}