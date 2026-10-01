const BASE_URL = import.meta.env.VITE_API_URL || 'http://127.0.0.1:8000/api/v1';

/**
 * Generic request helper with error handling
 */
async function request(endpoint, options = {}) {
  const url = `${BASE_URL}${endpoint}`;
  const config = {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  };

  const response = await fetch(url, config);

  if (!response.ok) {
    let errorDetail = `Request failed with status ${response.status}`;
    try {
      const errorJson = await response.json();
      if (errorJson && errorJson.detail) {
        errorDetail = typeof errorJson.detail === 'string'
          ? errorJson.detail
          : JSON.stringify(errorJson.detail);
      }
    } catch {
      // response wasn't JSON
    }
    const error = new Error(errorDetail);
    error.status = response.status;
    throw error;
  }

  // Check if no content (e.g. 204)
  if (response.status === 204) {
    return null;
  }

  return response.json();
}

export const api = {
  /**
   * Health check
   */
  async checkHealth() {
    return request('/health');
  },

  /**
   * List all careers
   */
  async getCareers() {
    return request('/careers');
  },

  /**
   * Get career details with required skills
   */
  async getCareer(careerId) {
    return request(`/careers/${careerId}`);
  },

  /**
   * List all users
   */
  async getUsers() {
    return request('/users');
  },

  /**
   * Get or create a user by email
   */
  async getOrCreateUser(email) {
    try {
      const user = await request('/users', {
        method: 'POST',
        body: JSON.stringify({ email }),
      });
      return user;
    } catch (err) {
      if (err.status === 409) {
        // User already exists; find in users list
        const users = await request('/users');
        const existing = users.find(
          (u) => u.email.toLowerCase() === email.trim().toLowerCase()
        );
        if (existing) {
          return existing;
        }
      }
      throw err;
    }
  },

  /**
   * Create or update student profile
   */
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

  /**
   * Upsert a student skill level (1-5)
   */
  async upsertStudentSkill(userId, skillId, level, source = 'self_assessed') {
    return request(`/users/${userId}/skills`, {
      method: 'POST',
      body: JSON.stringify({
        skill_id: skillId,
        level: Number(level),
        source: source,
      }),
    });
  },

  /**
   * Create a career goal for a user
   */
  async createCareerGoal(userId, careerId, status = 'active') {
    return request(`/users/${userId}/goals`, {
      method: 'POST',
      body: JSON.stringify({
        career_id: Number(careerId),
        status: status,
      }),
    });
  },

  /**
   * Run and create gap analysis snapshot for a career goal
   */
  async createGapAnalysis(goalId) {
    return request(`/goals/${goalId}/gap-analysis`, {
      method: 'POST',
    });
  },

  /**
   * Get latest gap analysis snapshot for a career goal
   */
  async getLatestGapAnalysis(goalId) {
    return request(`/goals/${goalId}/gap-analysis/latest`);
  },
};
