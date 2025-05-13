import { useEffect, useState } from "react";
import { Card, CardContent } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { AlertTriangle, Gauge, Flame } from "lucide-react";

export default function MetaDashboard() {
  const [meta, setMeta] = useState(null);

  useEffect(() => {
    const eventSource = new EventSource("/meta-stream");  // Connect to the SSE endpoint
    eventSource.onmessage = (e) => {
      try {
        setMeta(JSON.parse(e.data));  // Update state with received data
      } catch (err) {
        console.error("Bad JSON from stream", err);  // Handle JSON parse errors
      }
    };
    return () => eventSource.close();  // Cleanup when component is unmounted
  }, []);

  if (!meta) return <div className="p-4 text-gray-500">Waiting for data...</div>;  // Show loading message

  return (
    <div className="grid gap-4 p-4 md:grid-cols-2 lg:grid-cols-3">
      <Card>
        <CardContent className="p-4">
          <h2 className="text-xl font-bold mb-2">System Meta</h2>
          <p><strong>Timestamp:</strong> {meta.timestamp}</p>
          <p><strong>Total Drift:</strong> {meta.total_drift}</p>
          <p><strong>Max Velocity:</strong> {meta.max_velocity}</p>
          <p><strong>Avg Acceleration:</strong> {meta.avg_acceleration}</p>
          {meta.cluster_alert && <Badge variant="destructive"><AlertTriangle className="w-4 h-4 mr-1" /> Cluster Alert</Badge>}
        </CardContent>
      </Card>

      {Object.entries(meta.cart_metrics).map(([cart, regs]) => (
        <Card key={cart}>
          <CardContent className="p-4">
            <h3 className="text-lg font-semibold mb-1">Cart {cart}</h3>
            {Object.entries(regs).map(([reg, vals]) => (
              <div key={reg} className="flex justify-between text-sm">
                <span>{reg}</span>
                <span className="flex gap-2">
                  <Gauge className="w-4 h-4" /> {vals.avg_velocity},
                  <Flame className="w-4 h-4" /> {vals.avg_acceleration}
                </span>
              </div>
            ))}
          </CardContent>
        </Card>
      ))}
    </div>
  );
}
