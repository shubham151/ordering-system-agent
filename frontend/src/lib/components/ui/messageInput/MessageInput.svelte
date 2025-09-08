<script lang="ts">
  import Button from '$lib/components/ui/button/button.svelte';
  import { cn } from "$lib/utils/common";
  import type { MessageInputProps } from '$lib/types';
  
  export let message: MessageInputProps['message'];
  export let isLoading: MessageInputProps['isLoading'];
  export let onSubmit: MessageInputProps['onSubmit'];
  
  const handleKeyDown = (event: KeyboardEvent) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      onSubmit();
    }
  };

  $: isSubmitDisabled = isLoading || !message.trim();
</script>

<div class="bg-white rounded-lg shadow-md p-6">
  <div class="space-y-4">
    <div>
      <label for="message-input" class="block text-sm font-medium text-gray-700 mb-2">
        Drive thru message:
      </label>
      <div class="text-xs text-gray-500 mb-3">
        Ex: "I would like one burger and an order of fries", "Cancel order #2"
      </div>
    </div>
    
    <div class="flex gap-3">
      <input
        id="message-input"
        bind:value={message}
        on:keydown={handleKeyDown}
        placeholder="Enter your order or cancellation request..."
        disabled={isLoading}
        class="flex-1 px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent disabled:bg-gray-100 disabled:cursor-not-allowed text-base"
      />
      
      <Button
        on:click={onSubmit}
        disabled={isSubmitDisabled}
        class={cn(
          "px-8 py-3 text-base font-medium rounded-lg transition-all duration-200",
          isLoading
            ? "bg-gray-400 cursor-not-allowed"
            : "bg-blue-600 hover:bg-blue-700 text-white shadow-md hover:shadow-lg"
        )}
      >
        {#if isLoading}
          <div class="flex items-center gap-2">
            <div class="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            Processing...
          </div>
        {:else}
          Run
        {/if}
      </Button>
    </div>
  </div>
</div>
