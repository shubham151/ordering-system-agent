<script lang="ts">
  import { onMount } from 'svelte';
  import { orderState, totals, orders, isLoading, error, lastResponse } from '../stores/orderStore';
  import { appLogic, messageLogic } from '../logic/appLogic';
  import TotalCard from '../components/ui/TotalCard/TotalCard.svelte';
  import MessageInput from '../components/ui/MessageInput/MessageInput.svelte';
  import StatusMessage from '../components/ui/StatusMessage/StatusMessage.svelte';
  import OrderHistory from '../components/ui/OrderHistory/OrderHistory.svelte';
  import burgerIcon from '../../assets/hamburger.png'
  import friesIcon from '../../assets/french-fries.png'
  import drinkIcon from '../../assets/drink.png'
  
  let currentMessage = '';
  
  onMount(() => {
    appLogic.initialize();
  });
  
  const handleMessageChange = (message: string) => {
    currentMessage = message;
  };
  
  const handleSubmit = async () => {
    if (!messageLogic.canSubmit(currentMessage, $isLoading)) return;
    
    await appLogic.processMessage(currentMessage);
    currentMessage = '';
  };
  
  const handleCancelOrder = async (orderId: string) => {
    await appLogic.cancelOrder(orderId);
  };
  
  $: totalCards = [
    { title: 'Total # of burgers', value: $totals.burgers, icon: burgerIcon, color: 'red' as const },
    { title: 'Total # of fries', value: $totals.fries, icon: friesIcon, color: 'yellow' as const },
    { title: 'Total # of drinks', value: $totals.drinks, icon: drinkIcon, color: 'blue' as const }
  ];
</script>

<main class="min-h-screen bg-gradient-to-br from-orange-50 to-red-50 p-4">
  <div class="max-w-4xl mx-auto">
    <!-- Header -->
    <header class="text-center mb-8">
      <h1 class="text-4xl font-bold text-gray-800 mb-2"> Drive Thru Ordering System</h1>
      <p class="text-gray-600">AI-powered natural language ordering</p>
    </header>
    
    <!-- Totals Display -->
    <section class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-8" aria-label="Order totals">
      {#each totalCards as card (card.title)}
        <TotalCard {...card} />
      {/each}
    </section>
    
    <!-- Message Input -->
    <section class="mb-8" aria-label="Order input">
      <MessageInput
  bind:message={currentMessage}
  isLoading={$isLoading}
  onSubmit={handleSubmit}
/>

      
      <!-- Status Messages -->
      {#if $lastResponse}
        <div class="mt-4">
          <StatusMessage type="success" message={$lastResponse} />
        </div>
      {/if}
      
      {#if $error}
        <div class="mt-4">
          <StatusMessage type="error" message={$error} />
        </div>
      {/if}
    </section>
    
    <!-- Order History -->
    <section aria-label="Order history">
      <OrderHistory 
        orders={$orders} 
        onCancelOrder={handleCancelOrder}
      />
    </section>
    
    <!-- Footer -->
    <footer class="text-center mt-8 text-sm text-gray-500">
      <p>Powered by AI • Natural Language Processing</p>
    </footer>
  </div>
</main>
