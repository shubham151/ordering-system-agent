import { orderActions } from "../stores/orderStore";
import {
  processOrderRequest,
  loadInitialOrders,
  createSuccessMessage,
  createErrorMessage,
} from "../services/orderService";

export const appLogic = {
  async initialize() {
    try {
      const { orders, totals } = (await loadInitialOrders()) as any;
      orderActions.updateOrders(totals, orders);
    } catch (error) {
      console.error("Failed to initialize app:", error);
      orderActions.setError("Failed to load initial data");
    }
  },

  async processMessage(message: string) {
    orderActions.setLoading(true);
    orderActions.clearMessages();

    try {
      const result = await processOrderRequest(message);

      if (result.success) {
        orderActions.updateOrders(result.totals, result.orders);
        orderActions.setSuccess(createSuccessMessage(result));
      } else {
        orderActions.setError(
          result.message || "Failed to process your request"
        );
      }
    } catch (error) {
      orderActions.setError(createErrorMessage(error));
    } finally {
      orderActions.setLoading(false);
    }
  },

  async cancelOrder(orderId: string) {
    const message = `Cancel order ${orderId}`;
    await this.processMessage(message);
  },

  clearMessages() {
    orderActions.clearMessages();
  },

  reset() {
    orderActions.reset();
  },
};

export const messageLogic = {
  validate: (message: string) => {
    const trimmed = message.trim();
    return {
      isValid: trimmed.length > 0,
      isEmpty: trimmed.length === 0,
      isTooLong: trimmed.length > 500,
    };
  },

  getValidationMessage: (message: string) => {
    const { isEmpty, isTooLong } = messageLogic.validate(message);

    if (isEmpty) return "Please enter a message";
    if (isTooLong) return "Message is too long (max 500 characters)";
    return "";
  },

  canSubmit: (message: string, isLoading: boolean) => {
    const { isValid } = messageLogic.validate(message);
    return isValid && !isLoading;
  },
};

export const uiLogic = {
  handleKeyPress: (event: KeyboardEvent, onSubmit: () => void) => {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      onSubmit();
    }
  },

  focusInput: (inputId: string) => {
    const input = document.getElementById(inputId);
    input?.focus();
  },

  scrollToElement: (elementId: string) => {
    const element = document.getElementById(elementId);
    element?.scrollIntoView({ behavior: "smooth" });
  },
};
