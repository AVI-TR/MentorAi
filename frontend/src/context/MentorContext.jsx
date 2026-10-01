import React, { createContext, useCallback, useEffect, useMemo, useState } from 'react';
import { api } from '../api/client';

export const MentorContext = createContext(null);
const USER_ID_KEY = 'mentor:userId';
const GOAL_ID_KEY = 'mentor:goalId';

const clearStoredIds = () => {
  localStorage.removeItem(USER_ID_KEY);
  localStorage.removeItem(GOAL_ID_KEY);
};

export function MentorProvider({ children }) {
  const [profile, setProfile] = useState({ email: '', education: '', year: '', interests: '' });
  const [careers, setCareers] = useState([]);
  const [selectedCareer, setSelectedCareer] = useState(null);
  const [careerDetails, setCareerDetails] = useState(null);
  const [isLoadingCareers, setIsLoadingCareers] = useState(true);
  const [isLoadingDetails, setIsLoadingDetails] = useState(false);
  const [skillLevels, setSkillLevels] = useState({});
  const [analysisResult, setAnalysisResult] = useState(null);
  const [roadmap, setRoadmap] = useState(null);
  const [isLoadingRoadmap, setIsLoadingRoadmap] = useState(false);
  const [roadmapError, setRoadmapError] = useState(null);
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisError, setAnalysisError] = useState(null);
  const [currentUser, setCurrentUser] = useState(null);
  const [currentGoal, setCurrentGoal] = useState(null);
  const [sessionLoading, setSessionLoading] = useState(true);
  const [sessionError, setSessionError] = useState(null);

  useEffect(() => {
    let mounted = true;
    api.getCareers()
      .then((data) => mounted && setCareers(data || []))
      .catch(() => mounted && setSessionError('Unable to load career paths. Check the backend and retry.'))
      .finally(() => mounted && setIsLoadingCareers(false));
    return () => { mounted = false; };
  }, []);

  const restoreSession = useCallback(async () => {
    const userId = localStorage.getItem(USER_ID_KEY);
    const goalId = localStorage.getItem(GOAL_ID_KEY);
    if (!userId || !goalId) {
      setSessionLoading(false);
      return;
    }

    try {
      const [user, goal, analysis, savedRoadmap] = await Promise.all([
        api.getUser(userId),
        api.getCareerGoal(userId, goalId),
        api.getLatestGapAnalysis(goalId),
        api.getLatestRoadmap(goalId).catch((error) => {
          if (error.status === 404) return null;
          throw error;
        }),
      ]);
      const career = await api.getCareer(goal.career_id);
      const savedProfile = await api.getProfile(userId).catch((error) => {
        if (error.status === 404) return null;
        throw error;
      });

      setCurrentUser(user);
      setCurrentGoal(goal);
      setSelectedCareer(career);
      setCareerDetails(career);
      setAnalysisResult(analysis);
      setRoadmap(savedRoadmap);
      if (savedProfile) {
        setProfile({
          email: user.email || '',
          education: savedProfile.education || '',
          year: savedProfile.year || '',
          interests: savedProfile.interests || '',
        });
      } else {
        setProfile((prev) => ({ ...prev, email: user.email || '' }));
      }
    } catch (error) {
      if (error.status === 404 || error.status === 422) {
        clearStoredIds();
      } else {
        setSessionError('We could not restore your saved session. Check the backend and retry.');
      }
    } finally {
      setSessionLoading(false);
    }
  }, []);

  useEffect(() => {
    const timer = window.setTimeout(() => { restoreSession(); }, 0);
    return () => window.clearTimeout(timer);
  }, [restoreSession]);

  const selectCareer = useCallback(async (career) => {
    if (!career) return;
    setSelectedCareer(career);
    setCareerDetails(null);
    setSkillLevels({});
    setRoadmap(null);
    setIsLoadingDetails(true);
    try {
      const details = await api.getCareer(career.id);
      setCareerDetails(details);
    } catch {
      setSessionError('Unable to load the skills for this career. Please retry.');
    } finally {
      setIsLoadingDetails(false);
    }
  }, []);

  const setSkillLevel = useCallback((skillId, level) => {
    setSkillLevels((prev) => ({ ...prev, [skillId]: level }));
  }, []);

  const updateProfile = useCallback((fields) => {
    setProfile((prev) => ({ ...prev, ...fields }));
  }, []);

  const runAnalysis = useCallback(async () => {
    if (!profile.email?.trim()) throw new Error('Email is required.');
    if (!selectedCareer || !careerDetails) throw new Error('Please select a career goal.');

    const requiredSkills = careerDetails.career_skills || [];
    const unrated = requiredSkills.filter((skill) => skillLevels[skill.skill_id] === undefined);
    if (unrated.length) throw new Error('Please rate every required skill before continuing.');

    setIsAnalyzing(true);
    setAnalysisError(null);
    setRoadmapError(null);

    try {
      const user = await api.createUser(profile.email.trim());
      setCurrentUser(user);
      await api.upsertProfile(user.id, profile);
      await api.batchUpdateStudentSkills(
        user.id,
        requiredSkills.map((skill) => ({
          skill_id: skill.skill_id,
          level: Number(skillLevels[skill.skill_id]),
          source: 'self_assessed',
        })),
      );

      const goal = await api.createCareerGoal(user.id, selectedCareer.id, 'active');
      setCurrentGoal(goal);

      const result = await api.createGapAnalysis(goal.id);
      setAnalysisResult(result);

      setIsLoadingRoadmap(true);
      const generatedRoadmap = await api.createRoadmap(goal.id);
      setRoadmap(generatedRoadmap);

      localStorage.setItem(USER_ID_KEY, String(user.id));
      localStorage.setItem(GOAL_ID_KEY, String(goal.id));
      return result;
    } catch (error) {
      setAnalysisError(error.message || 'Failed to complete the analysis.');
      throw error;
    } finally {
      setIsLoadingRoadmap(false);
      setIsAnalyzing(false);
    }
  }, [profile, selectedCareer, careerDetails, skillLevels]);

  const updateRoadmapItem = useCallback(async (itemId, status) => {
    if (!currentGoal) throw new Error('No active career goal.');
    const updatedItem = await api.updateRoadmapItem(currentGoal.id, itemId, status);
    setRoadmap((previous) => {
      if (!previous) return previous;
      const items = previous.items.map((item) => item.id === itemId ? { ...item, status: updatedItem.status } : item);
      const done = items.filter((item) => item.status === 'done').length;
      return { ...previous, items, done, total: items.length, percent: items.length ? Number(((done / items.length) * 100).toFixed(2)) : 0 };
    });
    return updatedItem;
  }, [currentGoal]);

  const resetSession = useCallback(() => {
    clearStoredIds();
    setProfile({ email: '', education: '', year: '', interests: '' });
    setSelectedCareer(null);
    setCareerDetails(null);
    setSkillLevels({});
    setAnalysisResult(null);
    setRoadmap(null);
    setRoadmapError(null);
    setAnalysisError(null);
    setCurrentUser(null);
    setCurrentGoal(null);
    setSessionError(null);
  }, []);

  const value = useMemo(() => ({
    profile, updateProfile, careers, selectedCareer, selectCareer, careerDetails,
    isLoadingCareers, isLoadingDetails, skillLevels, setSkillLevel,
    analysisResult, roadmap, isLoadingRoadmap, roadmapError, isAnalyzing, analysisError,
    runAnalysis, updateRoadmapItem, currentUser, currentGoal, sessionLoading, sessionError,
    restoreSession, resetSession,
  }), [
    profile, updateProfile, careers, selectedCareer, selectCareer, careerDetails,
    isLoadingCareers, isLoadingDetails, skillLevels, setSkillLevel, analysisResult,
    roadmap, isLoadingRoadmap, roadmapError, isAnalyzing, analysisError, runAnalysis,
    updateRoadmapItem, currentUser, currentGoal, sessionLoading, sessionError,
    restoreSession, resetSession,
  ]);

  return <MentorContext.Provider value={value}>{children}</MentorContext.Provider>;
}
