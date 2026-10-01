const BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api/v1';

async function request(endpoint, options = {}) {
  const response = await fetch(`${BASE_URL}${endpoint}`, {
    headers: { 'Content-Type': 'application/json', ...options.headers },
    ...options,
  });

  if (!response.ok) {
    let detail = `Request failed with status ${response.status}`;
    try {
      const body = await response.json();
      if (body?.detail) detail = typeof body.detail === 'string' ? body.detail : JSON.stringify(body.detail);
    } catch {
      // Non-JSON error response.
    }
    const error = new Error(detail);
    error.status = response.status;
    throw error;
  }

  return response.status === 204 ? null : response.json();
}

export const api = {
  async checkHealth() { return request('/health'); },
  async getCareers() { return request('/careers'); },
  async getCareer(careerId) { return request(`/careers/${careerId}`); },
  async createUser(email) {
    return request('/users', { method: 'POST', body: JSON.stringify({ email }) });
  },
  async getUser(userId) { return request(`/users/${userId}`); },
  async getProfile(userId) { return request(`/users/${userId}/profile`); },
  async upsertProfile(userId, profileData) {
    return request(`/users/${userId}/profile`, {
      method: 'POST',
      body: JSON.stringify({
        education: profileData.education || null,
        year: profileData.year || null,
        interests: profileData.interests || null,
      }),
    });
  },
  async batchUpdateStudentSkills(userId, skills) {
    return request(`/users/${userId}/skills`, {
      method: 'PUT',
      body: JSON.stringify(skills),
    });
  },
  async createCareerGoal(userId, careerId, status = 'active') {
    return request(`/users/${userId}/goals`, {
      method: 'POST',
      body: JSON.stringify({ career_id: Number(careerId), status }),
    });
  },
  async getCareerGoal(userId, goalId) {
    return request(`/users/${userId}/goals/${goalId}`);
  },
  async createGapAnalysis(goalId) {
    return request(`/goals/${goalId}/gap-analysis`, { method: 'POST' });
  },
  async getLatestGapAnalysis(goalId) {
    return request(`/goals/${goalId}/gap-analysis/latest`);
  },
  async createRoadmap(goalId) {
    return request(`/goals/${goalId}/roadmap`, { method: 'POST' });
  },
  async getLatestRoadmap(goalId) {
    return request(`/goals/${goalId}/roadmap/latest`);
  },
  async updateRoadmapItem(goalId, itemId, status) {
    return request(`/goals/${goalId}/roadmap/items/${itemId}`, {
      method: 'PATCH',
      body: JSON.stringify({ status }),
    });
  },
};
