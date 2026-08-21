import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../contexts/AuthContext";
import { listColis, type Colis } from "../services/colisService";

export default function DashboardPage() {
  const { user, logout } = useAuth();
  const navigate = useNavigate();

  const [colis, setColis] = useState<Colis[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    loadColis();
  }, []);

  async function loadColis() {
    try {
      setIsLoading(true);
      setError("");
      const data = await listColis();
      setColis(data);
    } catch (err: any) {
      setError("Impossible de charger les colis. Verifie que le backend tourne.");
    } finally {
      setIsLoading(false);
    }
  }

  function handleLogout() {
    logout();
    navigate("/login");
  }

  // Fonction utilitaire pour afficher les statuts en couleur
  function getStatutBadge(statut: string) {
    const styles: Record<string, string> = {
      en_attente: "bg-yellow-100 text-yellow-800",
      envoye: "bg-blue-100 text-blue-800",
      adresse_recue: "bg-green-100 text-green-800",
      relance: "bg-orange-100 text-orange-800",
      echec_envoi: "bg-red-100 text-red-800",
      echoue: "bg-red-100 text-red-800",
    };
    const labels: Record<string, string> = {
      en_attente: "En attente",
      envoye: "WhatsApp envoye",
      adresse_recue: "Adresse recue",
      relance: "Relance envoyee",
      echec_envoi: "Echec envoi",
      echoue: "Echoue",
    };

    const style = styles[statut] || "bg-gray-100 text-gray-800";
    const label = labels[statut] || statut;

    return (
      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${style}`}>
        {label}
      </span>
    );
  }

  // Format d une date ISO en jj/mm/aaaa HH:mm
  function formatDate(iso: string): string {
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
      {/* Header */}
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

      {/* Contenu principal */}
      <main className="max-w-7xl mx-auto px-6 py-8">
        {/* Barre d actions */}
        <div className="flex items-center justify-between mb-6">
          <div>
            <h2 className="text-2xl font-bold text-gray-900">Tableau de bord</h2>
            <p className="text-sm text-gray-600 mt-1">
              {colis.length} colis au total
            </p>
          </div>
          <button
            onClick={() => navigate("/colis/nouveau")}
            className="bg-blue-600 hover:bg-blue-700 text-white font-medium px-4 py-2 rounded-lg flex items-center gap-2 transition-colors"
          >
            <span className="text-xl leading-none">+</span>
            Nouveau colis
          </button>
        </div>

        {/* Message d erreur */}
        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm mb-6">
            {error}
          </div>
        )}

        {/* Etat de chargement */}
        {isLoading && (
          <div className="bg-white rounded-lg shadow-sm p-12 text-center">
            <p className="text-gray-500">Chargement des colis...</p>
          </div>
        )}

        {/* Liste vide */}
        {!isLoading && colis.length === 0 && !error && (
          <div className="bg-white rounded-lg shadow-sm p-12 text-center">
            <p className="text-gray-500 mb-2">Aucun colis enregistre pour l instant</p>
            <p className="text-sm text-gray-400">Cliquez sur "+ Nouveau colis" pour commencer</p>
          </div>
        )}

        {/* Tableau des colis */}
        {!isLoading && colis.length > 0 && (
          <div className="bg-white rounded-lg shadow-sm overflow-hidden">
            <table className="w-full">
              <thead className="bg-gray-50 border-b border-gray-200">
                <tr>
                  <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Code-barres
                  </th>
                  <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Telephone
                  </th>
                  <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Statut
                  </th>
                  <th className="text-left px-6 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Cree le
                  </th>
                  <th className="text-right px-6 py-3 text-xs font-medium text-gray-500 uppercase tracking-wider">
                    Actions
                  </th>
                </tr>
              </thead>
              <tbody className="divide-y divide-gray-200">
                {colis.map((c) => (
                  <tr key={c.id} className="hover:bg-gray-50 transition-colors">
                    <td className="px-6 py-4 text-sm font-mono font-medium text-gray-900">
                      {c.code_barres}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-700">
                      {c.telephone}
                    </td>
                    <td className="px-6 py-4">
                      {getStatutBadge(c.statut)}
                    </td>
                    <td className="px-6 py-4 text-sm text-gray-600">
                      {formatDate(c.created_at)}
                    </td>
                    <td className="px-6 py-4 text-right">
                      <button
                        onClick={() => navigate(`/colis/${c.id}`)}
                        className="text-blue-600 hover:text-blue-800 text-sm font-medium"
                      >
                        Voir details
                      </button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </main>
    </div>
  );
}