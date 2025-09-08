import type { Order, OrderResponse, OrderTotals, ItemType } from "$lib/types";

export const formatOrderItems = (order: Order): string => {
  const items = [];

  if (order.burgers > 0) {
    items.push(`${order.burgers} Burger${order.burgers !== 1 ? "s" : ""}`);
  }
  if (order.fries > 0) {
    items.push(`${order.fries} Fries`);
  }
  if (order.drinks > 0) {
    items.push(`${order.drinks} Drink${order.drinks !== 1 ? "s" : ""}`);
  }

  return items.join(", ") || "Empty order";
};

export const formatItemName = (type: ItemType, count: number): string => {
  const names = {
    burgers: count === 1 ? "burger" : "burgers",
    fries: "fries",
    drinks: count === 1 ? "drink" : "drinks",
  };
  return names[type];
};

export const createOrderSummary = (order: Order): string => {
  const items = Object.entries(order)
    .filter(([_, count]) => count > 0)
    .map(
      ([type, count]) => `${count} ${formatItemName(type as ItemType, count)}`
    );

  return items.join(", ");
};

export const generateDefaultMessage = (result: OrderResponse): string => {
  if (result.action === "placed" && result.order_id && result.items) {
    const summary = createOrderSummary(result.items);
    return `Order #${result.order_id} placed: ${summary}`;
  }

  if (result.action === "canceled" && result.order_id) {
    return `Order #${result.order_id} has been canceled`;
  }

  return "Request processed successfully";
};

export const calculateTotalItems = (totals: OrderTotals): number =>
  totals.burgers + totals.fries + totals.drinks;

export const isEmptyOrder = (order: Order): boolean =>
  order.burgers === 0 && order.fries === 0 && order.drinks === 0;

export const hasActiveOrders = (orders: Record<string, Order>): boolean =>
  Object.keys(orders).length > 0;

export const getOrderCount = (orders: Record<string, Order>): number =>
  Object.keys(orders).length;
