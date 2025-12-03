/**
 * API client for Travel Planner backend
 */
import axios, { AxiosError } from 'axios';

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

export interface TravelPlanRequest {
  destination: string;
  origin?: string;
  departure_date?: string;
  return_date?: string;
  budget_level?: 'tight' | 'moderate' | 'flexible';
  interests?: string[];
  trip_type?: 'solo' | 'couple' | 'family' | 'friends';
  duration_days?: number;
}

export interface FlightOption {
  price: number;
  currency: string;
  duration: string;
  segments: number;
  one_way: boolean;
}

export interface HotelOption {
  name: string;
  rating: string;
  price_per_night: number;
  total_price: number;
  currency: string;
  area: string;
}

export interface Attraction {
  name: string;
  rating: number;
  types: string[];
  vicinity: string;
  coordinates: { lat: number; lng: number };
  description?: string;
}

export interface BudgetEstimate {
  daily_total: number;
  meals: number;
  transport: number;
  accommodation: number;
  airport_transfer?: number;
}

export interface TravelPlanResponse {
  destination: string;
  origin?: string;
  best_dates: string;
  weather_summary: string;
  flight_options: FlightOption[];
  hotel_options: HotelOption[];
  budget_estimate: {
    tight?: BudgetEstimate;
    moderate?: BudgetEstimate;
    flexible?: BudgetEstimate;
  };
  attractions: Record<string, Attraction[]>;
  itinerary: string;
  tips: any;
  execution_time?: number;
}

export interface ApiError {
  detail: string;
}

const api = axios.create({
  baseURL: API_URL,
  timeout: 180000, // 3 minutes for complex planning
  headers: {
    'Content-Type': 'application/json',
  },
});

export const travelPlannerAPI = {
  /**
   * Create a travel plan
   */
  async createPlan(request: TravelPlanRequest): Promise<TravelPlanResponse> {
    try {
      const response = await api.post<TravelPlanResponse>('/plan', request);
      return response.data;
    } catch (error) {
      if (axios.isAxiosError(error)) {
        const axiosError = error as AxiosError<ApiError>;
        throw new Error(
          axiosError.response?.data?.detail || 'Failed to create travel plan'
        );
      }
      throw error;
    }
  },

  /**
   * Health check
   */
  async healthCheck(): Promise<{ status: string }> {
    const response = await api.get('/health');
    return response.data;
  },

  /**
   * Get popular destinations
   */
  async getPopularDestinations(): Promise<any> {
    const response = await api.get('/destinations/popular');
    return response.data;
  },
};

export default travelPlannerAPI;
