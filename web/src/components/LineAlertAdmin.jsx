import { useState } from "react";

function LineAlertAdmin() {
  const [file, setFile] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const handleUpload = async () => {
    if (!file) return;
    setLoading(true);
    setError(null);
    setResult(null);

    const formData = new FormData();
    formData.append("snapshot", file);

    try {
      const res = await fetch("/api/drift-test", {
        method: "POST",
        body: formData,
      });

      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.error || "Drift test failed.");
      }
      setResult(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleLearn = async (register, value) => {
    try {
      const res = await fetch("/api/learn", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ register, value }),
      });

      const data = await res.json();
      if (!res.ok) {
        throw new Error(data.error || "Learn request failed.");
      }
      alert(`✅ Learned Register ${register} = ${value}`);
    } catch (err) {
      alert(`❌ Learn Failed: ${err.message}`);
    }
  };

  return (
    <div className="min-h-screen bg-gray-100 flex items-center justify-center p-6">
      <div className="w-full max-w-xl bg-white rounded-xl shadow-lg p-6 space-y-6">
        <h1 className="text-2xl font-bold text-center">LineAlert Tech Admin Portal</h1>

        <div className="space-y-2">
          <label className="block text-sm font-medium text-gray-700">Upload Snapshot (.lasnap)</label>
          <input
            type="file"
            accept=".lasnap"
            onChange={(e) => setFile(e.target.files[0])}
            className="block w-full rounded border border-gray-300 p-2"
          />
          <button
            onClick={handleUpload}
            disabled={loading || !file}
            className="w-full bg-blue-600 text-white font-semibold py-2 px-4 rounded hover:bg-blue-700 disabled:opacity-50"
          >
            {loading ? "Running Drift Test..." : "Run Drift Test"}
          </button>
        </div>

        {error && (
          <div className="bg-red-100 text-red-700 p-4 rounded border border-red-400">
            ❌ Error: {error}
          </div>
        )}

        {result && (
          <div className="bg-gray-50 border border-gray-300 rounded p-4">
            <h2 className="text-lg font-semibold mb-2">Validation Results</h2>
            {result.passed ? (
              <p className="text-green-600 font-medium">✅ Snapshot PASSED</p>
            ) : (
              <>
                <p className="text-red-600 font-medium">❌ Snapshot FAILED</p>
                <ul className="list-disc ml-5 mt-2 text-sm text-red-500">
                  {result.violations.map((v, idx) => (
                    <li key={idx}>
                      Register {v.register} = {v.value} (expected range:{" "}
                      {v.min !== null && v.max !== null ? `${v.min}-${v.max}` : "?-?"})
                      {(v.min === null || v.max === null) && (
                        <button
                          onClick={() => handleLearn(v.register, v.value)}
                          className="ml-3 bg-yellow-300 text-black px-2 py-1 rounded text-xs hover:bg-yellow-400"
                        >
                          Learn This
                        </button>
                      )}
                    </li>
                  ))}
                </ul>
              </>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default LineAlertAdmin;
