/**
 * API Client
 * Handles all API requests to the backend
 */

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:4000';

interface ApiResponse<T> {
  data?: T;
  error?: string;
}

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  private getHeaders(): HeadersInit {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
    };

    // Add auth token if available
    if (typeof window !== 'undefined') {
      const token = localStorage.getItem('access_token');
      if (token) {
        headers['Authorization'] = `Bearer ${token}`;
      }
    }

    return headers;
  }

  async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<ApiResponse<T>> {
    try {
      const headers = this.getHeaders();
      
      const response = await fetch(`${this.baseUrl}${endpoint}`, {
        ...options,
        headers: {
          ...headers,
          ...options.headers,
        },
      });

      // Handle 204 No Content responses (no body to parse)
      if (response.status === 204) {
        return { data: undefined as T };
      }

      const data = await response.json();

      if (!response.ok) {
        // If 401 and we have a refresh token, try to refresh
        if (response.status === 401 && typeof window !== 'undefined') {
          const refreshToken = localStorage.getItem('refresh_token');
          if (refreshToken && !endpoint.includes('/auth/')) {
            const refreshResult = await this.refreshAccessToken(refreshToken);
            if (refreshResult.success) {
              // Retry the original request with new token
              return this.request<T>(endpoint, options);
            }
          }
        }
        
        // Handle 404 errors specifically
        if (response.status === 404) {
          return {
            error: 'Not Found',
          };
        }
        
        return {
          error: data.detail || `Error ${response.status}`,
        };
      }

      return { data };
    } catch (error) {
      console.error('API Request Error:', error);
      
      // Provide more specific error messages
      if (error instanceof TypeError && error.message === 'Failed to fetch') {
        return {
          error: 'Network error - please check your connection or try again',
        };
      }
      
      return {
        error: error instanceof Error ? error.message : 'Network error',
      };
    }
  }

  private async refreshAccessToken(refreshToken: string): Promise<{ success: boolean }> {
    try {
      const response = await fetch(`${this.baseUrl}/v1/auth/refresh`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ refresh_token: refreshToken }),
      });

      if (response.ok) {
        const data = await response.json();
        localStorage.setItem('access_token', data.access_token);
        if (data.refresh_token) {
          localStorage.setItem('refresh_token', data.refresh_token);
        }
        return { success: true };
      }
      
      return { success: false };
    } catch (error) {
      console.error('Token refresh error:', error);
      return { success: false };
    }
  }

  // Auth endpoints
  async signup(userData: {
    email: string;
    username: string;
    password: string;
    full_name?: string;
    date_of_birth: string;
  }) {
    return this.request('/v1/auth/signup', {
      method: 'POST',
      body: JSON.stringify(userData),
    });
  }

  async login(credentials: { email: string; password: string }) {
    return this.request('/v1/auth/login', {
      method: 'POST',
      body: JSON.stringify(credentials),
    });
  }

  // User endpoints
  async getCurrentUser() {
    return this.request('/v1/users/me', {
      method: 'GET',
    });
  }

  // Wallet endpoints
  async getWallet() {
    return this.request('/v1/wallet', {
      method: 'GET',
    });
  }

  async getTransactions() {
    return this.request('/v1/wallet/transactions', {
      method: 'GET',
    });
  }

  // Match endpoints
  async getTodayMatches() {
    return this.request('/v1/matches/today', {
      method: 'GET',
    });
  }

  async getMatch(matchId: number) {
    return this.request(`/v1/matches/${matchId}`, {
      method: 'GET',
    });
  }

  // Calendar endpoints
  async getCalendarMatches(params: {
    start_date: string;
    end_date: string;
    league_id?: number;
    status?: string;
  }) {
    const queryParams = new URLSearchParams();
    queryParams.append('start_date', params.start_date);
    queryParams.append('end_date', params.end_date);
    if (params.league_id) {
      queryParams.append('league_id', params.league_id.toString());
    }
    if (params.status) {
      queryParams.append('status', params.status);
    }

    return this.request(`/v1/matches/calendar/matches?${queryParams.toString()}`, {
      method: 'GET',
    });
  }

  async getAvailableLeagues(start_date: string, end_date: string) {
    const queryParams = new URLSearchParams();
    queryParams.append('start_date', start_date);
    queryParams.append('end_date', end_date);

    return this.request(`/v1/matches/calendar/leagues?${queryParams.toString()}`, {
      method: 'GET',
    });
  }

  // Room endpoints
  async joinRoom(matchId: number) {
    return this.request(`/v1/rooms/join/${matchId}`, {
      method: 'POST',
    });
  }

  async unlockChat(matchId: number) {
    return this.request(`/v1/rooms/unlock-chat/${matchId}`, {
      method: 'POST',
    });
  }

  async sendMessage(matchId: number) {
    return this.request(`/v1/rooms/send-message/${matchId}`, {
      method: 'POST',
    });
  }

  // Fantasy endpoints
  async getFantasyTeam() {
    return this.request('/v1/fantasy/team', {
      method: 'GET',
    });
  }

  async getFantasyPlayers(params?: {
    position?: string;
    team?: string;
    min_cost?: number;
    max_cost?: number;
    search?: string;
  }) {
    const queryParams = new URLSearchParams();
    if (params?.position) queryParams.append('position', params.position);
    if (params?.team) queryParams.append('team', params.team);
    if (params?.min_cost) queryParams.append('min_cost', params.min_cost.toString());
    if (params?.max_cost) queryParams.append('max_cost', params.max_cost.toString());
    if (params?.search) queryParams.append('search', params.search);

    const query = queryParams.toString();
    return this.request(`/v1/fantasy/players${query ? '?' + query : ''}`, {
      method: 'GET',
    });
  }

  async createFantasyTeam(teamData: {
    name: string;
    formation: string;
    player_ids: number[];
    captain_player_id: number;
  }) {
    return this.request('/v1/fantasy/team', {
      method: 'POST',
      body: JSON.stringify(teamData),
    });
  }

  async updateFantasyTeam(teamData: {
    name?: string;
    formation?: string;
    player_ids?: number[];
    captain_player_id?: number;
  }) {
    return this.request('/v1/fantasy/team', {
      method: 'PUT',
      body: JSON.stringify(teamData),
    });
  }

  async deleteFantasyTeam() {
    return this.request('/v1/fantasy/team', {
      method: 'DELETE',
    });
  }

  async getFantasyLeaderboard(limit: number = 10) {
    return this.request(`/v1/fantasy/leaderboard?limit=${limit}`, {
      method: 'GET',
    });
  }
}

export const api = new ApiClient(API_URL);
