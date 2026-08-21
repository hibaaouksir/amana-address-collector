import { useState, type FormEvent } from "react";
import { useNavigate, Link } from "react-router-dom";
import { createColis } from "../services/colisService";

export default function NouveauColisPage() {
  const [codeBarres, setCodeBarres] = useState("");
  const [telephone, setTelephone] = useState("+212");
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");

  const navigate = useNavigate();

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError("");
    setSuccess("");
    setIsSubmitting(true);

    try {
      const colis = await createColis(codeBarres, telephone);
      setSuccess(`Colis ${colis.code_barres} enregistre. Envoi WhatsApp en cours...`);

      // Redirection vers le dashboard apres 2 secondes
      setTimeout(() => {
        navigate("/");
      }, 2000);
    } catch (err: any) {
      if (err.response?.status === 409) {
        setError(`Un colis avec le code-barres ${codeBarres} existe deja.`);
      } else if (err.code === "ERR_NETWORK") {
        setError("Impossible de contacter le serveur. Verifie que le backend tourne.");
      } else {
        setError("Une erreur est survenue. Reessaye.");
      }
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header simple */}
      <header className="bg-white border-b border-gray-200 shadow-sm">
        <div className="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-xl font-bold text-blue-600">Amana Address Collector</h1>
            <p className="text-xs text-gray-500 mt-0.5">Barid Al-Maghrib</p>
          </div>
          <Link
            to="/"
            className="text-sm text-gray-600 hover:text-gray-900"
          >
            &larr; Retour au tableau de bord
          </Link>
        </div>
      </header>

      {/* Formulaire */}
      <main className="max-w-2xl mx-auto px-6 py-8">
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-gray-900">Enregistrer un nouveau colis</h2>
          <p className="text-sm text-gray-600 mt-1">
            Un message WhatsApp sera envoye automatiquement au destinataire pour recuperer son adresse.
          </p>
        </div>

        <div className="bg-white rounded-lg shadow-sm p-8">
          <form onSubmit={handleSubmit} className="space-y-6">
            {/* Message d erreur */}
            {error && (
              <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg text-sm">
                {error}
              </div>
            )}

            {/* Message de succes */}
            {success && (
              <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-3 rounded-lg text-sm">
                {success}
              </div>
            )}

            {/* Code-barres */}
            <div>
              <label htmlFor="code_barres" className="block text-sm font-medium text-gray-700 mb-1">
                Code-barres du colis
              </label>
              <input
                id="code_barres"
                type="text"
                value={codeBarres}
                onChange={(e) => setCodeBarres(e.target.value.toUpperCase())}
                required
                disabled={isSubmitting}
                placeholder="AM2026XXX"
                autoFocus
                className="w-full px-4 py-2 border border-gray-300 rounded-lg font-mono focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none disabled:bg-gray-100"
              />
              <p className="text-xs text-gray-500 mt-1">
                Scannez avec la douchette ou saisissez manuellement
              </p>
            </div>

            {/* Telephone */}
            <div>
              <label htmlFor="telephone" className="block text-sm font-medium text-gray-700 mb-1">
                Numero de telephone du destinataire
              </label>
              <input
                id="telephone"
                type="tel"
                value={telephone}
                onChange={(e) => setTelephone(e.target.value)}
                required
                disabled={isSubmitting}
                placeholder="+212612345678"
                className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent outline-none disabled:bg-gray-100"
              />
              <p className="text-xs text-gray-500 mt-1">
                Format international avec le code pays (+212 pour le Maroc)
              </p>
            </div>

            {/* Boutons */}
            <div className="flex items-center justify-end gap-3 pt-4 border-t border-gray-200">
              <Link
                to="/"
                className="text-gray-600 hover:text-gray-900 px-4 py-2 text-sm font-medium"
              >
                Annuler
              </Link>
              <button
                type="submit"
                disabled={isSubmitting}
                className="bg-blue-600 hover:bg-blue-700 disabled:bg-blue-400 text-white font-medium px-6 py-2.5 rounded-lg transition-colors"
              >
                {isSubmitting ? "Enregistrement..." : "Enregistrer et envoyer WhatsApp"}
              </button>
            </div>
          </form>
        </div>

        {/* Info supplementaire */}
        <div className="mt-6 bg-blue-50 border border-blue-200 rounded-lg p-4">
          <p className="text-sm text-blue-900 font-medium mb-1">A savoir</p>
          <p className="text-xs text-blue-800">
            Le destinataire recevra un message WhatsApp lui demandant son adresse.
            Sa reponse sera automatiquement analysee par IA pour extraire l adresse structuree.
          </p>
        </div>
      </main>
    </div>
  );
}