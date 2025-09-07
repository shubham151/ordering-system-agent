export interface OrderTotals {
  burgers: number;
  fries: number;
  drinks: number;
}

export interface Order {
  burgers: number;
  fries: number;
  drinks: number;
}

export interface OrderResponse {
  success: boolean;
  action: "placed" | "canceled" | "error" | "none";
  order_id?: number;
  items?: Order;
  message?: string;
  totals: OrderTotals;
  orders: Record<string, Order>;
}

export interface OrderRequest {
  message: string;
}

export interface AppState {
  totals: OrderTotals;
  orders: Record<string, Order>;
  isLoading: boolean;
  error: string;
  lastResponse: string;
}

export interface MessageState {
  value: string;
  isValid: boolean;
  errorMessage?: string;
}

export interface TotalCardProps {
  title: string;
  value: number;
  icon: string;
  color: "red" | "yellow" | "blue";
}

export interface OrderCardProps {
  id: string;
  order: Order;
  onCancel?: (id: string) => void;
}

export interface MessageInputProps {
  message: string;
  isLoading: boolean;
  onMessageChange: (message: string) => void;
  onSubmit: () => void;
}

export interface StatusMessageProps {
  type: "success" | "error";
  message: string;
}

export type ItemType = "burgers" | "fries" | "drinks";

export interface ValidationResult {
  isValid: boolean;
  error?: string;
}
