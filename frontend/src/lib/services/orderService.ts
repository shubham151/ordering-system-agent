import { processMessage, getOrders } from "../core/Api";
import { validateMessage } from "../utils/validations";
import { generateDefaultMessage } from "../utils/order";
import type { OrderResponse, ValidationResult } from "../types";

export const processOrderRequest = async (
  message: string
): Promise<OrderResponse> => {
  const validation = validateMessage(message);
  if (!validation.isValid) {
    throw new Error(validation.error || "Invalid message");
  }
  return await processMessage(message);
};

export const loadInitialOrders = async () => {
  try {
    return await getOrders();
  } catch (error) {
    console.error("Failed to load orders:", error);
    return {
      orders: {},
      totals: { burgers: 0, fries: 0, drinks: 0 },
    };
  }
};

export const createSuccessMessage = (result: OrderResponse): string =>
  result.message || generateDefaultMessage(result);

export const createErrorMessage = (error: unknown): string => {
  if (error instanceof Error) {
    return error.message;
  }
  return "Unable to connect to the ordering system. Please try again.";
};

export const validateOrderMessage = (message: string): ValidationResult =>
  validateMessage(message);

export const orderProcessingPipeline = {
  validate: validateOrderMessage,
  process: processOrderRequest,
  createSuccessMessage,
  createErrorMessage,
};
