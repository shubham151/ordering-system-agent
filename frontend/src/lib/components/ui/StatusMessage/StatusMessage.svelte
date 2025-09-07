<script lang="ts">
  import type { StatusMessageProps } from '../../../types';
  import successIcon from '../../../../assets/success.svg'
  import failureIcon from '../../../../assets/failure.svg'
  
  export let type: StatusMessageProps['type'];
  export let message: StatusMessageProps['message'];
  
  const styles = {
    success: {
      container: 'bg-green-50 border-green-200',
      icon: 'text-green-600',
      text: 'text-green-800',
      iconSymbol: successIcon,
      title: "Success"
    },
    error: {
      container: 'bg-red-50 border-red-200',
      icon: 'text-red-600', 
      text: 'text-red-800',
      iconSymbol: failureIcon,
      title: "Failure"
    }
  };
  
  $: currentStyle = styles[type];
</script>

<div class="p-3 border rounded-lg {currentStyle.container}">
  <div class="flex items-start gap-2">
    <div class="mt-0.5 {currentStyle.icon}">
      <img src={currentStyle.iconSymbol} alt={currentStyle.title} class="w-10 h-10 object-contain" />
    </div>
    <p class="text-sm {currentStyle.text}">{message}</p>
  </div>
</div>