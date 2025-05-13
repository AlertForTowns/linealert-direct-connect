import React from "react";
import { createRoot } from "react-dom/client";
import MetaDashboard from "./MetaDashboard";

const container = document.getElementById("root");
const root = createRoot(container);
root.render(<MetaDashboard />);
