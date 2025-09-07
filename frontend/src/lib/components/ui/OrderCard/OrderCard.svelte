<script lang="ts">
  import { formatOrderItems } from '../../../utils/order';
  import type { OrderCardProps } from '../../../types';
  
  export let id: OrderCardProps['id'];
  export let order: OrderCardProps['order'];
  export let onCancel: OrderCardProps['onCancel'] = undefined;
  
  const handleCancel = () => {
    if (onCancel) {
      onCancel(id);
    }
  };
  
  $: formattedItems = formatOrderItems(order);
</script>

<div class="flex items-center justify-between p-4 bg-gray-50 rounded-lg border">
  <div class="flex items-center gap-3">
    <div class="bg-blue-100 text-blue-800 px-3 py-1 rounded-full text-sm font-medium">
      Order #{id}
    </div>
    <div class="text-gray-700">
      {formattedItems}
    </div>
  </div>
  
  <div class="flex items-center gap-2">
    <div class="text-sm text-gray-500">Active</div>
    {#if onCancel}
      <button
        on:click={handleCancel}
        class="text-red-600 hover:text-red-800 text-sm font-medium px-2 py-1 rounded hover:bg-red-50 transition-colors"
      >
        Cancel
      </button>
    {/if}
  </div>
</div>