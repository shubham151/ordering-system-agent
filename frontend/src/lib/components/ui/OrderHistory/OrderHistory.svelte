<script lang="ts">
  import OrderCard from '../OrderCard/OrderCard.svelte';
  import type { Order } from '../../../types';
  import cartIcon from '../../../../assets/cart.png'
  
  export let orders: Record<string, Order>;
  export let onCancelOrder: ((id: string) => void) | undefined = undefined;
  const title = "Cart"
  $: orderEntries = Object.entries(orders);
  $: orderCount = orderEntries.length;
  $: hasOrders = orderCount > 0;
</script>

<div class="bg-white rounded-lg shadow-md">
  <div class="px-6 py-4 border-b border-gray-200">
    <h2 class="text-xl font-semibold text-gray-800">Order History</h2>
    <p class="text-sm text-gray-600 mt-1">
      {orderCount} active order{orderCount !== 1 ? 's' : ''}
    </p>
  </div>
  
  <div class="p-6">
    {#if !hasOrders}
      <div class="text-center py-8">
        <div class="text-6xl mb-4"><img src={cartIcon} alt={title} class="mx-auto mb-4 w-16 h-16 object-contain" /></div>
        <p class="text-gray-500 text-lg">No active orders</p>
        <p class="text-gray-400 text-sm mt-2">Place your first order using the input above!</p>
      </div>
    {:else}
      <div class="space-y-3">
        {#each orderEntries as [id, order] (id)}
          <OrderCard 
            {id} 
            {order} 
            onCancel={onCancelOrder}
          />
        {/each}
      </div>
    {/if}
  </div>
</div>