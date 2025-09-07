import { writable, derived } from "svelte/store";
import type { AppState, OrderTotals, Order } from "../types";

const initialState: AppState = {
  totals: { burgers: 0, fries: 0, drinks: 0 },
  orders: {},
  isLoading: false,
  error: "",
  lastResponse: "",
};

export const orderState = writable<AppState>(initialState);

export const totals = derived(orderState, ($state) => $state.totals);
export const orders = derived(orderState, ($state) => $state.orders);
export const isLoading = derived(orderState, ($state) => $state.isLoading);
export const error = derived(orderState, ($state) => $state.error);
export const lastResponse = derived(
  orderState,
  ($state) => $state.lastResponse
);

export const hasOrders = derived(
  orders,
  ($orders) => Object.keys($orders).length > 0
);
export const orderCount = derived(
  orders,
  ($orders) => Object.keys($orders).length
);
export const totalItems = derived(
  totals,
  ($totals) => $totals.burgers + $totals.fries + $totals.drinks
);

export const orderActions = {
  setLoading: (loading: boolean) =>
    orderState.update((state) => ({ ...state, isLoading: loading })),

  setError: (error: string) =>
    orderState.update((state) => ({ ...state, error, lastResponse: "" })),

  setSuccess: (message: string) =>
    orderState.update((state) => ({
      ...state,
      lastResponse: message,
      error: "",
    })),

  updateOrders: (totals: OrderTotals, orders: Record<string, Order>) =>
    orderState.update((state) => ({ ...state, totals, orders })),

  clearMessages: () =>
    orderState.update((state) => ({ ...state, error: "", lastResponse: "" })),

  reset: () => orderState.set(initialState),
};

export const selectOrderById = (
  orders: Record<string, Order>,
  id: string
): Order | undefined => orders[id];

export const selectOrdersByType = (
  orders: Record<string, Order>,
  hasItem: keyof Order
) => Object.entries(orders).filter(([_, order]) => order[hasItem] > 0);

export const selectLargestOrder = (
  orders: Record<string, Order>
): [string, Order] | null => {
  const entries = Object.entries(orders);
  if (entries.length === 0) return null;

  return entries.reduce((largest, current) => {
    const currentTotal =
      current[1].burgers + current[1].fries + current[1].drinks;
    const largestTotal =
      largest[1].burgers + largest[1].fries + largest[1].drinks;
    return currentTotal > largestTotal ? current : largest;
  });
};
