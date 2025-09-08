const getApiBaseUrl = (): string => {
  if (typeof window !== "undefined") {
    return (window as any).__API_URL__ || "http://localhost:8000";
  }
  return "http://localhost:8000";
};

const API_BASE_URL = getApiBaseUrl();

export type { OrderTotals, Order, OrderResponse, OrderRequest } from "../types";

interface ApiError {
  detail?: string;
  message?: string;
}

const createApiClient = (baseUrl: string, timeout = 30000) => {
  const apiUrl = baseUrl.replace(/\/$/, "");

  const fetchWithTimeout = async (
    url: string,
    options: RequestInit = {}
  ): Promise<Response> => {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeout);

    try {
      const response = await fetch(url, {
        ...options,
        signal: controller.signal,
        headers: {
          "Content-Type": "application/json",
          ...options.headers,
        },
      });

      clearTimeout(timeoutId);
      return response;
    } catch (error) {
      clearTimeout(timeoutId);

      if (error instanceof Error && error.name === "AbortError") {
        throw new Error("Request timed out. Please try again.");
      }

      throw error;
    }
  };

  const handleResponse = async <T>(response: Response): Promise<T> => {
    if (!response.ok) {
      let errorMessage = `HTTP ${response.status}: ${response.statusText}`;

      try {
        const errorData: ApiError = await response.json();
        errorMessage = errorData.detail || errorData.message || errorMessage;
      } catch {
      }

      throw new Error(errorMessage);
    }

    try {
      return await response.json();
    } catch (error) {
      throw new Error("Invalid response format from server");
    }
  };

  return {
    async processMessage(message: string) {
      if (!message?.trim()) {
        throw new Error("Message cannot be empty");
      }

      const response = await fetchWithTimeout(`${apiUrl}/api/v1/process`, {
        method: "POST",
        body: JSON.stringify({ message: message.trim() }),
      });

      return handleResponse(response);
    },

    async getOrders() {
      const response = await fetchWithTimeout(`${apiUrl}/api/v1/orders`);
      return handleResponse(response);
    },

    async cancelOrder(orderId: number) {
      const response = await fetchWithTimeout(
        `${apiUrl}/api/v1/orders/${orderId}`,
        {
          method: "DELETE",
        }
      );

      return handleResponse(response);
    },

    async healthCheck() {
      const response = await fetchWithTimeout(`${apiUrl}/health`);
      return handleResponse(response);
    },

    async testConnection() {
      try {
        await this.healthCheck();
        return true;
      } catch {
        return false;
      }
    },
  };
};

// Create API client instance
const apiClient = createApiClient(API_BASE_URL);

// Exported functions (functional approach)
export const processMessage = (message: string) =>
  apiClient.processMessage(message);

export const getOrders = () => apiClient.getOrders();

export const cancelOrder = (orderId: number) => apiClient.cancelOrder(orderId);

export const healthCheck = () => apiClient.healthCheck();

export const testConnection = () => apiClient.testConnection();

// Utility functions
export const isApiError = (error: unknown): error is Error =>
  error instanceof Error;

export const getApiErrorMessage = (error: unknown): string => {
  if (isApiError(error)) {
    return error.message;
  }
  return "An unexpected error occurred";
};

// API client factory for testing or different environments
export const createCustomApiClient = (
  baseUrl: string,
  options?: { timeout?: number }
) => createApiClient(baseUrl, options?.timeout);

// Export singleton for advanced usage
export const DriveThruApi = apiClient;
