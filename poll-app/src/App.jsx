import { BrowserRouter, Routes, Route } from "react-router-dom";
import Navbar from "./components/Navbar";
import Footer from "./components/Footer";

import Home from "./pages/Home";
import About from "./pages/About";
import Contact from "./pages/Contact";
import Login from "./pages/Login";
import Polls from "./pages/Polls";
import Results from "./pages/Results";

function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <div className="min-h-screen">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/about" element={<About />} />
          <Route path="/contact" element={<Contact />} />
          <Route path="/login" element={<Login />} />
          <Route path="/polls" element={<Polls />} />
          <Route path="/results/:id" element={<Results />} />
        </Routes>
      </div>
      <Footer />
    </BrowserRouter>
  );
}

export default App;
