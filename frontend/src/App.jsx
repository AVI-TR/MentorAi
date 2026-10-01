import React from 'react';
import { BrowserRouter, Routes, Route, useLocation, Navigate } from 'react-router-dom';
import { AnimatePresence } from 'framer-motion';
import { MentorProvider } from './context/MentorContext';
import Navbar from './components/Navbar';
import ProgressIndicator from './components/ProgressIndicator';

import WelcomePage from './pages/WelcomePage';
import ProfilePage from './pages/ProfilePage';
import CareerGoalPage from './pages/CareerGoalPage';
import SkillAssessmentPage from './pages/SkillAssessmentPage';
import AnalysisPage from './pages/AnalysisPage';
import RoadmapPage from './pages/RoadmapPage';

function AnimatedRoutes() {
  const location = useLocation();

  return (
    <AnimatePresence mode="wait">
      <Routes location={location} key={location.pathname}>
        <Route path="/" element={<WelcomePage />} />
        <Route path="/profile" element={<ProfilePage />} />
        <Route path="/goal" element={<CareerGoalPage />} />
        <Route path="/skills" element={<SkillAssessmentPage />} />
        <Route path="/analysis" element={<AnalysisPage />} />
        <Route path="/roadmap" element={<RoadmapPage />} />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </AnimatePresence>
  );
}

export default function App() {
  return (
    <MentorProvider>
      <BrowserRouter>
        <div className="app-layout">
          <Navbar />
          <ProgressIndicator />
          <main className="main-content">
            <AnimatedRoutes />
          </main>
          <footer className="app-footer">
            <div className="footer-content">
              <span>Mentor AI • Career Mentorship Platform</span>
            </div>
          </footer>
        </div>
      </BrowserRouter>
    </MentorProvider>
  );
}
