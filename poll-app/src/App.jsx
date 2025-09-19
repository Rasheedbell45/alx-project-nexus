import { BrowserRouter, Routes, Route } from "react-router-dom";
import Login from "./pages/Login";
import Polls from "./pages/Polls";
import Results from "./pages/Results";

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Login />} />
        <Route path="/polls" element={<Polls />} />
        <Route path="/results/:id" element={<Results />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
