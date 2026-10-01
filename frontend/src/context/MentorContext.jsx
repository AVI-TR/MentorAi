import React, { createContext, useContext, useState, useEffect, useCallback } from 'react';
import { api } from '../api/client';

const MentorContext = createContext(null);

export function MentorProvider({ children }) {
  // Profile state
  const [profile, setProfile] = useState({
    email: '',
    education: '',
    year: '',
    interests: '',
  });

  // Career state
  const [careers, setCareers] = useState([]);
  const [selectedCareer, setSelectedCareer] = useState(null);
  const [careerDetails, setCareerDetails] = useState(null);
  const [isLoadingCareers, setIsLoadingCareers] = useState(true);
  const [isLoadingDetails, setIsLoadingDetails] = useState(false);

  // Skill assessments: { [skill_id]: 1 | 2 | 3 | 4 | 5 }
  const [skillLevels, setSkillLevels] = useState({});

  // Analysis and backend execution state
  const [analysisResult, setAnalysisResult] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisError, setAnalysisError] = useState(null);

  // User and Goal records returned from API
  const [currentUser, setCurrentUser] = useState(null);
  const [currentGoal, setCurrentGoal] = useState(null);

  // Load careers list on mount
  useEffect(() => {
    let isMounted = true;
    async function loadCareers() {
      setIsLoadingCareers(true);
      try {
        const data = await api.getCareers();
        if (isMounted) {
          setCareers(data || []);
        }
      } catch (err) {
        console.error('Failed to load careers:', err);
      } finally {
        if (isMounted) {
          setIsLoadingCareers(false);
        }
      }
    }
    loadCareers();
    return () => {
      isMounted = false;
    };
  }, []);

  // When a career is selected, fetch its required skills
  const selectCareer = useCallback(async (career) => {
    if (!career) return;
    setSelectedCareer(career);
    setIsLoadingDetails(true);
    try {
      const details = await api.getCareer(career.id);
      setCareerDetails(details);

      // Pre-initialize any missing skills with 1 (Beginner) as default if not already chosen
      setSkillLevels((prev) => {
        const updated = { ...prev };
        details.career_skills?.forEach((cs) => {
          if (!updated[cs.skill_id]) {
            updated[cs.skill_id] = 1; // Default to Beginner
          }
        });
        return updated;
      });
    } catch (err) {
      console.error('Failed to load career details:', err);
    } finally {
      setIsLoadingDetails(false);
    }
  }, []);

  // Set skill level
  const setSkillLevel = useCallback((skillId, level) => {
    setSkillLevels((prev) => ({
      ...prev,
      [skillId]: level,
    }));
  }, []);

  // Update profile fields
  const updateProfile = useCallback((fields) => {
    setProfile((prev) => ({
      ...prev,
      ...fields,
    }));
  }, []);

  // Run the full analysis pipeline against the backend
  const runAnalysis = useCallback(async () => {
    if (!profile.email?.trim()) {
      throw new Error('Email is required.');
    }
    if (!selectedCareer || !careerDetails) {
      throw new Error('Please select a career goal.');
    }

    setIsAnalyzing(true);
    setAnalysisError(null);

    try {
      // 1. Get or create user by email
      const user = await api.getOrCreateUser(profile.email.trim());
      setCurrentUser(user);

      // 2. Upsert profile information
      await api.upsertProfile(user.id, {
        education: profile.education?.trim() || null,
        year: profile.year?.trim() || null,
        interests: profile.interests?.trim() || null,
      });

      // 3. Upsert student skills for the selected career
      const requiredSkills = careerDetails.career_skills || [];
      for (const cs of requiredSkills) {
        const level = skillLevels[cs.skill_id] || 1;
        await api.upsertStudentSkill(user.id, cs.skill_id, level, 'self_assessed');
      }

      // 4. Create career goal
      const goal = await api.createCareerGoal(user.id, selectedCareer.id, 'active');
      setCurrentGoal(goal);

      // 5. Generate gap analysis snapshot
      const result = await api.createGapAnalysis(goal.id);
      setAnalysisResult(result);
      return result;
    } catch (err) {
      setAnalysisError(err.message || 'Failed to complete analysis.');
      throw err;
    } finally {
      setIsAnalyzing(false);
    }
  }, [profile, selectedCareer, careerDetails, skillLevels]);

  const value = {
    profile,
    updateProfile,
    careers,
    selectedCareer,
    selectCareer,
    careerDetails,
    isLoadingCareers,
    isLoadingDetails,
    skillLevels,
    setSkillLevel,
    analysisResult,
    isAnalyzing,
    analysisError,
    runAnalysis,
    currentUser,
    currentGoal,
  };

  return <MentorContext.Provider value={value}>{children}</MentorContext.Provider>;
}

export function useMentor() {
  const context = useContext(MentorContext);
  if (!context) {
    throw new Error('useMentor must be used within a MentorProvider');
  }
  return context;
}
